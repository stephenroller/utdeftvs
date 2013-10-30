#!/usr/bin/env python
import sys
from collections import Counter

c = Counter()

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    c.update(line.strip().split("\t")[1].split(" "))

for x, v in c.most_common(10000):
    print "%10d    %s" % (v, x)
