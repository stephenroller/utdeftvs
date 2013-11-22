#!/bin/sh

export A="$2"
export F=""
if [[ $2 != "" ]]
then
    export F=".$A"
    export A=" --$A"
fi

hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-0.20.2-cdh3u2.jar \
    -D mapred.reduce.tasks=32 \
    -input $1 \
    -output "$1$F.wordcount" \
    -mapper "wc-map.py$A" \
    -reducer wc-reduce.py \
    -file wc-map.py \
    -file util.py \
    -file wc-reduce.py

    #-D stream.num.map.output.key.fields=2 \
    #-D mapred.text.key.partitioner.options=-k1 \
    #-combiner wc-reduce.py \
