#!/usr/bin/env python
import sys
import argparse
import pickle

def main():
    parser = argparse.ArgumentParser('Converts a Sparse Matrix format (.sm) into form needed for VW.')
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file')
    parser.add_argument('--docnames', '-d', type=argparse.FileType('w'), default=None, help='Output docnames to this file.')
    args = parser.parse_args()

    space = pickle.load(args.input)
    matrix = space.get_cooccurrence_matrix().mat

    colnames = [c.replace(":", "__") for c in space.id2column]

    for i, row in enumerate(space.id2row):
        vector = matrix[i].A[0]
        nz = vector.nonzero()[0]
        outs = "| " + " ".join("%s:%d" % (colnames[j], vector[j]) for j in nz)
        args.output.write(outs + "\n")
        args.docnames.write(row + "\n")

if __name__ == '__main__':
    main()
