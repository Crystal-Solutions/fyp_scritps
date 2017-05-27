# -*- coding: utf-8 -*-
"""
Created on Sun May 14 16:58:02 2017

@author: Janaka
"""
#Imports
import os,nltk
import re
from nltk.tag import StanfordPOSTagger
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
#from word_to_vec import model as w2v_model

stPosTagger = StanfordPOSTagger('english-bidirectional-distsim.tagger') 
total_sents = 0
stopWords = set(stopwords.words('english'))
stemmer = PorterStemmer()
promptWords = ['lectures', 'how']


#Constants
ANN_DIR = '../data/annotated/'
SRC_DIR = '../data/senna_output/'
DEST_DIR = '../data/senna_output_tagged_with_word2vec/'

def spans_tokens(txt,tokens):
    offset = 0
    for token in tokens:
        if(len(token)==0):
            yield [], offset, offset
            continue
        offset = txt.find(token[0], offset)
        yield token, offset, offset+len(token[0])
        offset += len(token[0])


def tag(senna_txt, txt, ann,tagList):
    lines = [tuple(l.strip().split()) for l in senna_txt.split("\n")]
    tokens = [list(i) for i in spans_tokens(txt,lines)]
    
    #Prepare word list and their coun and rank
    wordList = []
    for line in tokens:
        if len(line[0])>0:
            wordList.append(stemmer.stem(line[0][0].lower()))
    wordSet = set(wordList)
    wordCounts = {}
    wordRanks = {}
    for w in wordSet:
        wordCounts[w] = wordList.count(w)
    rank = 1
    last_count = 0
    for key, value in [(k, wordCounts[k]) for k in sorted(wordCounts, key=wordCounts.get, reverse=True)]:
        wordRanks[key] = rank
        if(value!=last_count):
            rank+=1
            last_count = value

    #adding tags for prompt, stopword, word Count, word rank and 
    for line in tokens:
#        print(line)
        if(len(line[0])==0):
            line.append('Y')
            line.append('N')
            line.append(0)
            line.append(0)
            line.append([])
            continue
        w = line[0][0].lower()
        stem_w = stemmer.stem(w)
        line.append('Y' if w in stopWords else 'N')
        line.append('Y' if w in promptWords else 'N')
        line.append(wordCounts[stem_w])
        line.append(wordRanks[stem_w])
        line.append([])
    
    #add annotation tags
    anns = [line.split() for line in ann.split('\n')]
    for a in anns:
        if len(a)>4 and a[0][0]=='T' and a[1] in tagList:
            s,e = int(a[2]),int(a[3])
            for tok in tokens:
#                print(tok)
                token_start = tok[1]
                if token_start>=s and token_start<=e:
                    tok[-1].append(a[0])
                    
    return tokens

missing_words = set();
def get_wc_tags(word):
    
    if word in w2v_model:
        vec = w2v_model[word]
    else:
        vec = [0]*300
        missing_words.add(word)
        
    txt = ""
    for i in vec:
        txt+=str(i)+" "
    return txt

#save method save them to a file
def save_as_wordlist(tokens,dest,fileName):
    file_path = os.path.join(dest, fileName)
    f = open(file_path, 'w')
    
    b_added = False
    for tok in tokens:
        if(len(tok[0])>0):
            w,pos,chunk = tok[0][0],tok[0][1],tok[0][2]
            
            tag = 'O'
            if len(tok[-1])>=1:
                tag = 'I' if b_added else 'B'
                b_added = True
            else:
                b_added = False
            
            f.write(w+' '+pos+' '+chunk+' '+tok[3]+' '+tok[4]+' '+str(tok[5])+' '+str(tok[6])+' '+get_wc_tags(w)+tag+'\n')
        else:
            f.write("\n")
    f.close()



#process file by file
for file in os.listdir(ANN_DIR):
    if file.endswith(".txt"):
        print("Processing:"+file, end='\n')
        txt_file_path = os.path.join(ANN_DIR, file)
        f = open(txt_file_path)
        txt = f.read().replace('\n','\n\n')
        
        ann_file_path = os.path.join(ANN_DIR, file[:-3]+'ann')
        f = open(ann_file_path)
        ann = f.read()
        if ann == "":
            print("skiping")
            continue
        
        senna_file_path = os.path.join(SRC_DIR, file[:-3]+'txt.out')
        f = open(senna_file_path)
        senna = f.read()
        
        result = tag(senna,txt, ann,['PositiveTarget','NegativeTarget','Target'])
        save_as_wordlist(result, DEST_DIR, file)
#        break