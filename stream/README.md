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


## Resources

- https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/consumer.py
- https://docs.confluent.io/current/clients/confluent-kafka-python/#module-confluent_kafka.admin
- config parameters: https://kafka.apache.org/08/documentation.html
- Python API intro: https://www.confluent.io/blog/introduction-to-apache-kafka-for-python-programmers/
- Docker setup intro: https://docs.confluent.io/5.0.0/installation/docker/docs/installation/clustered-deployment.html#docker-setup-3-node
- Testing kafka: https://dzone.com/articles/a-quick-and-practical-example-of-kafka-testing
- High level stream API descriptions: https://dzone.com/articles/real-time-stream-processing-with-apache-kafkapart-1
- Kafka stream workflow overview: https://dzone.com/articles/real-time-stream-processing-with-apache-kafkapart
- Kafka realtime best practices: https://dzone.com/articles/using-apache-kafka-for-real-time-event-processing
- Kafka listners, details and resources: https://rmoff.net/2018/08/02/kafka-listeners-explained/
-
