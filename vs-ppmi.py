#!/usr/bin/env python
import sys
import argparse

from numpy import log2

def load_targets(file):
    items = (w.strip().split("\t") for w in file if w.strip())
    return {k : int(v) for k, v in items}

def main():
    parser = argparse.ArgumentParser('Transforms a space by PPMI')
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file')
    parser.add_argument('--rows', '-r', type=argparse.FileType('r'), help='Frequency file of rows.')
    parser.add_argument('--cols', '-c', type=argparse.FileType('r'), help='Frequency file of cols.')

    args = parser.parse_args()
    rows = load_targets(args.rows)
    cols = load_targets(args.cols)

    total = sum(rows.itervalues())
    assert total == sum(cols.itervalues())
    log2total = log2(total)

    for line in args.input:
        line = line.strip()
        row, col, value = line.split()
        value = int(value)

        if value * total < rows[row] * cols[col]:
            # pmi less than 0, skip this line
            continue

        # pmi = log2 [ p(r,c) / [ p(r) * p(c) ]
        #     = log2 ( #(r,c) / #(*,*) ) - log2 [ #(r,*)/#(*,*) ] - log2 [ #(*,c)/#(*,*) ]
        #     = log2 #(r,c) - log2 #(*,*) - log2 #(r,*) + log2 #(*,*) - log2 #(*,c) + log2 #(*,*)
        #     = log2 #(r,c) - log2 #(r,*) - log2 #(*,c) + log2 #(*,*)

        pmi = log2(value) - log2(rows[row]) - log2(cols[col]) + log2total
        assert pmi > 0.0

        print "%s\t%s\t%f" % (row, col, pmi)





if __name__ == '__main__':
    main()
