#!/usr/bin/env python

import json
import os

import boto
from boto.s3.connection import OrdinaryCallingFormat


class Cleaner:
    _connection = None
    _bucket = None
    _index = None
    _keep = None

    def __init__(self, access_key='', secret_key='', host='s3.amazonaws.com', port=443, is_secure=True,
                 bucket_name='registry', dry_run=True):
        self._access_key = access_key
        self._secret_key = secret_key
        self._host = host
        self._port = port
        self._is_secure = is_secure
        self._bucket_name = bucket_name
        self._dry_run = dry_run

    def get_connection(self):
        if self._connection is None:
            print 'Connecting to S3 storage repository...'
            self._connection = boto.connect_s3(
                aws_access_key_id=self._access_key,
                aws_secret_access_key=self._secret_key,
                host=self._host,
                port=self._port,
                is_secure=self._is_secure,
                calling_format=OrdinaryCallingFormat())
        return self._connection

    def get_bucket(self):
        if self._bucket is None:
            print 'Opening bucket...'
            self._bucket = self.get_connection().get_bucket(self._bucket_name)
        return self._bucket

    def get_index(self):
        if self._index is None:
            print 'Generating index of images...'
            self._index = dict()
            keys = self.get_bucket().list(prefix=self._bucket_name + '/repositories/')
            for key in keys:
                key_base = os.path.basename(key.key)
                if key_base.startswith('tag_'):
                    tag = key_base.replace('tag_', '', 1)
                    directory = os.path.dirname(key.key)
                    image = os.path.basename(directory)
                    repo = os.path.basename(os.path.dirname(directory))
                    slug = repo + '/' + image
                    image_hash = key.get_contents_as_string(encoding='utf-8')
                    if slug not in self._index:
                        self._index[slug] = dict()
                    self._index[slug][tag] = image_hash
        return self._index

    def get_tag_ancestry(self, image_hash):
        key = self.get_bucket().get_key(self._bucket_name + '/images/' + image_hash + "/ancestry")
        ancestry = []
        if key is not None:
            for ihash in json.loads(key.get_contents_as_string(encoding='utf-8')):
                ancestry.append(ihash)
        return ancestry

    def get_images_to_keep(self):
        if self._keep is None:
            print 'Generating list of used images...'
            self._keep = set()
            for repo_name, tags in self.get_index().iteritems():
                for tag, image_hash in tags.iteritems():
                    self._keep.update(self.get_tag_ancestry(image_hash))
        return self._keep

    def trim_repo_index(self, slug):
        print 'Trimming the image index for: ' + slug + '...'
        key = self.get_bucket().get_key(self._bucket_name + '/repositories/' + slug + '/_index_images')
        if key is not None:
            data = json.loads(key.get_contents_as_string(encoding='utf-8'))
            update = False
            for item in data:
                if item['id'] not in self.get_images_to_keep():
                    data.remove(item)
                    update = True
            if update:
                self._update_key(key, json.dumps(data))
            else:
                print '  nothing to trim'

    def _update_key(self, key, value):
        print '  updating key: ' + key.key + ' => ' + value
        if self._dry_run:
            print '  dry-run - not updated'
        else:
            key.set_contents_from_string(value)

    def _delete_key(self, key):
        print '  deleting key: ' + key.key
        if self._dry_run:
            print '  dry-run - not deleted'
        else:
            key.delete()
        return key.size

    def _delete_image(self, image_hash):
        print 'Deleting image: ' + image_hash + '...'
        keys = self.get_bucket().list(prefix=self._bucket_name + '/images/' + image_hash + '/')
        deleted_size = 0
        for key in keys:
            deleted_size += self._delete_key(key)
        return deleted_size

    def clean(self):
        # trim the orphaned images from _index_images
        for slug in self.get_index():
            self.trim_repo_index(slug)

        # delete all the orphaned images
        total_deleted_count = 0
        total_deleted_size = 0
        all_image_prefixes = self.get_bucket().list(prefix=self._bucket_name + '/images/', delimiter='/')
        for prefix in all_image_prefixes:
            image_hash = os.path.basename(os.path.dirname(prefix.name))
            if image_hash not in self.get_images_to_keep():
                size = self._delete_image(image_hash)
                total_deleted_count += 1
                total_deleted_size += size
                print '  deleted ' + str(size) + ' bytes'

        # print a summary
        print "\n\n  DELETED " + str(total_deleted_count) + ' IMAGES FREEING ' + str(total_deleted_size) + " BYTES\n\n"


if __name__ == '__main__':
    cleaner = Cleaner(
        access_key=os.environ.get('S3_ACCESS_KEY', ''),
        secret_key=os.environ.get('S3_SECRET_KEY', ''),
        host=os.environ.get('S3_HOST', 's3.amazonaws.com'),
        port=int(os.environ.get('S3_PORT', 443)),
        is_secure=str(os.environ.get('S3_IS_SECURE', "True")).lower() != 'false',
        bucket_name=os.environ.get('S3_BUCKET_NAME', 'registry'),
        dry_run=str(os.environ.get('DRY_RUN', "False")).lower() != 'false')

    cleaner.clean()