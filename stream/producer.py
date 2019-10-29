from time import sleep
from confluent_kafka import Producer
from os.path import abspath
import os
from uuid import uuid4
import sys

import pandas as pd
from random import choice

from pprint import pprint

import logging
from logging import debug as logDebug

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def fetch_dataset():
    source_file = abspath('./data/preprocessed_data.csv')
    return pd.read_csv(source_file)

def get_random_row(dataset_df: pd.DataFrame) -> pd.DataFrame:
    return dataset_df.sample(n=1)


# acked is called when the message is delivered
def acked(err, msg):
    if err is not None:
        logDebug("Failed to deliver message: {0}: {1}".format(msg.value(), err.str()))
    else:
        logDebug("Message produced and delivered: {0}".format(msg.value()))


def main():
    env_var_key = "KAFKA_BROKERS"
    kafka_brokers = os.environ[env_var_key]
    producer = Producer({'bootstrap.servers': kafka_brokers})

    topic = "UFC"
    dataset = fetch_dataset()

    keys = ["my_key"+ str(uuid4()) for _ in range(5)]

    while True:
        row = get_random_row(dataset)
        row_json = row.to_json()
        key = choice(keys)
        producer.produce(topic, key=key, value=row_json.encode(), callback=acked)


if __name__ == '__main__':
    main()