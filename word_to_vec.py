# -*- coding: utf-8 -*-
"""
Created on Thu May 25 12:33:39 2017

@author: Janaka
"""
MODEL_FILE = 'I:/google_model/GoogleNews-vectors-negative300.bin'
import gensim


model = gensim.models.KeyedVectors.load_word2vec_format(MODEL_FILE, binary=True) 

