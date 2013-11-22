#!/usr/bin/env python2.7

def pos(word):
    return word[-1]
    dash = word.rindex("-")
    return word[dash+1:]

def ngrams(sentence, n):
    assert isinstance(n, int) and n > 0
    for i in xrange(len(sentence) + 1 - n):
        yield i, tuple(sentence[i:i+n])

def bigrams(sentence):
    return ngrams(sentence, 2)



