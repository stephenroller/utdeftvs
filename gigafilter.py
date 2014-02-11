#!/usr/bin/env python2.7

import sys

for line in sys.stdin:
    line = line.strip()
    if line.startswith(sys.argv[1]):
        print line


