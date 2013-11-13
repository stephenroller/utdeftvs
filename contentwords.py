
#!/usr/bin/env python

import sys
import argparse
import logging
from collections import Counter

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
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input file')
    parser.add_argument('--min', '-m', type=int, help='Minimum word count.', default=50)
    args = parser.parse_args()
    inpt = open(args.input)

    wc = Counter()
    logging.info("Pass 1...")
    for sentence in inpt:
        sentence = [is_content_word(wp) for wp in sentence.strip().split(" ")]
        sentence = [w for w in sentence if w]
        wc.update(sentence)

    inpt.seek(0)
    logging.info("Pass 2...")
    for sentence in inpt:
        sentence = [is_content_word(wp) for wp in sentence.strip().split(" ")]
        sentence = [w for w in sentence if w and wc[w] >= args.min]

        if len(sentence) >= 2:
            print " ".join(sentence)


if __name__ == '__main__':
    main()

