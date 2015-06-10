#!/usr/bin/env python
import sys
import argparse
import pickle
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
from sklearn.preprocessing import normalize

def similarity_benchmark_spearman(space, data):
    coses = []
    gold = []
    for i, row in data.iterrows():
        try:
            vec1 = space.get_vector(row['word1'])
            vec2 = space.get_vector(row['word2'])
        except KeyError:
            continue
        cos = vec1.dot(vec2) / np.sqrt(vec1.dot(vec1) * vec2.dot(vec2))
        coses.append(cos)
        gold.append(row['similarity'])

    rho, p = spearmanr(coses, gold)
    n = len(coses)
    return rho, p, n

def print_similarity_benchmark(space, name, dataname):
    data = pd.read_table(dataname)
    print "%s:" % name
    rho, p, n = similarity_benchmark_spearman(space, data)
    print "    n = %d" % n
    print "  rho = %f" % rho
    print "    p = %f" % p


def relationship_benchmark_accuracy(space, data):
    # first we need to remove OOV words
    mask = []
    for i, row in data.iterrows():
        not_oov = ((row['word1'] in space.row2id) and
                   (row['word2'] in space.row2id) and
                   (row['word3'] in space.row2id) and
                   (row['word4'] in space.row2id))
        mask.append(not_oov)
    data = data[mask]

    full_matrix = space.get_cooccurrence_matrix().mat.A
    full_normalized = normalize(full_matrix, axis=1, norm='l2')
    del full_matrix

    # and now calculate the predicted 4th word for every row
    # using each of the different methods:
    # 3cosadd, 3cosmul
    A = []
    As = []
    B = []
    for i, row in data.iterrows():
        A.append(full_normalized[space.row2id[row['word1']]])
        As.append(full_normalized[space.row2id[row['word2']]])
        B.append(full_normalized[space.row2id[row['word3']]])
    A = np.matrix(A)
    As = np.matrix(As)
    B = np.matrix(B)
    full_T = full_normalized.T
    del full_normalized

    STEP = 1000
    cosadd_preds = []
    cosmul_preds = []
    # gotta do it in increments or we'll run out of memory
    for i in xrange(0, A.shape[0], STEP):
        print "%d/%d" % (i, A.shape[0])
        j = min(i + STEP, A.shape[0])
        lhs = B[i:j] - A[i:j] + As[i:j]
        Bs_argmax = lhs.dot(full_T).argmax(axis=1).T.A[0]
        cosadd_preds += [space.id2row[int(bs)] for bs in Bs_argmax]

        #AcosBs = A[i:j].dot(full_T)
        #AscosBs = As[i:j].dot(full_T)
        #BcosBs = B[i:j].dot(full_T)

        #_3cosadd = (BcosBs - AcosBs + AscosBs)
        #cosadd_preds += [space.id2row[int(bs)] for bs in _3cosadd.argmax(axis=1).T.A[0]]
        #_3cosmul = np.divide(np.multiply(BcosBs, AscosBs), AcosBs + 1e-3)
        #cosmul_preds += [space.id2row[int(bs)] for bs in _3cosmul.T.A[0]]

    data['_3cosadd'] = cosadd_preds
    #data['_3cosmul'] = cosmul_preds

    acc_add = np.sum(data['_3cosadd'] == data['word4'])/float(len(data))
    #acc_mul = np.sum(data['_3cosmul'] == data['word4'])/float(len(data))


    #return [('n', len(data)), ('Overall 3cosadd', acc_add), ('Overall 3cosmul', acc_mul)]
    return [('n', len(data)), ('Overall 3cosadd', acc_add)]








def print_relationship_benchmark(space, name, dataname):
    data = pd.read_table(dataname)
    print "%s:" % name
    accuracies = relationship_benchmark_accuracy(space, data)
    for category, accuracy in accuracies:
        print "  %15s = %f" % (category, accuracy)



def main():
    parser = argparse.ArgumentParser('Runs a number of benchmarks on a vector space.')
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input space')
    #parser.add_argument('benchmark', default='all', help='Which benchmark(s) to run')
    args = parser.parse_args()
    space = pickle.load(args.input)

    print_similarity_benchmark(space, "WordSim353", "data/ws353.tsv")
    print
    print_similarity_benchmark(space, "Rubenstein-Goodenough", "data/rg.tsv")
    print
    print_similarity_benchmark(space, "MEN", "data/men.tsv")
    print

    print_relationship_benchmark(space, "MSR Relations", "data/msr_relations.tsv")
    print
    print_relationship_benchmark(space, "Google Relations", "data/google_relations_lc.tsv")
    print



if __name__ == '__main__':
    main()
