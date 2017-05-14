# -*- coding: utf-8 -*-
"""
Created on Sun May 14 12:37:50 2017

@author: Shanika Ediriweera
"""

from nltk import word_tokenize
from nltk.tag import SennaTagger
senna = SennaTagger('../../tools/senna')
sents = ["All the banks are closed", "Today is Sunday"]

tokenized_sents = [word_tokenize(sent) for sent in sents]
print(senna.tag_sents(tokenized_sents))