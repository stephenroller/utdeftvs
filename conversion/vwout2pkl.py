#!/usr/bin/env python
import sys
import argparse
import pickle
import numpy as np
from composes.semantic_space.space import Space
from composes.matrix.dense_matrix import DenseMatrix

def main():
    parser = argparse.ArgumentParser('Converts a VW topic output to a COMPOSES pkl file.')
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), help='Input file')
    parser.add_argument('--docnames', '-d', type=argparse.FileType('r'), help='Docnames file')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file')

    args = parser.parse_args()
    docnames = [l for l in (l.strip() for l in args.docnames) if l]
    matrix = None
    for i, line in enumerate(args.input):
        line = line.strip()
        weights = map(float, line.split(" "))
        if matrix is None:
            matrix = np.zeros((len(docnames), len(weights)), dtype=np.float)
        weights = np.array(weights)
        matrix[i] = weights

    dm = DenseMatrix(matrix)
    sp = Space(dm, docnames, [])
    pickle.dump(sp, args.output)
    args.output.close()


if __name__ == '__main__':
    main()
