
#!/usr/bin/env python

import sys
import argparse

GOOD_POS = set("JJ JJR JJS NN NNS NP NPS VV VVD VVG VVN VVP VVZ".split())

def is_content_word(word_pos):
    return word_pos.split("/")[-1] in GOOD_POS

def main():
    parser = argparse.ArgumentParser(
                description='Filters non-content words from a given vs corpus.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input file')
    args = parser.parse_args()

    if not args.input or args.input == "-":
        args.input = sys.stdin
    else:
        args.input = open(args.input)

    for sentence in args.input:
        sentence = [wp for wp in sentence.strip().split(" ") if is_content_word(wp)]
        if sentence:
            print " ".join(sentence)


if __name__ == '__main__':
    main()

