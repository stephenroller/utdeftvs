#!/usr/bin/env python2.7
import sys
import logging
import gc
from collections import Counter, defaultdict

logging.basicConfig(level=logging.DEBUG)

def read_corpus(corpus):
    for line in corpus:
        yield line.rstrip().split(" ")

def load_contexts(file):
    return set(w.strip() for w in file if w.strip())

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

        if sno % 50000 == 0:
            # flush out the memory
            for target, values in space.iteritems():
                for context, count in values.iteritems():
                    yield target, context, count
            space = defaultdict(Counter)
            gc.collect()

            logging.info("Processed line %.2fm (memory flushed)" % (sno/1e6))


    for target, values in space.iteritems():
        for context, count in values.iteritems():
            yield target, context, count


def main():
    # now let's actually make the space
    contexts = load_contexts(open('contexts.txt'))
    for target, context, count in make_bow_vectorspace(sys.stdin, contexts):
        print "%s\t%s\t%d" % (target, context, count)

if __name__ == '__main__':
    main()


