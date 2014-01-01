#!/usr/bin/env python

import sys
import argparse


def load_targets(file):
    return set(w.strip().split("\t")[0] for w in file if w.strip())

def main():
    parser = argparse.ArgumentParser(
                description='Filters a vector space to only be concerned targets.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input vector space', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--targets', '-t', metavar='FILE', type=argparse.FileType('r'), help='File of targets (or targets w/ counts)')
    parser.add_argument('--compoundsearch', '-c', metavar='FILE', type=argparse.FileType('r'), help='File of compounds to search for.')
    parser.add_argument('--contexts', '-x', metavar='FILE', type=argparse.FileType('r'), help='File of contexts (or contexts w/ counts)')
    args = parser.parse_args()

    targets = None
    contexts = None
    if args.targets:
        targets = load_targets(args.targets)
        exact_match = True
    elif args.compoundsearch:
        targets = load_targets(args.compoundsearch)
        exact_match = False

    if args.contexts:
        contexts = load_targets(args.contexts)

    for line in args.input:
        line = line.rstrip()
        target_match = False
        context_match = False

        fields = line.split("\t")
        t = fields[0]
        c = fields[1]

        if targets:
            if exact_match and t in targets:
                target_match = True
            elif not exact_match:
                searchterm = line.split("__")[0]
                if searchterm in targets:
                    target_match = True
        else:
            target_match = True

        if contexts:
            if c in contexts:
                context_match = True
        else:
            context_match = True

        if target_match and context_match:
            print line


if __name__ == '__main__':
    main()

