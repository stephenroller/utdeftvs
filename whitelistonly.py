#!/usr/bin/env python2.7
import sys
import argparse
import logging

class contains_always():
    def __init__(self, value):
        self.value = value
    def __contains__(self, x):
        return self.value

def main():
    parser = argparse.ArgumentParser(
                description='Keeps only words from a given list.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input file', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--whitelist', '-w', metavar='FILE', help='Whitelist file')
    parser.add_argument('--blacklist', '-b', metavar='FILE', help='Blacklist file')
    args = parser.parse_args()
    inpt = args.input

    if args.whitelist:
        whitelist = set(l.strip().split("\t")[0] for l in open(args.whitelist))
    else:
        whitelist = contains_always(True)
    if args.blacklist:
        blacklist = set(l.strip().split("\t")[0] for l in open(args.blacklist))
    else:
        blacklist = contains_always(False)

    for sentence in inpt:
        tokens = sentence.strip().split(" ")
        sentence = [w for w in tokens if w in whitelist and w not in blacklist]
        if len(sentence) >= 2:
            print " ".join(sentence)

if __name__ == '__main__':
    main()

