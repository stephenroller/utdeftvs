#!/bin/sh

hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-0.20.2-cdh3u2.jar \
    -D mapred.reduce.tasks=56 \
    -input $1 \
    -output "$1.wordcount" \
    -mapper wc-map.py \
    -reducer wc-reduce.py \
    -file wc-map.py \
    -file wc-reduce.py

    #-D stream.num.map.output.key.fields=2 \
    #-D mapred.text.key.partitioner.options=-k1 \
    #-combiner wc-reduce.py \
