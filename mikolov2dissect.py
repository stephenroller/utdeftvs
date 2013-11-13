#!/usr/bin/env python

import argparse
import struct
import pickle
import numpy as np
from composes.semantic_space.space import Space
from composes.matrix.dense_matrix import DenseMatrix

FLOAT_SIZE = 4

def main():
    parser = argparse.ArgumentParser(
                description="Converts a Mikolov binary vector file into one compatible with Trento's COMPOSES.")
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), help='Input file')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), help='Output file')
    args = parser.parse_args()

    header = args.input.readline().rstrip()
    vocab_s, dims = map(int, header.split(" "))

    vocab = []

    # init matrix
    matrix = np.zeros((vocab_s, dims), dtype=np.float)

    i = 0
    while True:
        line = args.input.readline()
        if not line:
            break
        sep = line.find(" ")
        if sep == -1:
            print "data so far: '%s'" % line[:100]
            import pdb
            pdb.set_trace()
            #sep = MAX_WORD_LEN

        word = line[:sep]
        data = line[sep+1:]
        if len(data) < FLOAT_SIZE * dims + 1:
            data += args.input.read(FLOAT_SIZE * dims + 1 - len(data))
        data = data[:-1]
        vocab.append(word)
        vector = (struct.unpack("%df" % dims, data))
        matrix[i] = vector
        i += 1

    dm = DenseMatrix(matrix)
    sp = Space(dm, vocab, [])
    pickle.dump(sp, args.output)
    args.output.close()





if __name__ == '__main__':
    main()

