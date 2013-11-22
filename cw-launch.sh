#!/bin/sh

hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-0.20.2-cdh3u2.jar \
    -D mapred.reduce.tasks=0 \
    -input $1 \
    -output "$1.content" \
    -mapper contentwords.py \
    -file util.py \
    -file contentwords.py
