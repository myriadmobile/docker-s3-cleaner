REPO = myriadmobile
NAME = docker-s3-cleaner
VERSION = v1.0.1

build: build-app

push: push-app

release: build push

build-app:
		docker build --rm --pull -t $(REPO)/$(NAME) .
		docker tag -f $(REPO)/$(NAME) $(REPO)/$(NAME):$(VERSION)

push-app:
		docker push $(REPO)/$(NAME):$(VERSION)
		docker push $(REPO)/$(NAME):latest