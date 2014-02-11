#!/usr/bin/env python2.7

"""
Converts from DHG's TLP (Text, Lemma, POS) format into CoNLL format
for use as input to the MaltParser.

TLP format is one sentence per line,

TEXTID <tab> TYPE <tab> SENTENCE1 <tab> SENTENCE2 <tab> ...
SENTENCE := WORD1 <space> WORD2 <space> ...
WORD := TOKEN '|' LEMMA '|' POS

"""

import sys
import os
#from subprocess import Popen, PIPE
from os import popen3

TREETAGGER_BIN = "/scratch/01813/roller/software/src/maltparser/treetagger/cmd/tree-tagger-english-utf8"
MALT_DIR = "/scratch/01813/roller/software/src/maltparser"
JARS = "lexsem-assembly.jar liblinear-1.92.jar libsvm.jar maltparser-1.7.2.jar".split()
CLASSPATH = ":".join(MALT_DIR + "/" + j for j in JARS)
MCO = "engmalt.linear-1.7"
MALT_CMD = "/share/apps/teragrid/jdk64/jdk1.7.0_45/bin/java -Xmx1G -cp %s org.maltparser.Malt -w %s -c %s -m parse" % (CLASSPATH, MALT_DIR, MCO)

def treetagger_real(sentence):
    rawtext = " ".join(sentence)
    #p = Popen(TREETAGGER_BIN, stdin=PIPE, stdout=PIPE, stderr=devnull)
    #(stdin, stdout) = p.communicate(rawtext + "\n")
    stdin, stdout, stderr = popen3(TREETAGGER_BIN)
    stdin.write(rawtext + "\n")
    stdin.close()
    output = stdout.read()
    output_lst = []
    for line in output.split("\n"):
        line = line.strip()
        if not line: continue
        word, pos, lemma = line.split("\t")
        if lemma == "<unknown>": lemma = word
        output_lst.append((word, lemma, pos))
    return output_lst

def fix_pos(pos, lemma):
    direct_fixes = {
        '-LRB-' : '(',
        '-RRB-' : ')',
        '-LSB-' : '(',
        '-RSB-' : ')',
        '-LCB-' : '(',
        '-RCB-' : ')',
        '.' : 'SENT',
        'NNPS' : 'NPS',
        'NNP' : 'NP',
        'PRP' : 'PP',
        'PRP$' : 'PP$',

    }
    if pos in direct_fixes:
        return direct_fixes[pos]
    pos2 = pos[:2]
    # handle the verbs be and have
    if lemma == 'have' and pos2 == 'VB':
        return pos[0] + 'H' + pos[2:]
    elif lemma == 'be' and pos2 == 'VB':
        return pos
    elif pos2 == 'VB':
        return pos[0] + 'V' + pos[2:]
    else:
        # unchanged
        return pos

def fake_malt_parse(tagged_sentences):
    output = []
    for s in tagged_sentences:
        words = []
        for i, (t, l, p) in enumerate(s, 1):
            line = "%d\t%s\t%s\t%s\t%s\t_\t0\ta\t_\t_" % (i, t, l, p, p)
            words.append(line.split("\t"))
        output.append(words)
    return output

malt_stdin, malt_stdout, malt_stderr = popen3(MALT_CMD)

def real_malt_parse(tagged_sentences):
    parsed_sentences = []

    for s in tagged_sentences:
        for i, (t, l, p) in enumerate(s, 1):
            line = "%d\t%s\t%s\t%s\t%s\t_\t0\ta\t_\t_" % (i, t, l, p, p)
            malt_stdin.write(line + "\n")
        malt_stdin.write("\n")
        malt_stdin.flush()

        # read it back
        this_parse = []
        for j in xrange(i):
            line = malt_stdout.readline()
            c = line.split("\t")
            fields = [1, 2, 3, 0, 6]
            w = [c[i] for i in fields]
            w.append(c[7].upper())
            this_parse.append(w)
        parsed_sentences.append(this_parse)

        # drop the extra null
        malt_stdout.readline()

    return parsed_sentences

malt_parse = real_malt_parse

def main():
    for line in sys.stdin:
        line = line.strip()
        split = line.split("\t")
        key = split[0]
        tagged_sentences = []
        print '<text id="%s">' % key
        for sentence in split[2:]:
            words = sentence.split(" ")
            parsed = (w.split("|") for w in words)
            tagged = ((t, l, fix_pos(p, l)) for t, l, p in parsed)
            #sentence = (t for t, l, p in parsed)
            #tagged = treetagger(sentence)
            tagged_sentences.append(tagged)
        malt_parsed = malt_parse(tagged_sentences)
        for sentence in malt_parsed:
            if not sentence:
                continue
            print "<s>"
            for word in sentence:
                print "\t".join(word)
            print "</s>"
        print "</text>"

    malt_stdin.close()
    malt_stdout.close()
    malt_stderr.close()


if __name__ == '__main__':
    main()

