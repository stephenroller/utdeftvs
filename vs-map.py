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

def make_bow_vectorspace(corpus, contexts):
    logging.info("Size of contexts: %d" % len(contexts))
    space = defaultdict(Counter)
    for sno, sentence in enumerate(read_corpus(corpus), 1):
        sentence_contexts = [(i, w) for i, w in enumerate(sentence) if w in contexts]
        indices = set(i for i, w in sentence_contexts)
        sentence_contexts = Counter(w for i, w in sentence_contexts)
        for t, target in enumerate(sentence):
            space[target].update(sentence_contexts)
            if t in indices:
                # uh oh, we counted a word as cooc'ing with itself. gotta undo that
                space[target].subtract([target])

        if sno % FLUSH_FREQUENCY == 0:
            # flush out the memory
            for target, values in space.iteritems():
                for context, count in values.iteritems():
                    if count > 0:
                        yield target, context, count
            space = defaultdict(Counter)
            gc.collect()

            logging.info("Processed line %.2fm (memory flushed)" % (sno/1e6))


    for target, values in space.iteritems():
        for context, count in values.iteritems():
            if count > 0:
                yield target, context, count

def make_ngram_bow_vectorspace(corpus, contexts, n=2, pospattern="an"):
    pospattern = tuple(pospattern)
    assert len(pospattern) == n, "POS pattern must be the same size as the ngram size"

    space = defaultdict(Counter)
    for sno, sentence in enumerate(read_corpus(corpus), 1):
        sentence_contexts = [(i, w) for i, w in enumerate(sentence) if w in contexts]
        indices = set(i for i, w in sentence_contexts)
        sentence_contexts = Counter(w for i, w in sentence_contexts)
        for t, ngram in ngrams(sentence, n):
            if tuple(map(pos, ngram)) == pospattern:
                space[ngram].update(sentence_contexts)
                for i in xrange(n):
                    if t + i in indices:
                        space[ngram].subtract(ngram[i])

            if sno % FLUSH_FREQUENCY == 0:
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
    args = parser.parse_args()

    # now let's actually make the space
    contexts = load_contexts(args.contexts)
    if args.adjnoun:
        bow_f = partial(make_ngram_bow_vectorspace, pospattern="an", n=2)
    elif args.nounnoun:
        bow_f = partial(make_ngram_bow_vectorspace, pospattern="nn", n=2)
    else:
        bow_f = make_bow_vectorspace

    for target, context, count in bow_f(args.input, contexts):
        print "%s\t%s\t%d" % (target, context, count)

if __name__ == '__main__':
    main()


