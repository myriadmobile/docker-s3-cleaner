# CoreOS

## Installation

1. Open a shell to your CoreOS cluster
2. `git clone https://github.com/myriadmobile/docker-s3-cleaner`
3. `cd docker-s3-cleaner/contrib/coreos`
3. Open `docker-s3-cleaner.service` in your favorite text editor
4. Edit at minimum `S3_ACCESS_KEY`, `S3_SECRET_KEY`, and `S3_BUCKET_NAME`
5. `fleetctl submit docker-s3-cleaner.service`
6. `fleetctl start docker-s3-cleaner.service`

## Configuration

Additional [configuration](../../README.md#configuration) can be supplied to Docker with a `-e` flag. e.g. `-e KEY=VALUE -e ANOTHER_KEY=VALUE`