# -*- coding: utf-8 -*-
"""
Created on Tue May  9 18:35:21 2017
Load annotations and txt fils from ../data/annotated/ and convert them into ../data/wordlist dir
@author: Janaka
"""

#Imports
import os,nltk


#Constants
SOURCE_DIR = '../data/annotated/'
DEST_DIR = '../data/wordlist'


def spans_words(txt,tokens,base_offset):
    offset = 0
    for token in tokens:
        offset = txt.find(token, offset)
        yield token, base_offset+offset, base_offset+offset+len(token)
        offset += len(token)
    

def spans_sentences(txt,base_offset):
    tokens=nltk.sent_tokenize(txt)
    offset = 0
    for token in tokens:
        offset = txt.find(token, offset)
        yield token, base_offset+offset, base_offset+offset+len(token)
        offset += len(token)


def get_tagged_word_tokens(txt,annText, tagList=[],):
    
    sents = [sent for sent in spans_words(txt,nltk.sent_tokenize(txt),0)]
    
    tokens = [
            [[token] for token in spans_words(sent[0],nltk.word_tokenize(sent[0]),sent[1])] for sent in sents]
    print(len(txt))
    anns = [line.split() for line in annText.split('\n')]
    for a in anns:
        if len(a)>4 and a[0][0]=='T' and a[1] in tagList:
            s,e = int(a[2]),int(a[3])
            for sent in tokens:
                for tok in sent:
                    token_start = tok[0][1]
                    if token_start>=s and token_start<=e:
                        tok.append(a[0])
                        
    return tokens

#print([ a for a in spans_words("Hi, I have no idea what to say.",0)])


#Iterate through files
for file in os.listdir(SOURCE_DIR):
    if file.endswith(".txt"):
        txt_file_path = os.path.join(SOURCE_DIR, file)
        f = open(txt_file_path)
        txt = f.read().replace('\n','\n\n')
        
        ann_file_path = os.path.join(SOURCE_DIR, file[:-3]+'ann')
        f = open(ann_file_path)
        ann = f.read()
        result = get_tagged_word_tokens(txt,ann,['PositiveTarget','NegativeTarget','Target'])
        break