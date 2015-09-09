#!/usr/bin/env python

import numpy as np
from sklearn.preprocessing import normalize

class VectorSpace(object):
    def __init__(self, matrix, vocab):
        self.vocab = vocab
        self.matrix = matrix
        self.lookup = {v:i for i, v in enumerate(vocab)}

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.matrix[key]
        elif isinstance(key, str):
            return self.matrix[self.lookup[key]]

    def __contains__(self, key):
        return key in self.lookup

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
        return VectorSpace(normalize(self.matrix, norm='l2', axis=1), self.vocab)

def load_numpy(filename_combined, insertblank=False):
    data = np.load(filename_combined)
    mat = data['matrix']
    labels = data['rows']
    if insertblank:
        dims = mat.shape[1]
        mat = np.concatenate([np.zeros((1, dims), dtype=mat.dtype), mat])
        labels = np.concatenate([np.array(['']), labels])
    return VectorSpace(mat, labels)

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
    matrix = []
    with open(filename) as f:
        for l in f:
            l = l.strip().split()
            word = l.pop(0)
            if word.endswith("-n"):
                word = word[:-2]
            vocab.append(word)
            matrix.append(np.array(map(float, l)))

    matrix = np.array(matrix)
    return VectorSpace(matrix, vocab)

