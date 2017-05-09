# -*- coding: utf-8 -*-
"""
Created on Mon May  8 17:25:27 2017
This one is to use nltk default corpus loader to load our annotations
@author: Janaka
"""


from nltk.corpus import LazyCorpusLoader,ConllChunkCorpusReader



SOURCE_DIR = '../boi_pos_data/'

boi_pos_data = LazyCorpusLoader(
    SOURCE_DIR, ConllChunkCorpusReader,
    [SOURCE_DIR+'feedback_cs2012_2-result.txt'], ('T'),
    tagset='wsj', encoding='ascii')


test_sents = boi_pos_data.chunked_sents('test.txt', chunk_types=['T'])
print(test_sents)