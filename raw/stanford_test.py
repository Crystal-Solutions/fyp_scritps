# -*- coding: utf-8 -*-
"""
Created on Tue May  9 17:50:43 2017

@author: Janaka
"""

from nltk.tag import StanfordPOSTagger
from nltk import sent_tokenize, word_tokenize
st = StanfordPOSTagger('english-bidirectional-distsim.tagger') 
#tagged = st.tag('Rami Eid is studying at Stony Brook University in NY'.split())

sentences = 'Mr. Shanika is a good man.This is the first sentnece. This is the second. And this is the third'
s= sent_tokenize(sentences)
t_s = [st.tag(word_tokenize(i)) for i in s]