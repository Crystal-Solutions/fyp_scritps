# -*- coding: utf-8 -*-
"""
Created on Wed May 17 15:23:46 2017

@author: Janaka
"""

#def print_def(file_name):
file_name = '../data/senna_output_tagged/all/accuracy/cross.txt'
txt = open(file_name).read().strip()
tags = [ [i.split() for i in t.strip().split('\n')] for t in txt.split('* Done')]
results = list(filter(lambda t:len(t)==9,tags))
result_sums = {'B':[[],[],[]],'I':[[],[],[]], 'O':[[],[],[]]}
for res in results:
    for i,tag in enumerate(res[6:]):
        t = tag[0]
        p,r,f = tuple([float(l[3:]) for l in tag[1:]])
        
        result_sums[t][0].append(p)        
        result_sums[t][1].append(r)        
        result_sums[t][2].append(f)
        
        print(tag,i,p,r,f)
        

avg = {'B':[], 'I':[],'O':[]}
for k,v in result_sums.items():
    for j in v:
        avg[k].append(sum(j)/len(j))


f = open(file_name+'.avg.csv','w')
for k,v in avg.items():
    f.write(k+',')
    for val in v:
        f.write(str(val)+', ')
    f.write('\n')
f.close()