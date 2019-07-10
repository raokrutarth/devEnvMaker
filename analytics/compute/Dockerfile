FROM openjdk:8-alpine

RUN apk --update add wget tar bash

RUN wget http://mirrors.ocf.berkeley.edu/apache/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz

RUN tar -xzf spark-2.4.3-bin-hadoop2.7.tgz && \
    mv spark-2.4.3-bin-hadoop2.7 /spark && \
    rm spark-2.4.3-bin-hadoop2.7.tgz

COPY run-as-worker.sh /run-as-worker.sh
RUN chmod +x /run-as-worker.sh

COPY run-as-master.sh /run-as-master.sh
RUN chmod +x /run-as-master.sh


