#!/usr/bin/env python2.7

def pos(word):
    return word[-1]
    dash = word.rindex("-")
    return word[dash+1:]

def bigrams(sentence):
    for i in xrange(len(sentence) - 1):
        yield i, sentence[i], sentence[i + 1]



