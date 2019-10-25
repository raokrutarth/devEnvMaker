# Streaming Application

Use Kafka containers to create a cluster that allows a producer and consumer to use the cluster to share messages.

Docker compose setup: https://docs.confluent.io/5.0.0/installation/docker/docs/installation/clustered-deployment.html#docker-setup-3-node

## TODO

- use confluent-python-kafka APIs to setup multi broker producers and consumers.
- figure out api versions
- write script that randomly stops and starts kafka containers and tests impact on messages.
- write script that randomly stops and starts consumer containers.
- write a unit test for the consumer/producer.
- understand kafka & zookeeper comntainer flags.
- ??