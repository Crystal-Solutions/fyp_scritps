# -*- coding: utf-8 -*-
"""
Created on Wed May 17 15:23:46 2017

@author: Janaka
"""

#def print_def(file_name):
file_name = '../data/senna_output_tagged/all/output/out1.txt'
txt = open(file_name).read().strip()
tags = txt.split('\n')
tags = list(filter(len,tags))
difs = []
for i in range(0,len(tags)-1,2):
    spts = tags[i].split()
    pred_tag = tags[i+1].strip()
    
    if(len(spts)>0 and spts[-1]!=pred_tag):
#        print(i,spts,pred_tag)
        sample_txt = tags[i][0].split()[0]
        difs.append((i,spts,pred_tag,sample_txt))
