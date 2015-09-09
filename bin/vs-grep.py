#!/usr/bin/env python

import sys
import argparse


def load_targets(file):
    return set(w.strip().split("\t")[0] for w in file if w.strip())

def main():
    parser = argparse.ArgumentParser(
                description='Filters a column to have only the terms')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input vector space', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--column', '-c', type=int, default=1, help='Column to filter, one-indexed.')
    parser.add_argument('--whitelist', '-w', metavar='FILE', type=argparse.FileType('r'), help='File of items to keep (only first column read)')
    parser.add_argument('--invert', '-I', action='store_true', help='Filter contexts NOT in the contexts list.')
    args = parser.parse_args()

    whitelist = load_targets(args.whitelist)

    for line in args.input:
        line = line.strip()
        fields = line.split("\t")
        t = fields[args.column-1]
        cond = t in whitelist
        if args.invert:
            cond = not cond

        if cond:
            print line

if __name__ == '__main__':
    main()

