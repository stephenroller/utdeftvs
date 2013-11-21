#!/usr/bin/env python2.7

import sys
import random
import argparse

def main():
    parser = argparse.ArgumentParser(
                description='Splits a file into a train/test bits.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input vector space', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--prob', '-p', metavar='PROB', type=float, help='Probability of being in test.', default=0.5)
    args = parser.parse_args()

    inpt = args.input
    p = args.prob

    for line in inpt:
        line = line.rstrip()
        r = random.random()
        if r < p:
            split = "test"
        else:
            split = "train"
        print "%s\t%s" % (split, line)

if __name__ == '__main__':
    main()


