#!/usr/bin/env python
import sys
import argparse
import scipy.sparse as sp
import scipy.sparse.linalg as la

def load_targets(file):
    items = (w.strip().split("\t") for w in file if w.strip())
    vocab = np.array([k for k, v in items])
    lookup = {k : i for i, (k, v) in enumerate(vocab)}
    return vocab, lookup

def main():
    parser = argparse.ArgumentParser('Dimensionality reduces a space using the SVD')
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), help='Output file')
    parser.add_argument('--contextsoutput', '-x' type=argparse.FileType('w'),
                        help='Output file (contexts matrix)')
    parser.add_argument('-k', type=int, default=300, help='Target dimensionality')
    parser.add_argument('--rows', '-r', type=argparse.FileType('r'), help='Frequency file of rows.')
    parser.add_argument('--cols', '-c', type=argparse.FileType('r'), help='Frequency file of cols.')
    args = parser.parse_args()

    rvocab, rows = load_targets(args.rows)
    cvocab, cols = load_targets(args.cols)

    spmat = sp.lil_matrix((len(rows), len(cols)))
    for line in args.input:
        line = line.strip()
        row, col, value = line.split()
        value = float(value)

        i, j = rows[row], cols[col]
        spmat[i,j] = value

    u, s, vt = la.svds(spmat, k=args.k)
    s12 = np.sqrt(s)
    vectors = u.dot(np.diag(s12))

    np.savez_compressed(args.output, matrix=vectors, vocab=rvocab)

    if args.contextsoutput:
        contexts = np.diag(s12).dot(vt).T
        np.savez_compressed(args.contextsoutput, matrix=contexts, vocab=cvocab)



if __name__ == '__main__':
    main()
