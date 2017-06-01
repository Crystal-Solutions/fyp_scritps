# -*- coding: utf-8 -*-
"""
Created on Mon May 15 13:24:01 2017

@author: Janaka
"""

import os
import random
fileNames = ['feedback_cs2012_4',
             'feedback_cs2062_1',
             'feedback_cs2012_1',
             'feedback_cs2202_7',
             'feedback_cs2202_2',
             'feedback_cs2202_6',
             'feedback_cs2202_10']
fileNames = [f+'.txt' for f in fileNames]

SRC_DIR = '../data/senna_output_tagged'
DEST_DIR = '../data/senna_output_tagged/all/cross/'

def sent_to_text(lst):
    txt = ""
    for s in lst:
        txt+= s+"\n\n"
    return txt.strip()

sents = []
            
for fileName in fileNames:
    txt_file_path = os.path.join(SRC_DIR, fileName)
    f = open(txt_file_path)
    sents += f.read().strip().split('\n\n')
random.seed(0)
random.shuffle(sents)


wordCount = 0
for s in sents:
    x = s.strip().split("\n")
    wordCount+= len(x)


group_count = 10
group_size = wordCount/group_count

size_of_this_group = 0
train_txts = []
test_txts = []
group_start_i = 0
for i,s in enumerate(sents):
    size_of_this_group+= len(s.strip().split('\n'))
    
    if(size_of_this_group>group_size or s == sents[-1]):
        test_txts.append((sent_to_text(sents[group_start_i:i+1])).strip())
        train_txts.append((sent_to_text(sents[:group_start_i])+"\n\n"+sent_to_text(sents[i+1:])).strip())
#        train_txts.append()
        print(size_of_this_group)
        group_start_i = i+1
        size_of_this_group = 0
#        break
    
for i, (tr, ts) in enumerate(zip(train_txts,test_txts)):
    f = open(DEST_DIR+"train_"+str(i)+'.txt','w')
    f.write(tr)
    f.close()
    f = open(DEST_DIR+"test_"+str(i)+'.txt','w')
    f.write(ts)
    f.close()
    print(i,len(tr),len(ts), len(tr)+len(ts))




