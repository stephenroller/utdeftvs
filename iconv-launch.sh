
#!/bin/sh

hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-streaming-0.20.2-cdh3u2.jar \
    -D mapred.reduce.tasks=0 \
    -input $1 \
    -output "$1.utf8" \
    -mapper "iconv -flatin1 -tutf8"