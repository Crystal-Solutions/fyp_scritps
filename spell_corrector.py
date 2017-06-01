# -*- coding: utf-8 -*-
"""
Created on Mon May 29 14:18:17 2017

@author: Shanika Ediriweera
"""
#Imports
import os
from nltk.tokenize import sent_tokenize

from cleaner import clean_sentence_spellcheck, clean_sentence_correct
from bing_spell_check_api import bing_spell_correct

#Constants
SOURCE_DIR_RESPS = '../data/senna_input_resps/'
SOURCE_DIR_SENTS = '../data/senna_input_sents/'
DEST_DIR_RESPS = '../data/spell_corrected_resps/'
DEST_DIR_SENTS = '../data/spell_corrected_sents/'

MAX_CHARS_PER_REQ = 8000

def create_request_texts_sents(text):
    request_texts = []
    char_count = 0
    request_text = ""
    sentences = sent_tokenize(text)
    for sentence in sentences:
        if char_count + len(sentence) >= MAX_CHARS_PER_REQ:
            request_texts.append(clean_sentence_spellcheck(request_text))
            char_count = 0
            request_text = ""
        else:
            char_count += len(sentence) + 1
        request_text += sentence + "\n"
    request_texts.append(clean_sentence_spellcheck(request_text))
    return request_texts
    

def create_request_texts_resps(text):
    request_texts = []
    sentences = text.split('\n\n')
    for sentence in sentences:
        request_texts.append(clean_sentence_spellcheck(sentence))
    return request_texts
        

def spell_correct(request_texts):
    spell_corrected_text = ""
    for request_text in request_texts:
        spell_corrected = bing_spell_correct(request_text)
        post_processed = clean_sentence_correct(spell_corrected)
        spell_corrected_text += post_processed + "\n"
    return spell_corrected_text
    

def save_spell_corrected_data(text, destination, file):
    file_path = os.path.join(destination, file)
    f = open(file_path, 'w') 
    f.write(text)
    f.close()


def run(sents_or_resps):
    if sents_or_resps == "sents":
        #Iterate through files - preprocessing
        for file in os.listdir(SOURCE_DIR_SENTS):
            if file.endswith(".txt"):
                print("Processing:"+file, end='\t')
                txt_file_path = os.path.join(SOURCE_DIR_SENTS, file)
                f = open(txt_file_path)
                txt = f.read()
                
                requests = create_request_texts_sents(txt)
                spell_corrected_text = spell_correct(requests)
                save_spell_corrected_data(spell_corrected_text, DEST_DIR_SENTS, file)
                f.close()
    elif sents_or_resps == "resps":
        #Iterate through files - preprocessing
        for file in os.listdir(SOURCE_DIR_RESPS):
            if file.endswith(".txt"):
                print("Processing:"+file, end='\t')
                txt_file_path = os.path.join(SOURCE_DIR_SENTS, file)
                f = open(txt_file_path)
                txt = f.read()
                
                requests = create_request_texts_resps(txt)
                spell_corrected_text = spell_correct(requests)
                save_spell_corrected_data(spell_corrected_text, DEST_DIR_SENTS, file)
                f.close()
    else:
        print("Invalid document type")
        return None
           
if __name__ == '__main__':
    #run("resps")
    run("sents")

