#!/usr/bin/env python

import sys

stopwords = set(l.strip() for l in open("/scratch/01813/roller/corpora/en_stopwords.txt"))


for line in sys.stdin:
    line = line.rstrip()
    fields = line.split("\t")
    ngram = fields[0].split(" ")
    if all(n in stopwords for n in ngram):
        continue
    print line


