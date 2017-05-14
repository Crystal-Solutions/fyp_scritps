# -*- coding: utf-8 -*-
"""
Created on Sat May 13 18:51:42 2017

@author: Shanika Ediriweera
"""
#Imports
import os, nltk
import re
from nltk.tag import SennaTagger, SennaChunkTagger
from nltk.tokenize import sent_tokenize

#Constants
SOURCE_DIR = '../data/annotated/'
SENNA_INPUT_DIR = '../data/senna_input/'
SENNA_EXECUTABLE_DIR = '../../tools/senna'

pos_tagger = SennaTagger(SENNA_EXECUTABLE_DIR)
chunk_tagger = SennaChunkTagger(SENNA_EXECUTABLE_DIR)


def add_space_between_sentences(text):
    """
    Add space between sentences where no space is added after period
    """
    space_added_txt = re.sub(r"(\w+)\.(\w+)",r"\1. \2",text)
    return space_added_txt


def add_space_between_sentence_and_period(text, text_type):
    """
    Add space between sentence and period.
    This is needed for SENNA to tokenize sentences.
    text_type:  "single" for single sentence, 
                "multiple" for multiple newline seperated responses
    """
    if text_type == "single":
        counter = 1
        while(counter < len(text) and text[-counter] == ' '):
            counter += 1
        if counter >= len(text): return
        elif text[-counter] == '.':
            return text[:-counter] + " ."    
        else:
            return text[:-counter] + text[-counter] + " ."    
        
    elif text_type == "multiple":
        return re.sub(r"\.(\n+)",r" .\1",text)

    
def preprocess(text, text_type):
    """
    Preprocess for SENNA.
    text_type:  "single" for feeding sentence by sentence, 
                "multiple" for multiple newline seperated responses
    """
    space_added_txt = add_space_between_sentences(text)
    if text_type == "single":
        preprocessed_text = ""
        sentences = sent_tokenize(space_added_txt)
        for sentence in sentences:
            preprocessed_text += add_space_between_sentence_and_period(sentence, text_type) + "\n"
        return preprocessed_text
    elif text_type == "multiple":
        return add_space_between_sentence_and_period(space_added_txt, text_type)
    else:
        print("Invalid text type. text_type: \"single\" for single sentence, \"multiple\" for multiple newline seperated responses")
    
    ''''
#Iterate through files
for file in os.listdir(SOURCE_DIR):
    if file.endswith(".txt"):
        print("Processing:"+file, end='\t')
        txt_file_path = os.path.join(SOURCE_DIR, file)
        f = open(txt_file_path)
        #txt = f.read().replace('\n','\n\n')
        txt = f.read()
'''
f = open("feedback_cs2202_1.txt")
#txt = f.read().replace('\n','\n\n')
txt = f.read()
#a=preprocess(txt, "single")
#print(preprocess(txt, "single"))
a=add_space_between_sentences(txt)
q= sent_tokenize(a)
print(q)
z=chunk_tagger.tag(q)
print(z)