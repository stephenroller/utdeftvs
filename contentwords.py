#!/usr/bin/env python2.7

import sys
import argparse

GOOD_POS = dict(JJ="a", NN="n", NP="p", VV="v")

def is_content_word(word_pos):
    if not word_pos:
        return False
    pos = word_pos.split("/")[-1]
    word = "".join(word_pos.split("/")[:-1])
    if '__' in word_pos or pos[:2] not in GOOD_POS:
        return False
    else:
        shortpos = GOOD_POS[pos[:2]]
        if shortpos == 'p':
            return word + "-" + shortpos
        else:
            return word.lower() + "-" + shortpos

def main():
    parser = argparse.ArgumentParser(
                description='Filters non-content words from a given vs corpus.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', type=argparse.FileType('r'), help='Input file', default=sys.stdin)
    parser.add_argument('--usingpos', '-p', action='store_true', help='Filter content words using the pos tags.')
    parser.add_argument('--stopwords', '-s', metavar='FILE', type=argparse.FileType('r'), help='Stopwords file.')
    args = parser.parse_args()

    stopwords = set()
    if args.stopwords:
        stopwords = set(l.strip().split("\t")[0] for l in args.stopwords)

    inpt = args.input

    for sentence in inpt:
        sentence = sentence.strip().split(" ")
        if args.usingpos:
            sentence = (is_content_word(wp) for wp in sentence)
        if stopwords:
            sentence = (wp for wp in sentence if wp.lower() not in stopwords)
        sentence = [w for w in sentence if w]
        if len(sentence) >= 2:
            print " ".join(sentence)


if __name__ == '__main__':
    main()

