#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	TOKENISATION AS WELL AS CASE FOLDING

'''
###IMPORTS######
import sys
import re
import nltk
from nltk.util import ngrams
import string
from stemmer import *

a = ["&nbsp;","&gt;","&lt;","&quot","\n","/ref"]
def token(final,id,field):
    if len(final)==0:
	return []
    for i in a:
	final = final.replace(i," ")
    replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
    final = final.lower()	
    final = final.translate(replace_punctuation)
    final = final.split(" ")
    l = final
    l=filter(lambda a:a!='', l)
    l = stemList(l)
    final = []
    new = list(set(l))
    new.sort()
    for j in new:
	final.append([j,l.count(j),id,field])
    del new
    del l
    return final    

