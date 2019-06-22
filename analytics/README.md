# Analytics

Contains the big data application (compute + backend) and storage.

## Option 1

```shell
#!/bin/sh

docker build -t sparki:v2.4.0 .

# /spark/bin/spark-class org.apache.spark.deploy.master.Master --ip `hostname` --port 7077 --webui-port 8080

# elect current node as master and start it's webUI
/spark/bin/spark-class org.apache.spark.deploy.master.Master --ip $SPARK_LOCAL_IP --port $SPARK_MASTER_PORT --webui-port $SPARK_MASTER_WEBUI_PORT

# elect current node as worker and start it
/spark/bin/spark-class org.apache.spark.deploy.worker.Worker --webui-port 8080 spark://spark-master:7077

/spark/bin/spark-class org.apache.spark.deploy.worker.Worker --webui-port $SPARK_WORKER_WEBUI_PORT $SPARK_MASTER

# docker run to start master node
docker run --rm -it --name spark-master --hostname spark-master -p 7077:7077 -p 8080:8080 sparki

# submit a test spark job to the master node
/spark/bin/spark-submit --master spark://spark-master:7077 --class org.apache.spark.examples.SparkPi /spark/examples/jars/spark-examples_2.11-2.4.0.jar 1000

# run with 3 workers and 1 master
docker-compose up --scale spark-worker=3
```

## Option 2

docker-compose.yaml

```
version: "2.2"
services:
  master:
    image: cbspark
    build:
      context: .
      dockerfile: Dockerfile
    command: bin/spark-class org.apache.spark.deploy.master.Master -h master
    hostname: master
    environment:
      MASTER: spark://master:7077
      SPARK_CONF_DIR: /conf
      SPARK_PUBLIC_DNS: localhost
      PYSPARK_PYTHON: python3
    expose:
      - 7001
      - 7002
      - 7003
      - 7004
      - 7005
      - 7077
      - 6066
    ports:
      - 4040:4040
      - 6066:6066
      - 7077:7077
      - 8080:8080
    volumes:
      - ./conf/master:/conf
      - ./data/data:/data
      - ./data/code:/code

  worker:
    image: cbspark
    command: bin/spark-class org.apache.spark.deploy.worker.Worker spark://master:7077
    hostname: worker
    environment:
      SPARK_CONF_DIR: /conf
      SPARK_WORKER_CORES: 2
      SPARK_WORKER_MEMORY: 1g
      SPARK_WORKER_PORT: 8881
      SPARK_WORKER_WEBUI_PORT: 8081
      SPARK_PUBLIC_DNS: localhost
      PYSPARK_PYTHON: python3
    links:
      - master
    expose:
      - 7012
      - 7013
      - 7014
      - 7015
      - 8881
    ports:
      - 8081:8081
    volumes:
      - ./conf/worker:/conf
      - ./data/data:/data
- ./data/code:/code
```

Dockerfile

```
FROM debian:stretch
MAINTAINER Carbon Black "https://github.com/carbonblack/"

RUN apt-get update \
 && apt-get install -y locales fish man-db nano \
 && dpkg-reconfigure -f noninteractive locales \
 && locale-gen C.UTF-8 \
 && /usr/sbin/update-locale LANG=C.UTF-8 \
 && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
 && locale-gen \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*


# Users with other locales should set this in their derivative image
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN apt-get update \
 && apt-get install -y curl unzip git \
    python3 python3-setuptools \
 && easy_install3 pip py4j \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# PYTHON
RUN pip3 install pyspark jupyter

# http://blog.stuart.axelbrooke.com/python-3-on-spark-return-of-the-pythonhashseed
ENV PYTHONHASHSEED 0
ENV PYTHONIOENCODING UTF-8
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYSPARK_PYTHON python2.7
ENV PYSPARK3_PYTHON python3

# JAVA
ARG JAVA_MAJOR_VERSION=8
ARG JAVA_UPDATE_VERSION=202
ARG JAVA_BUILD_NUMBER=08
ENV JAVA_HOME /usr/jdk1.${JAVA_MAJOR_VERSION}.0_${JAVA_UPDATE_VERSION}

ENV PATH $PATH:$JAVA_HOME/bin
RUN curl -sL --retry 3 --insecure \
  --header "Cookie: oraclelicense=accept-securebackup-cookie;" \
  "http://download.oracle.com/otn-pub/java/jdk/${JAVA_MAJOR_VERSION}u${JAVA_UPDATE_VERSION}-b${JAVA_BUILD_NUMBER}/1961070e4c9b4e26a04e7f5a083f551e/server-jre-${JAVA_MAJOR_VERSION}u${JAVA_UPDATE_VERSION}-linux-x64.tar.gz" \
  | gunzip \
  | tar x -C /usr/ \
  && ln -s $JAVA_HOME /usr/java \
  && rm -rf $JAVA_HOME/man

# HADOOP
ENV HADOOP_VERSION 3.0.0
ENV HADOOP_HOME /usr/hadoop-$HADOOP_VERSION
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH $PATH:$HADOOP_HOME/bin
RUN curl -sL --retry 3 \
  "http://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz" \
  | gunzip \
  | tar -x -C /usr/ \
 && rm -rf $HADOOP_HOME/share/doc \
 && chown -R root:root $HADOOP_HOME

# SPARK
ENV SPARK_VERSION 2.4.0
ENV SPARK_PACKAGE spark-${SPARK_VERSION}-bin-without-hadoop
ENV SPARK_HOME /usr/spark-${SPARK_VERSION}
ENV SPARK_DIST_CLASSPATH="$HADOOP_HOME/etc/hadoop/*:$HADOOP_HOME/share/hadoop/common/lib/*:$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/hdfs/lib/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/yarn/lib/*:$HADOOP_HOME/share/hadoop/yarn/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/tools/lib/*"
ENV PATH $PATH:${SPARK_HOME}/bin
RUN curl -sL --retry 3 \
  "https://www.apache.org/dyn/mirrors/mirrors.cgi?action=download&filename=spark/spark-${SPARK_VERSION}/${SPARK_PACKAGE}.tgz" \
  | gunzip \
  | tar x -C /usr/ \
 && mv /usr/$SPARK_PACKAGE $SPARK_HOME \
 && chown -R root:root $SPARK_HOME
RUN chsh -s /usr/bin/fish



 ## install ripgrep
 RUN curl -s --retry 3 -LO https://github.com/BurntSushi/ripgrep/releases/download/0.10.0/ripgrep_0.10.0_amd64.deb \
 && dpkg -i ripgrep_0.10.0_amd64.deb

WORKDIR $SPARK_HOME
CMD ["bin/spark-class", "org.apache.spark.deploy.master.Master"]
```

- list of similar projects: <https://github.com/search?q=docker-spark>
- kafka + spark + docker: <https://blog.antlypls.com/blog/2015/10/05/getting-started-with-spark-streaming-using-docker/>
- full big data demo app and code: <https://github.com/big-data-europe/demo-spark-sensor-data>
- <https://github.com/big-data-europe/docker-spark>
- <https://towardsdatascience.com/a-journey-into-big-data-with-apache-spark-part-1-5dfcc2bccdd2>
- <https://www.youtube.com/watch?v=Qei5VAnCpDM>
- <https://www.youtube.com/watch?v=z_D5L9h6B6c>
- <https://github.com/gettyimages/docker-spark>
- <https://github.com/carbonblack/docker-spark>
- <https://www.smaato.com/blog/spark-docker-amazon-ec2-code-tells-you-everything/>