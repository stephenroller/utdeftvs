#!/usr/bin/env python

import numpy as np
import struct
from sklearn.preprocessing import normalize

class VectorSpace(object):
    def __init__(self, matrix, vocab, cmatrix=None, cvocab=None, **other):
        self.vocab = vocab
        self.matrix = matrix
        self.lookup = {v:i for i, v in enumerate(vocab)}

        self.cmatrix = cmatrix
        self.cvocab = cvocab
        if cvocab is not None:
            self.clookup = {v:i for i, v in enumerate(cvocab)}

        for key, value in other.iteritems():
            setattr(self, key, value)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.matrix[key]
        elif isinstance(key, str):
            return self.matrix[self.lookup[key]]

    def __contains__(self, key):
        return key in self.lookup

    def save(self, filename):
        if self.cmatrix is not None:
            np.savez_compressed(filename, matrix=self.matrix, rows=self.vocab,
                                cmatrix=self.cmatrix, crows=self.cvocab)
        else:
            np.savez_compressed(filename, matrix=self.matrix, rows=self.vocab)

    def save_mikolov_text(self, filename):
        with open(filename, 'w') as f:
            for i, word in enumerate(self.vocab):
                row = self.matrix[i]
                line = " ".join(map(str, row))
                f.write("%s %s\n" % (word, line))

    def subset(self, whitelist):
        whitelist = set(whitelist)
        keep = [(i, word) for i, word in enumerate(self.vocab) if word in whitelist]
        indices, newvocab = zip(*keep)
        newmatrix = self.matrix[indices,:]
        return VectorSpace(newmatrix, newvocab)

    def normalize(self):
        magn = np.sqrt(np.sum(np.square(self.matrix), axis=1))
        nmat = normalize(self.matrix, norm='l2', axis=1)
        if self.cmatrix is not None:
            cmagn = np.sqrt(np.sum(np.square(self.cmatrix), axis=1))
            cnmat = normalize(self.cmatrix, norm='l2', axis=1)
        else:
            cmagn = None
            cnmat = None
        return VectorSpace(nmat, self.vocab, cnmat, self.cvocab, magn=magn, cmagn=cmagn)

    def svd(self, k=0):
        if not k:
            k = self.matrix.shape[1]
        U, s, V = np.linalg.svd(self.matrix, full_matrices=False)
        s = np.sqrt(s)
        U = U.dot(np.diag(s)).astype(np.float32)
        # note we could do V here too...
        return VectorSpace(U, self.vocab)

def load_numpy(filename_combined, insertblank=False):
    data = np.load(filename_combined)
    mat = data['matrix']
    labels = data['rows']
    if insertblank:
        dims = mat.shape[1]
        mat = np.concatenate([np.zeros((1, dims), dtype=mat.dtype), mat])
        labels = np.concatenate([np.array(['']), labels])

    # some spaces have an additional context matrix
    if 'crows' in data:
        cmat = data['cmatrix']
        clabels = data['crows']
        if insertblank:
            dims = cmat.shape[1]
            cmat = np.concatenate([np.zeros((1, dims), dtype=cmat.dtype), cmat])
            clabels = np.concatenate([np.array(['']), clabels])
    else:
        cmat = None
        clabels = None

    return VectorSpace(mat, labels, cmatrix=cmat, cvocab=clabels)

def load_numpy_and_vocab(filename_matrix, filename_rows, insertblank=False):
    mat = np.load(filename_matrix)
    with open(filename_rows) as rowfile:
        labels = [l.strip().split("\t")[0] for l in rowfile]
    if insertblank:
        dims = mat.shape[1]
        mat = np.concatenate([np.zeros((1, dims), dtype=mat.dtype), mat])
        labels.insert(0, '')
    return VectorSpace(mat, labels)

def load_mikolov_text(filename):
    vocab = []
    with open(filename) as f:
        X, Y = f.readline().strip().split()
        X, Y = int(X), int(Y)
        matrix = np.zeros((X, Y))

        for i, l in enumerate(f):
            l = l.strip().split()
            word = l.pop(0)
            vocab.append(word)
            matrix[i] = np.array(map(float, l))

    return VectorSpace(matrix, vocab)

def load_mikolov_binary(filename, insertblank=False):
    FLOAT_SIZE = 4
    spacefile = open(filename)
    header = spacefile.readline().rstrip()
    vocab_s, dims = map(int, header.split(" "))

    vocab = []
    if insertblank:
        vocab.insert(0, '')

    # init matrix
    matrix = np.zeros((vocab_s + int(insertblank), dims), dtype=np.float)

    i = int(insertblank)
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

    return VectorSpace(matrix, np.array(vocab))


