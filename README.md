# Docker S3 Cleaner

Docker S3 cleaner removes orphaned image layers from S3 backed private docker registries.

## Features
- removes orphaned images (images not part of a tagged image's ancestry)
- properly maintains repository index meta to keep the registry in a valid state
- highly configurable
- works with any s3 compatible stores

## Warning

Removing images from private registries is not officially supported by Docker and a variety of things can go wrong. Use at your own risk!

## Basic Usage

```bash
docker run -it myriadmobile/docker-s3-cleaner:v1.0.1 \
	-e S3_ACCESS_KEY=replace_me \
	-e S3_SECRET_KEY=replace_me \
	-e S3_BUCKET_NAME=my_registry
```

## Configuration
- `S3_ACCESS_KEY` - Your S3 access key.
- `S3_SECRET_KEY` - Your S3 secret key.
- `S3_HOST` - S3 compatible server host. default: `s3.amazonaws.com`
- `S3_PORT` - S3 compatible server port. default: `443`
- `S3_IS_SECURE` - Use SSL connection? default: `True`
- `S3_BUCKET_NAME` - Name of the bucket containing your registry data.
- `DRY_RUN` - When `True` all file operations are logged but not performed. default: `False`

## Removing Tags

The Docker S3 Cleaner will only remove layers that are no longer a part of a tagged hierarchy.

### View Tags
`curl -X GET http://REGISTRY_HOST:PORT/v1/repositories/NAMESPACE/REPO/tags`

### Delete Tag
`curl -X DELETE http://REGISTRY_HOST:PORT/v1/repositories/NAMESPACE/REPO/tags/TAG_NAME`

Note: For private repositories `NAMESPACE` is normally `library`

## Contrib

- [CoreOS](contrib/coreos)
- [Deis](contrib/deis)