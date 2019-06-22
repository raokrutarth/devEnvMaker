#!/bin/bash

# on-container script

# start the spark instance with the current node/container as the master
/spark/bin/spark-class \
    org.apache.spark.deploy.master.Master \
    --ip $SPARK_LOCAL_IP \
    --port $SPARK_MASTER_PORT \
    --webui-port $SPARK_MASTER_WEBUI_PORT


