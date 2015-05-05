FROM gliderlabs/alpine:3.1
MAINTAINER Chris Roemmich <croemmich@myriadmobile.com>

ENV S3_ACCESS_KEY="" \
	S3_SECRET_KEY="" \
	S3_HOST="s3.amazonaws.com" \
	S3_PORT="443" \
	S3_IS_SECURE="True" \
	S3_BUCKET_NAME="" \
	DRY_RUN="False"

RUN apk-install python py-pip openssl ca-certificates && \
  	pip install virtualenv && \
  	virtualenv /env

COPY app /app
WORKDIR /app

RUN /env/bin/pip install -r /app/requirements.txt

CMD ["/env/bin/python", "./clean.py"]