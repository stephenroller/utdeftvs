#!/usr/bin/env python2.7
import sys
import logging
import argparse
import gc
from collections import Counter, defaultdict
from functools import partial

from util import pos, ngrams

logging.basicConfig(level=logging.DEBUG)

FLUSH_FREQUENCY = 50000

def read_corpus(corpus):
    for line in corpus:
        yield line.rstrip().split(" ")

def load_contexts(file):
    return set(w.strip().split("\t")[0] for w in file if w.strip())

def make_ngram_bow_vectorspace(corpus, contexts, n=1, pospattern=False, window=0, flush_frequency=FLUSH_FREQUENCY):
    if pospattern:
        pospattern = tuple(pospattern)
        assert len(pospattern) == n, "POS pattern must be the same size as the ngram size"
    else:
        pospattern = False

    space = defaultdict(Counter)
    for sno, sentence in enumerate(read_corpus(corpus), 1):
        sentence_contexts = [(i, w) for i, w in enumerate(sentence) if w in contexts]
        indices = set(i for i, w in sentence_contexts)
        counted_sentence_contexts = Counter(w for i, w in sentence_contexts)
        for t, ngram in ngrams(sentence, n):
            if not pospattern or tuple(map(pos, ngram)) == pospattern:
                if not window:
                    # use entire sentence as context
                    space[ngram].update(counted_sentence_contexts)
                    for i in xrange(n):
                        if t + i in indices:
                            space[ngram].subtract(ngram[i])
                else:
                    # use just a window as a context. this is a bit trickier, probably a bit slower
                    left_t = max(0, t - window)
                    right_t = min(len(sentence) - 1, t + n + window)
                    window_context = sentence[left_t:t] + sentence[t+n:right_t]
                    window_context = [w for w in window_context if w in contexts]
                    space[ngram].update(window_context)

            if sno % flush_frequency == 0:
                for ngram, values in space.iteritems():
                    for context, count in values.iteritems():
                        if count > 0:
                            yield "__".join(ngram), context, count
                space = defaultdict(Counter)
                gc.collect()

    for ngram, values in space.iteritems():
        for context, count in values.iteritems():
            if count > 0:
                yield "__".join(ngram), context, count

def main():
    parser = argparse.ArgumentParser(
                description='')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input vector space', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--contexts', '-c', metavar='FILE', type=argparse.FileType('r'), help='File of contexts (or counts w/ counts)', default='contexts.txt')
    parser.add_argument('--adjnoun', action='store_true', help='Compute vectors for adj-nouns.')
    parser.add_argument('--nounnoun', action='store_true', help='Compute vectors for noun-nouns.')
    parser.add_argument('--window', type=int, default=0, help='Max context window size (0 for whole sentence context)')
    args = parser.parse_args()

    # now let's actually make the space
    contexts = load_contexts(args.contexts)
    if args.adjnoun:
        bow_f = partial(make_ngram_bow_vectorspace, pospattern="an", n=2, window=args.window)
    elif args.nounnoun:
        bow_f = partial(make_ngram_bow_vectorspace, pospattern="nn", n=2, window=args.window)
    else:
        bow_f = partial(make_ngram_bow_vectorspace, n=1, window=args.window)

    for target, context, count in bow_f(args.input, contexts):
        print "%s\t%s\t%d" % (target, context, count)

if __name__ == '__main__':
    main()


