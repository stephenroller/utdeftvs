#!/usr/bin/env python2.7

import sys
import argparse

GOOD_POS = dict(JJ="a", NN="n", NP="p", VV="v")

def is_content_word(word_pos):
    if not word_pos:
        return False
    pos = word_pos.split("/")[-1]
    word = "".join(word_pos.split("/")[:-1])
    if pos[:2] not in GOOD_POS:
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
    args = parser.parse_args()
    inpt = args.input

    for sentence in inpt:
        sentence = sentence.strip().split(" ")
        sentence = (is_content_word(wp) for wp in sentence)
        sentence = [w for w in sentence if w]
        if len(sentence) >= 2:
            print " ".join(sentence)


if __name__ == '__main__':
    main()

