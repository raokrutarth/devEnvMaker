


all: build jyp

build:
	@docker build -t scratch:tensorflow .

# run as non-root in container to avoid file permission issues
jyp:
	@docker run -it --rm \
		-u $(id -u):$(id -g) \
		-v $(realpath ./src):/src \
		-v $(realpath ./data):/data \
		-p 8888:8888 \
		--name tensorflowc \
		scratch:tensorflow \
		/bin/bash

gpu:
	@docker run -it --rm --runtime=nvidia tensorflow/tensorflow:latest-gpu-py3 /bin/bash