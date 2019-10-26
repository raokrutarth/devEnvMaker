#!/usr/bin/env python


from confluent_kafka.admin import \
    AdminClient, \
    NewTopic, \
    NewPartitions, \
    ConfigResource, \
    ConfigSource

from confluent_kafka import KafkaException


import sys, os
import threading
import logging

logging.basicConfig()

'''
    Adopted from https://github.com/confluentinc/confluent-kafka-python/tree/master/examples
'''


def create_topics(admin_client, topics, num_partitions=3, replication_factor=2):
    """
        Create topics
    """
    new_topics = [
        NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor) \
        for topic in topics
    ]


    # Call create_topics to asynchronously?? create topics, a dict
    # of <topic,future> is returned.
    topic_futures = admin_client.create_topics(new_topics, request_timeout=15.0)

    # Wait for operation to finish.
    # All futures will finish at the same time.
    for topic, future in topic_futures.items():
        try:
            # The return from result is None
            future.result()
            logging.debug("Topic {} created".format(topic))
        except Exception as e:
            logging.debug("Failed to create topic {}: {}".format(topic, e))


def delete_topics(admin_client, topics):
    """
        delete topics
    """

    # Call delete_topics to asynchronously delete topics, a future is returned.
    # By default this operation on the broker returns immediately while
    # topics are deleted in the background. But here, give it some time (30s)
    # to propagate in the cluster before returning.
    #
    # Returns a dict of <topic,future>.
    topic_futures = admin_client.delete_topics(topics, operation_timeout=30)

    # Wait for operation to finish.
    for topic, future in topic_futures.items():
        try:
            future.result()  # The result itself is None
            logging.debug("Topic {} deleted".format(topic))
        except Exception as e:
            logging.debug("Failed to delete topic {}: {}".format(topic, e))



def print_config(config, depth):
    logging.debug(
        '%40s = %-50s  [%s,is:read-only=%r,default=%r,sensitive=%r,synonym=%r,synonyms=%s]' %
        ((' ' * depth) + config.name, config.value, ConfigSource(config.source),
           config.is_read_only, config.is_default,
           config.is_sensitive, config.is_synonym,
           ["%s:%s" % (x.name, ConfigSource(x.source))
            for x in iter(config.synonyms.values())]))




def list_topics_and_cluster(admin_client, list_brokers=True, list_topics=True):
    """
        list topics and cluster metadata
    """
    metadata = admin_client.list_topics(timeout=10)

    logging.debug("Cluster {} metadata (response from broker {}):".format(metadata.cluster_id, metadata.orig_broker_name))

    if list_brokers:
        logging.debug(" %d brokers:" % len(metadata.brokers))
        for broker in iter(metadata.brokers.values()):
            if broker.id == metadata.controller_id:
                logging.debug("  {}  (controller)".format(broker))
            else:
                logging.debug("  {}".format(broker))


    logging.debug(" {} topics:".format(len(md.topics)))
    for t in iter(md.topics.values()):
        if t.error is not None:
            errstr = ": {}".format(t.error)
        else:
            errstr = ""

        logging.debug("  \"{}\" with {} partition(s){}".format(t, len(t.partitions), errstr))

        for p in iter(t.partitions.values()):
            if p.error is not None:
                errstr = ": {}".format(p.error)
            else:
                errstr = ""

            logging.debug("    partition {} leader: {}, replicas: {}, isrs: {}".format(
                p.id, p.leader, p.replicas, p.isrs, errstr))


if __name__ == '__main__':

    brokers = os.environ["KAFKA_BROKERS"]

    # Create Admin client
    admin_client = AdminClient({'bootstrap.servers': brokers})
