#!/usr/bin/env python


from confluent_kafka.admin import \
    AdminClient, \
    NewTopic, \
    NewPartitions, \
    ConfigResource, \
    ConfigSource

from confluent_kafka import KafkaException

from typing import List
import sys, os
import threading


import logging
from logging import debug as logDebug
from logging import error as logError

from time import sleep

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

'''
    Adopted from https://github.com/confluentinc/confluent-kafka-python/tree/master/examples
'''


def create_topics(admin_client, topics, num_partitions=3, replication_factor=2):
    """
        Create topics
    """
    logDebug("Attempting to create topics: %s", topics)

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
            logDebug("Topic {} created".format(topic))
        except Exception as e:
            logError("Failed to create topic {}: {}".format(topic, e))


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
            logDebug("Topic {} deleted".format(topic))
        except Exception as e:
            logError("Failed to delete topic {}: {}".format(topic, e))




def print_topics_and_cluster(admin_client, list_brokers=True, list_topics=True):
    """
        log topics and cluster metadata
    """
    metadata = admin_client.list_topics(timeout=10)

    logDebug("Cluster {} metadata (response from broker {}):".format(metadata.cluster_id, metadata.orig_broker_name))

    if list_brokers:
        logDebug(" %d brokers:", len(metadata.brokers))
        for broker in iter(metadata.brokers.values()):
            if broker.id == metadata.controller_id:
                logDebug("  {}  (controller)".format(broker))
            else:
                logDebug("  {}".format(broker))

    if list_topics:
        logDebug(" %d topics:", len(metadata.topics))
        for t in iter(metadata.topics.values()):
            if t.error is not None:
                errstr = ": {}".format(t.error)
            else:
                errstr = ""

            logDebug("\t\"{}\" with {} partition(s){}".format(t, len(t.partitions), errstr))

            for p in iter(t.partitions.values()):
                if p.error is not None:
                    errstr = ": {}".format(p.error)
                else:
                    errstr = ""

                logDebug("\t\tpartition {} leader: {}, replicas: {}, isrs: {}, error: {}".format(
                    p.id, p.leader, p.replicas, p.isrs, errstr))

def get_topics(admin_client) -> List[str]:
    metadata = admin_client.list_topics(timeout=10)
    topics = []

    for topic_metadata in iter(metadata.topics.values()):
        topics.append(topic_metadata.topic)

    return topics



def main():
    brokers = os.environ["KAFKA_BROKERS"]

    logDebug("Got broker addresses: %s", brokers)

    needed_topics = ["my_test_stream"]

    # Create Admin client
    # https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    admin_client = AdminClient(
        {
            'bootstrap.servers': brokers,
            "api.version.request": True,
        }
    )

    existing_topics = get_topics(admin_client)
    to_create = []

    for topic in needed_topics:
        if topic not in existing_topics:
            logDebug(topic + " not in existing topics")
            to_create.append(topic)

    if to_create:
        create_topics(admin_client, to_create)

    print_topics_and_cluster(admin_client)
    sleep(3)
    new_topics = get_topics(admin_client)

    logDebug("topics after init: {}".format(new_topics))


if __name__ == '__main__':
    main()
