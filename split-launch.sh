#!/bin/sh

hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-0.20.2-cdh3u2.jar \
    -D mapred.reduce.tasks=0 \
    -input $1 \
    -output "$1.split1" \
    -mapper 'split-map.py' \
    -file split-map.py

hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-0.20.2-cdh3u2.jar \
    -D mapred.reduce.tasks=0 \
    -input "$1.split1" \
    -output "$1.split2.test" \
    -mapper 'gigafilter.py test' \
    -file gigafilter.py

hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-0.20.2-cdh3u2.jar \
    -D mapred.reduce.tasks=0 \
    -input "$1.split2.test" \
    -output "$1.split.test" \
    -mapper 'cut -f2-'

hadoop fs -rmr "$1.split2.test"

hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-0.20.2-cdh3u2.jar \
    -D mapred.reduce.tasks=0 \
    -input "$1.split1" \
    -output "$1.split2.train" \
    -mapper 'gigafilter.py train' \
    -file gigafilter.py

hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-0.20.2-cdh3u2.jar \
    -D mapred.reduce.tasks=0 \
    -input "$1.split2.train" \
    -output "$1.split.train" \
    -mapper 'cut -f2-'

hadoop fs -rmr "$1.split2.test"
hadoop fs -rmr "$1.split1"

