#!/usr/bin/env python

import sys
from itertools import groupby

lines = (line.rstrip().split("\t") for line in sys.stdin if line.rstrip())
parsed = ((t, c, int(v)) for t, c, v in lines)
samekey = groupby(parsed, key=lambda x: (x[0], x[1]))
for (t, c), g in samekey:
    vs = sum(v for t, c, v in g)
    print "%s\t%s\t%d" % (t, c, vs)


