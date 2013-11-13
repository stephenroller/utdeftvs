#!/usr/bin/env python
import sys
import argparse
import logging

def main():
    parser = argparse.ArgumentParser(
                description='Keeps only words from a given list.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input file')
    parser.add_argument('--whitelist', '-w', type=argparse.FileType('r'), help='Input file')
    args = parser.parse_args()
    inpt = args.input
    whitelist = set(l.strip() for l in args.whitelist)

    for sentence in inpt:
        sentence = [w for w in sentence.strip().split(" ") if w in whitelist]
        if len(sentence) >= 2:
            print " ".join(sentence)

if __name__ == '__main__':
    main()

