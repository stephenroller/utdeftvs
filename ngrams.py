#!/usr/bin/env python

import sys
import argparse
from collections import Counter
from itertools import chain, combinations, permutations

def parse_n(s):
    if ',' in s:
        return chain(parse_n(ss) for ss in s.split(","))
    elif '-' in s:
        n, m = s.split("-")
        return xrange(int(n), int(m) + 1)
    else:
        return [int(s)]

def ngrams(sentence, n):
    for i in xrange(len(sentence) - n):
        yield sentence[i:i+n]

def load_whitelist(f):
    return [l.strip().split("\t")[0].split() for l in f]

def main():
    parser = argparse.ArgumentParser('Extracts n-grams')
    parser.add_argument('-n', help='n-gram size.')
    parser.add_argument('--whitelist', '-w', metavar='FILE', type=argparse.FileType('r'), help='Only extract ngrams from a whitelist.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', type=argparse.FileType('r'), help='Input file', default=sys.stdin)
    parser.add_argument('--mode', '-m', metavar='[ngram,perm]', default='ngram')
    parser.add_argument('--contexts', action='store_true')
    args = parser.parse_args()

    ns = list(parse_n(args.n))
    if args.whitelist:
        whitelist = load_whitelist(args.whitelist)
        whitelist = [ng for ng in whitelist if len(ng) in ns]
        if args.mode == 'perm':
            whitelist = list(chain(*[permutations(ng, len(ng)) for ng in whitelist]))
        whitelist = set(" ".join(ng) for ng in whitelist)
    else:
        whitelist = None


    for sentence in args.input:
        sentence = sentence.strip().split()
        sentence_c = Counter(sentence)
        for n in ns:
            for ngram in ngrams(sentence, n):
                ngram_s = " ".join(ngram)
                if whitelist and ngram_s not in whitelist:
                    continue
                if args.contexts:
                    for k, v in sentence_c.iteritems():
                        if k in ngram and v > 1:
                            print "%s\t%s\t%d" % (ngram_s, k, v - 1)
                        else:
                            print "%s\t%s\t%d" % (ngram_s, k, v)
                else:
                    print ngram_s + "\t1"



if __name__ == '__main__':
    main()

