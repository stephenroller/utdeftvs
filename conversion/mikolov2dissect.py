#!/usr/bin/env python2.7

import argparse
import struct
import pickle
import numpy as np
from composes.semantic_space.space import Space
from composes.matrix.dense_matrix import DenseMatrix

FLOAT_SIZE = 4

def read_mikolov(spacefile):
    header = spacefile.readline().rstrip()
    vocab_s, dims = map(int, header.split(" "))

    vocab = []

    # init matrix
    matrix = np.zeros((vocab_s, dims), dtype=np.float)

    i = 0
    while True:
        line = spacefile.readline()
        if not line:
            break
        sep = line.find(" ")
        if sep == -1:
            raise ValueError("Couldn't find the vocab/data separation character! Space file corruption?")

        word = line[:sep]
        data = line[sep+1:]
        if len(data) < FLOAT_SIZE * dims + 1:
            data += spacefile.read(FLOAT_SIZE * dims + 1 - len(data))
        data = data[:-1]
        vocab.append(word)
        vector = (struct.unpack("%df" % dims, data))
        matrix[i] = vector
        i += 1

    dm = DenseMatrix(matrix)
    sp = Space(dm, vocab, [])

    return sp

def main():
    parser = argparse.ArgumentParser(
                description="Converts a Mikolov binary vector file into one compatible with Trento's COMPOSES.")
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), help='Input file')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), help='Output file')
    args = parser.parse_args()

    sp = read_mikolov(args.input)

    pickle.dump(sp, args.output)
    args.output.close()

if __name__ == '__main__':
    main()

