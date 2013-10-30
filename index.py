#!/usr/bin/env python

import argparse
import cPickle
import logging
import os.path
from hashlib import md5
from struct import unpack
from contentwords import is_content_word

def bloomHash(key, k=2, m=256):
    bitvector = 0
    mask = m - 1
    hashes = md5(key).digest()
    for i in xrange(0, k*2, 2):
        hashint = unpack("H", hashes[i:i+2])[0] & mask
        bitvector |= (2 << hashint)
    return bitvector

def power2int(n):
    i = 2
    while i < n:
        if i == n:
            return n
        i <<= 1
    raise argparse.ArgumentTypeError("%d is not a power of 2." % n)

def query_index(corpus_filename, index, words):
    blooms = index['blooms']
    blocksize = index['blocksize']
    M = index['M']

    s = reduce(lambda x, y: x | y, (bloomHash(w, m=M) for w in words if is_content_word(w)))
    candidates = [k for k, bf in blooms if (bf & s) == s]
    logging.debug("Query # candidates: %d/%d" % (len(candidates), len(blooms)))

    with open(corpus_filename) as corpus:
        for pos in candidates:
            logging.debug("Checking block %s..." % pos)
            corpus.seek(pos)
            lines = (l for l in (corpus.readline().strip() for i in xrange(blocksize)) if l)
            for line in lines:
                sentence = set(line.split())
                if all(w in sentence for w in words):
                    yield line

def corpus_file(string):
    if not os.path.isfile(string):
        raise argparse.ArgumentTypeError("%s is not a valid corpus file." % string)
    return string

def corpus_file_with_index(string):
    string = corpus_file(string)
    if not os.path.isfile(string + ".index.pkl"):
        raise argparse.ArgumentTypeError("%s does not have an index." % string)
    return string

def create_index(corpus_filename, bits=4096, blocksize=200):
    inpt = open(corpus_filename, "r")
    blooms = []
    position = inpt.tell()
    bf = 0
    i = 0
    while inpt:
        lines = [l for l in (inpt.readline().strip() for i in xrange(blocksize)) if l]
        if not lines:
            break
        words = set(w for line in lines for w in line.split(" "))
        for word in words:
            if is_content_word(word):
                bf |= bloomHash(word, m=bits)
        blooms.append((position, bf))
        bf = 0
        i += blocksize
        if i % 100000 == 0:
            logging.debug("current line, position: %8d, %3.2fM" % (i, position/(1024.*1024)))
        position = inpt.tell()

    obj = dict(blooms=blooms, blocksize=blocksize, M=bits)
    with open(corpus_filename + ".index.pkl", "w") as outf:
        cPickle.dump(obj, outf)
    return obj

def load_index(corpus_filename):
    index = cPickle.load(open(corpus_filename + ".index.pkl"))
    return index

def main():
    parser = argparse.ArgumentParser(
                description='Indexes or queries the corpus to easily retrieve content words.',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(help='command to run', dest='command')

    # index only options
    parser_i = subparsers.add_parser('index', help='indexes a corpus')
    parser_i.add_argument('--bits', '-M', metavar='N', default=4096, type=power2int, help='Number bits for bloom filters; must be a power of 2.')
    parser_i.add_argument('--blocksize', '-B', metavar='blocksize', default=200, type=int, help='Size of blocks in number of sentences.')
    parser_i.add_argument('--corpus', '-c', metavar='FILE', help='corpus file', required=True, type=corpus_file)
    parser_i.add_argument('--verbose', '-v', action='store_true', help='verbose mode')

    # query options
    parser_q = subparsers.add_parser('query', help='queries a corpus', description='')
    parser_q.add_argument('words', nargs='+', metavar='WORD', help='Word to query')
    parser_q.add_argument('--corpus', '-c', metavar='FILE', help='corpus file', required=True, type=corpus_file_with_index)
    parser_q.add_argument('--verbose', '-v', action='store_true', help='verbose mode')

    args = parser.parse_args()
    logging.basicConfig(
            format="[ %(levelname)-10s %(module)-8s %(asctime)s  %(relativeCreated)-10d ]  %(message)s",
            datefmt="%H:%M:%S:%m",
            level=args.verbose and logging.DEBUG or logging.INFO)

    if args.command == 'index':
        create_index(args.corpus, bits=args.bits, blocksize=args.blocksize)
    elif args.command == 'query':
        index = load_index(args.corpus)
        for line in query_index(args.corpus, index, args.words):
            print line

if __name__ == '__main__':
    main()


