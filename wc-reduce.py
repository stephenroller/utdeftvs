#!/usr/bin/env python2.7

import sys
from itertools import groupby

def tryparse(wordcounts):
    for item in wordcounts:
        if len(item) != 2:
            continue
        w, c = item
        try:
            yield (w, int(c))
        except ValueError:
            try:
                yield (w, float(c))
            except:
                continue

lines = (l.strip() for l in sys.stdin)
wordcounts = (l.split("\t") for l in lines if l)
parsed = tryparse(wordcounts)
grouped = groupby(parsed, lambda x: x[0])
for k, g in grouped:
    s = sum(i for w, i in g)
    if isinstance(s, int):
        print "%s\t%d" % (k, s)
    else:
        print "%s\t%f" % (k, s)


