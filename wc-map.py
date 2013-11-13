#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip().split(" ")
    for w in line:
        print "%s\t1" % w

