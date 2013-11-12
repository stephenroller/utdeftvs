#!/usr/bin/env python
import sys
import argparse
import logging
from collections import Counter, defaultdict
from contentwords import is_content_word

logging.basicConfig(level=logging.DEBUG)

# MEM_LIMIT = 1024
# import psutil
# from os import getpid
# import gc

# def mem_usage():
#     p = psutil.Process(getpid())
#     # return in MB
#     return p.get_memory_info()[0]/1048576.

def read_corpus(corpus):
    for line in corpus:
        yield line.rstrip().split(" ")

def find_contexts(corpus, max_num_contexts):
    content_counts = Counter()
    for sno, sentence in enumerate(read_corpus(corpus)):
        content_counts.update(filter(is_content_word, sentence))
        if sno % 100000 == 0:
            logging.info("Processed line %.1fm, mem usage: %.2f MB" % (sno/1e6, mem_usage()))
    content_words = set(k for k, v in content_counts.most_common(max_num_contexts))
    return content_words

def load_contexts(file):
    return set(w.strip() for w in file if w.strip())

def make_bow_vectorspace(corpus, contexts):
    logging.info("Size of contexts: %d" % len(contexts))
    space = defaultdict(Counter)
    for sno, sentence in enumerate(read_corpus(corpus)):
        sentence_contexts = [(i, w) for i, w in enumerate(sentence) if w in contexts]
        indices = set(i for i, w in sentence_contexts)
        sentence_contexts = Counter(w for i, w in sentence_contexts)
        for t, target in enumerate(sentence):
            space[target].update(sentence_contexts)
            if t in indices:
                # uh oh, we counted a word as cooc'ing with itself. gotta undo that
                space[target].subtract([target])

#         if sno % 10000 == 0:
#             # check memory and stuff
#             if mem_usage() > MEM_LIMIT:
#                 for target, values in space.iteritems():
#                     for context, count in values.iteritems():
#                         yield target, context, count
#                 # time to flush the memory
#                 logging.info("Flushing memory...")
#                 space = defaultdict(Counter)
#                 gc.collect()
# 
#             logging.info("Processed line %.1fm, mem usage: %.2f MB" % (sno/1e6, mem_usage()))
# 

    for target, values in space.iteritems():
        for context, count in values.iteritems():
            yield target, context, count


def main_wc():
    logging.info("Starting...")
    contexts = find_contexts(sys.stdin, 10000)
    logging.info("Found contexts (%.1fk)." % (len(contexts)/1e3))
    for c in contexts:
        print c

def main_vs():
    # now let's actually make the space
    contexts = load_contexts(open('contexts.txt'))
    for target, context, count in make_bow_vectorspace(sys.stdin, contexts):
        print "%s\t%s\t%d" % (target, context, count)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'wc':
        main_wc()
    else:
        main_vs()


