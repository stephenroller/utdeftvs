#!/usr/bin/env python2.7

import sys
from itertools import groupby

lines = (l.strip() for l in sys.stdin)
wordcounts = (l.split("\t") for l in lines if l)
parsed = ((w, float(i)) for w, i in wordcounts)
grouped = groupby(parsed, lambda x: x[0])
for k, g in grouped:
    s = sum(i for w, i in g)
    print "%s\t%f" % (k, s)


