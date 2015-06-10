#!/usr/bin/env python2.7

import argparse
import struct
import pickle
import numpy as np
from composes.semantic_space.space import Space
from composes.matrix.dense_matrix import DenseMatrix

def main():
    parser = argparse.ArgumentParser(
                description="Converts a vecf file to dissect pkl format.")
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), help='Input file')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), help='Output file')
    args = parser.parse_args()

    header = args.input.readline().rstrip()
    vocab_s, dims = map(int, header.split(" "))

    vocab = []

    # init matrix
    matrix = np.zeros((vocab_s, dims), dtype=np.float)

    for i, line in enumerate(args.input):
        data = line.split()
        vector = np.array(map(float, data[1:]))
        word = data[0]
        vocab.append(word)
        matrix[i] = vector

    dm = DenseMatrix(matrix)
    sp = Space(dm, vocab, [])
    pickle.dump(sp, args.output)
    args.output.close()



if __name__ == '__main__':
    main()

