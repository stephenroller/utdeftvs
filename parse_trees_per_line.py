#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.rstrip("\n")
    if line.startswith("<text"):
        print line
        buf = []
    elif line == "</text>":
        print line
    elif line == "<s>":
        buf = []
    elif line == "</s>":
        print "\t".join(buf)
    else:
        buf.append(line)




