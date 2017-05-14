# -*- coding: utf-8 -*-
"""
Created on Tue May  9 18:35:21 2017
Load annotations and txt fils from ../data/annotated/ and convert them into ../data/wordlist dir
@author: Janaka
"""

#Imports
import os,nltk
import re
from nltk.tag import StanfordPOSTagger
from nltk.corpus import stopwords

stPosTagger = StanfordPOSTagger('english-bidirectional-distsim.tagger') 

total_sents = 0

#Constants
SOURCE_DIR = '../data/annotated/'
DEST_DIR = '../data/wordlist/'
DEST_DIR_PITTS = '../data/wordlist_pitts/'

#important phrases array (can replace 'is_in_prompt' feature of pittsburgh research)
IMP_PHRASES = []

#nltk stopwords TODO: get stanford stopwords
stop_words = set(stopwords.words('english'))

def spans_words(txt,base_offset):
    tokens = nltk.pos_tag(nltk.word_tokenize(txt))
    offset = 0
    for token in tokens:
        offset = txt.find(token[0], offset)
        yield token, base_offset+offset, base_offset+offset+len(token[0])
        offset += len(token[0])
    

def spans_sentences(txt,base_offset):
    space_added_txt = re.sub(r"(\w+)\.(\w+)",r"\1. \2",txt)
    tokens=nltk.sent_tokenize(space_added_txt)
    offset = 0
    for token in tokens:
        offset = txt.find(token, offset)
        yield token, base_offset+offset, base_offset+offset+len(token)
        offset += len(token)


def get_tagged_word_tokens(txt,annText, tagList=[],):
    global total_sents
    sents = [sent for sent in spans_sentences(txt,0)]
    tokens = [[[token] for token in spans_words(sent[0],sent[1])] for sent in sents]
    print(len(sents))
    total_sents += len(sents)
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

def save_as_wordlist(sents,dest,fileName):
    file_path = os.path.join(dest, fileName)
    f = open(file_path, 'w')
    
    for sent in sents:
        b_added = False
        for word in sent:
            w,pos = word[0][0]
            tag = 'O'
            if len(word)>1:
                tag = 'I-T' if b_added else 'B-T'
                b_added = True
            else:
                b_added = False
                
            f.write(w+' '+pos+' '+tag+'\n')
        f.write('\n')
    f.close()


#Iterate through files
for file in os.listdir(SOURCE_DIR):
    if file.endswith(".txt"):
        print("Processing:"+file, end='\t')
        txt_file_path = os.path.join(SOURCE_DIR, file)
        f = open(txt_file_path)
        txt = f.read().replace('\n','\n\n')
        
        ann_file_path = os.path.join(SOURCE_DIR, file[:-3]+'ann')
        f = open(ann_file_path)
        ann = f.read()
        if ann == "":
            print("skiping")
            continue
        result = get_tagged_word_tokens(txt,ann,['PositiveTarget','NegativeTarget','Target'])
        save_as_wordlist(result, DEST_DIR, file)
    
    
print("Total Sentences: "+str(total_sents))
        