#!/bin/sh

hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-0.20.2-cdh3u2.jar \
    -D mapred.reduce.tasks=32 \
    -D stream.num.map.output.key.fields=2 \
    -D mapred.text.key.partitioner.options=-k1 \
    -input $1 \
    -output "$1.adjnoun.window2.coocc" \
    -mapper "vs-map.py --adjnoun" \
    -reducer vs-reduce.py \
    -file vs-map.py \
    -file vs-reduce.py \
    -file util.py \
    -file contexts.txt

