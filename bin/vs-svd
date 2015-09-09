#!/usr/bin/env python
import sys
import argparse
import bz2
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as la

def load_targets(file):
    items = (w.strip().split("\t") for w in file if w.strip())
    vocab = np.array([k for k, v in items])
    lookup = {k : i for i, k in enumerate(vocab)}
    return vocab, lookup

def main():
    parser = argparse.ArgumentParser('Dimensionality reduces a space using the SVD')
    parser.add_argument('--input', '-i', default="-", help='Input file')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), help='Output file')
    parser.add_argument('--contextsoutput', '-x', type=argparse.FileType('w'),
                        help='Output file (contexts matrix)')
    parser.add_argument('-k', type=int, default=300, help='Target dimensionality')
    parser.add_argument('--rows', '-r', type=argparse.FileType('r'), help='Frequency file of rows.')
    parser.add_argument('--cols', '-c', type=argparse.FileType('r'), help='Frequency file of cols.')
    args = parser.parse_args()

    if args.input == "-":
        inpt = sys.stdin
    elif args.input.endswith('.bz2'):
        inpt = bz2.BZ2File(args.input)
    else:
        input = open(args.input)

    rvocab, rows = load_targets(args.rows)
    cvocab, cols = load_targets(args.cols)

    sys.stderr.write("Starting to read data matrix\n")
    data = []
    I = []
    J = []
    for line in inpt:
        line = line.strip()
        row, col, value = line.split()
        value = float(value)

        i, j = rows[row], cols[col]
        I.append(i)
        data.append(value)
        J.append(j)

    spmat = sp.coo_matrix((data, (I, J)), shape=(len(rows), len(cols))).tocsr()

    sys.stderr.write("Computing the SVD\n")
    u, s, vt = la.svds(spmat, k=args.k)
    s12 = np.sqrt(s)
    vectors = u.dot(np.diag(s12))

    sys.stderr.write("Saving output\n")
    np.savez_compressed(args.output, matrix=vectors, rows=rvocab)

    if args.contextsoutput:
        contexts = np.diag(s12).dot(vt).T
        np.savez_compressed(args.contextsoutput, matrix=contexts, rows=cvocab)



if __name__ == '__main__':
    main()
