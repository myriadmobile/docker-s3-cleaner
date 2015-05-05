# Deis

## Installation

1. Open a shell to your Deis cluster
2. `git clone https://github.com/myriadmobile/docker-s3-cleaner`
3. `cd docker-s3-cleaner/contrib/deis`
5. `fleetctl submit docker-s3-cleaner.service`
6. `fleetctl start docker-s3-cleaner.service`

## Configuration

Additional [configuration](../../README.md#configuration) can be supplied to Docker with a `-e` flag. e.g. `-e KEY=VALUE -e ANOTHER_KEY=VALUE`