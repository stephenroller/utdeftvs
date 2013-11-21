#!/usr/bin/env python2.7
import sys
import argparse
import logging

def main():
    parser = argparse.ArgumentParser(
                description='Keeps only words from a given list.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input file', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--whitelist', '-w', metavar='FILE', type=argparse.FileType('r'), help='Whitelist file')
    args = parser.parse_args()
    inpt = args.input
    whitelist = set(l.strip().split("\t")[0] for l in args.whitelist)

    for sentence in inpt:
        sentence = [w for w in sentence.strip().split(" ") if w in whitelist]
        if len(sentence) >= 2:
            print " ".join(sentence)

if __name__ == '__main__':
    main()

