

build:
	@docker image build -f ./Dockerfile-python  -t producer .
run:
	@docker run --net=host -it --rm \
    	-e KAFKA_BROKERS=localhost:39092,localhost:29092,localhost:19092 \
    	--name=producerc \
    	-v $(pwd):/app \
    	producer bash

test: build run

