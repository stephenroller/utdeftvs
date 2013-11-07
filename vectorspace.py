#!/usr/bin/env python
import argparse
import logging
from collections import Counter, defaultdict
from contentwords import is_content_word

logging.basicConfig(level=logging.DEBUG)

MEM_LIMIT = 1024

import psutil
from os import getpid

def mem_usage():
    p = psutil.Process(getpid())
    # return in MB
    return p.get_memory_info()[0]/1048576.

def read_corpus(filename):
    with open(filename, "r") as corpus:
        for line in corpus:
            yield line.rstrip().split(" ")

def find_targets_and_contexts(corpus_filename, min_target_count, max_num_contexts):
    all_counts = Counter()
    content_counts = Counter()

    for sno, sentence in enumerate(read_corpus(corpus_filename)):
        all_counts.update(sentence)
        content_counts.update(filter(is_content_word, sentence))
        if sno % 100000 == 0:
            logging.info("Processed line %.1fm, mem usage: %.2f MB" % (sno/1e6, mem_usage()))

    target_words = set(k for k, v in all_counts.iteritems() if v >= min_target_count)
    content_words = set(k for k, v in content_counts.most_common(max_num_contexts))

    return target_words, content_words

def make_bow_vectorspace(corpus_filename, targets, contexts):
    space = defaultdict(Counter)
    for sno, sentence in enumerate(read_corpus(corpus_filename)):
        sentence = [w for w in sentence if (w in contexts or w in targets)]
        for i in xrange(len(sentence)):
            middle = sentence[i]
            if middle not in targets:
                continue
            bow = [w for w in sentence[:i] + sentence[i+1:] if w in contexts]
            space[middle].update(bow)
        if sno % 100000 == 0:
            # check memory and stuff
            if mem_usage() > MEM_LIMIT:
                logging.info("Flushing memory...")
                #flush_out(space)
                space = defaultdict(Counter)

            logging.info("Processed line %.1fm, mem usage: %.2f MB" % (sno/1e6, mem_usage()))

    return space


def main():
    import sys
    corpus_filename = sys.argv[1]
    logging.info("Starting...")
    targets, contexts = find_targets_and_contexts(corpus_filename, 50, 10000)
    logging.info("Found targets (%.1fk), contexts (%.1fk)." % (len(targets)/1e3, len(contexts)/1e3))
    space = make_bow_vectorspace(corpus_filename, targets, contexts)


if __name__ == '__main__':
    main()

