#!/bin/bash

# on-container script

# run the current node as a worker node
/spark/bin/spark-class \
    org.apache.spark.deploy.worker.Worker \
    --webui-port $SPARK_WORKER_WEBUI_PORT \
    $SPARK_MASTER