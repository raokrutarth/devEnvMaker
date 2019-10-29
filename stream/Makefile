
DIR := ${CURDIR}

build:
	@docker image build -f ./Dockerfile-python  -t producer .

run:
	@printf "Mounting %s as /app\n" ${DIR}
	@docker run --net=host -it --rm \
    	-e KAFKA_BROKERS=localhost:39092,localhost:29092,localhost:19092 \
    	--name=producerc \
    	--mount type=bind,source=${DIR},target=/app \
    	producer bash

test: build run

