#!/usr/bin/env python

import sys
import argparse


def load_targets(file):
    return set(w.strip().split("\t")[0] for w in file if w.strip())

def main():
    parser = argparse.ArgumentParser(
                description='Filters a vector space to only be concerned targets.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input vector space', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--targets', '-t', metavar='FILE', type=argparse.FileType('r'), help='File of targets (or counts w/ counts)')
    parser.add_argument('--compoundsearch', '-c', metavar='FILE', type=argparse.FileType('r'), help='File of compounds to search for.')
    args = parser.parse_args()

    if args.targets:
        targets = load_targets(args.targets)
        exact_match = True
    elif args.compoundsearch:
        targets = load_targets(args.compoundsearch)
        exact_match = False

    for line in args.input:
        line = line.rstrip()
        t = line.split("\t")[0]
        if exact_match and t in targets:
            print line
        elif not exact_match:
            searchterm = line.split("__")[0]
            if searchterm in targets:
                print line

if __name__ == '__main__':
    main()

