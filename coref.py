# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 05:40:27 2017
P
@author: Janaka
"""
import os
import json
SRC_DIR = 'J:/Raw/CS/Sem6B/FYP/data/coref'

for file in os.listdir(SRC_DIR):
    if file.endswith(".txt"):
        print(file)
        file_path = os.path.join(SRC_DIR, file)
        txt_content = open(file_path).read().strip()
        
        jsonObject = json.loads(open(file_path+'.json').read().strip())
        corefs = jsonObject['corefs']
        sents = jsonObject['sentences']
        combinatations = []
        for (k,v) in corefs.items():
#            print(k)
            items = []
            for i,item in enumerate(v):
                s,e,txt,typ = item['startIndex']-1,item['endIndex']-2,item['text'],item['type']
                if(typ!='PROPER' and typ!='PRONOMINAL' ):
                    continue
                startOffset = sents[item['sentNum']-1]['tokens'][s]['characterOffsetBegin']
                endOffset = sents[item['sentNum']-1]['tokens'][e]['characterOffsetEnd']
                
                item_len = endOffset-startOffset
                replaces = {' ,':',', ' .': '.', ' \'': '\'', ' :': ':',  '-LRB- ': '(',  ' -RRB-': ')'}
                for q in replaces:
                    txt = txt.replace(q,replaces[q])
                new_s = txt_content.rfind(txt,0,startOffset+item_len+2)
                new_e = new_s+item_len
                items.append((new_s,new_e,txt,typ))
                if(new_s==-1):
                    print("Errr",startOffset+item_len+2)
                    print(txt,end="=>")
    #                print(txt_content[startOffset:endOffset+1],end="=>")
    #                print(new_s,new_e,end="=>")
                    print(txt_content[new_s:new_e])
            if(len(items)>1):
                combinatations.append(items)
#        break
#            print(items)
#            input()
       