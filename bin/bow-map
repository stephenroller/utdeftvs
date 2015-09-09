#!/usr/bin/env python
import sys
import argparse

def clamp(value, min, max):
    if value < min:
        return min
    if value > max:
        return max
    return value

def main():
    parser = argparse.ArgumentParser('Extracts target/context tuples within a BOW window.')
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file')
    parser.add_argument('--windowsize', '-w', type=int, default=2, help='Window size.')
    args = parser.parse_args()

    window = args.windowsize

    for line in args.input:
        line = line.strip()
        words = line.split()
        maxj = len(words) - 1
        for i, target in enumerate(words):
            leftj = clamp(i - window, 0, maxj)
            rightj = clamp(i + window, 0, maxj)
            for j in xrange(leftj, rightj+1):
                if i != j:
                    wordj = words[j]
                    args.output.write("%s\t%s\t1\n" % (target, wordj))

if __name__ == '__main__':
    main()
