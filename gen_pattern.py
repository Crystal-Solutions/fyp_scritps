# -*- coding: utf-8 -*-
"""
Created on Thu May 25 20:31:00 2017

@author: Shanika Ediriweera
"""

"""
generate pattern for word2vec unigrams for 1 word window
"""
def gen_w2v_unigram_single():   
    with open('generated_pattern.txt','w') as f:
        for i in range(7,307):
            line = 'U:w2v-1 X=%X[ 0,'+ str(i) + ']'
            f.write(line+"\n")
            print(line)
            
    
"""
generate pattern for word2vec unigrams for 1 word window commented
"""
def gen_w2v_unigram_single_commented():   
    with open('generated_pattern.txt','w') as f:
        for i in range(7,307):
            line = '#U:w2v-1 X=%X[ 0,'+ str(i) + ']'
            f.write(line+"\n")
            print(line)

"""
generate pattern
"""
def generate_pattern():
    gen_w2v_unigram_single()
    
generate_pattern()