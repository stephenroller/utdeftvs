#!/usr/bin/env python

import sys
import pandas as pd
from itertools import izip

f1 = open("word_relationship.questions")
f2 = open("word_relationship.answers")

data = []
for q, a in izip(f1, f2):
    w1, w2, w3 = q.strip().split()
    c, w4 = a.strip().split()
    data.append({'word1': w1, 'word2': w2, 'word3': w3, 'word4': w4, 'category': c})

pd.DataFrame(data).to_csv(sys.stdout, index=False, sep="\t")

