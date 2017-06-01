# -*- coding: utf-8 -*-
"""
Created on Mon May 29 14:18:17 2017

@author: Shanika Ediriweera
"""

#Imports
import os
from nltk.tokenize import sent_tokenize

from senna_tagging import add_space_between_sentences, add_space_between_sentence_and_period, save_preprocessed_data
from spell_corrector import create_request_texts_sents, create_request_texts_resps, spell_correct, save_spell_corrected_data

#Constants
SOURCE_DIR = '../../data/annotated/'
DIR_SENT_SPACE_ADDED = '../../data/preprocessed/sent_space_added/'
DIR_SPELL_CORRECTED_SENTS = '../../data/preprocessed/spell_corrected_sents/'
DIR_SPELL_CORRECTED_RESPS = '../../data/preprocessed/spell_corrected_resps/'
DIR_SPACE_ADDED_BEFORE_PERIOD_SENTS = '../../data/preprocessed/space_added_before_period_sents/'
DIR_SPACE_ADDED_BEFORE_PERIOD_RESPS = '../../data/preprocessed/space_added_before_period_resps/'
#DIR_COREFERENCE_RESOLVED_SENTS = '../../data/preprocessed/coreference_resolved_sents/'
#DIR_COREFERENCE_RESOLVED_RESPS = '../../data/preprocessed/coreference_resolved_resps/'


def preprocess():
    api_calls_file = open("api_calls.txt","a+")
    api_calls_file.write("new")
    api_calls_file.close()
    
    #Iterate through files - preprocessing
    for file in os.listdir(SOURCE_DIR):
        if file.endswith(".txt"):
            print("Preprocessing:"+file, end='\t')
            
            #opening source file
            txt_file_path = os.path.join(SOURCE_DIR, file)
            f = open(txt_file_path)
            text = f.read()
            f.close()
            
            #sentence space adding
            sent_space_added_text = add_space_between_sentences(text)
            sent_space_added_file = open(DIR_SENT_SPACE_ADDED+file, "w+")
            sent_space_added_file.write(sent_space_added_text)
            sent_space_added_file.close()
            
            #Spell correcting
            #responses
            requests = create_request_texts_resps(sent_space_added_text)
            spell_corrected_text_resps = spell_correct(requests)
            save_spell_corrected_data(spell_corrected_text_resps, DIR_SPELL_CORRECTED_RESPS, file)
            
            #sentences
            #might not need this - can use spell corrected responses for next step
            sents_separated_text = ""
            sentences = sent_tokenize(sent_space_added_text)
            for sentence in sentences:
                sents_separated_text += sentence + "\n"
            requests = create_request_texts_sents(sents_separated_text)
            spell_corrected_text_sents = spell_correct(requests)
            save_spell_corrected_data(spell_corrected_text_sents, DIR_SPELL_CORRECTED_SENTS, file)
            
            #space adding between sentences and period
            #sentences
            space_added_before_period_sents = ""
            sentences = sent_tokenize(spell_corrected_text_sents)
            for sentence in sentences:
                space_added_before_period_sents += add_space_between_sentence_and_period(sentence, "single") + "\n"
            space_added_before_period_sents_file = open(DIR_SPACE_ADDED_BEFORE_PERIOD_SENTS+file, "w")
            space_added_before_period_sents_file.write(space_added_before_period_sents)
            space_added_before_period_sents_file.close()
            
            #responses
            space_added_before_period_resps = add_space_between_sentence_and_period(spell_corrected_text_resps, "multiple")
            space_added_before_period_resps_file = open(DIR_SPACE_ADDED_BEFORE_PERIOD_RESPS+file, "w")
            space_added_before_period_resps_file.write(space_added_before_period_resps)
            space_added_before_period_resps_file.close()
    
def process_after_spell_correction():
    for file in os.listdir(SOURCE_DIR):
        if file.endswith(".txt"):
            print("Preprocessing:"+file, end='\t')
            
            #sentences
            sents_file = open(DIR_SPELL_CORRECTED_SENTS+file)
            spell_corrected_text_sents = sents_file.read()
            sents_file.close()
            space_added_before_period_sents = ""
            sentences = sent_tokenize(spell_corrected_text_sents)
            for sentence in sentences:
                space_added_before_period_sents += add_space_between_sentence_and_period(sentence, "single") + "\n"
            space_added_before_period_sents_file = open(DIR_SPACE_ADDED_BEFORE_PERIOD_SENTS+file, "w")
            space_added_before_period_sents_file.write(space_added_before_period_sents)
            space_added_before_period_sents_file.close()
            
            #responses
            resps_file = open(DIR_SPELL_CORRECTED_RESPS+file)
            spell_corrected_text_resps = resps_file.read()
            resps_file.close()
            space_added_before_period_resps = add_space_between_sentence_and_period(spell_corrected_text_resps, "multiple")
            space_added_before_period_resps_file = open(DIR_SPACE_ADDED_BEFORE_PERIOD_RESPS+file, "w")
            space_added_before_period_resps_file.write(space_added_before_period_resps)
            space_added_before_period_resps_file.close()

#process_after_spell_correction
#add_empty_line_between_responses
def add_empty_line_between_responses():
    for file in os.listdir(SOURCE_DIR):
        if file.endswith(".txt"):
            print("Processing:"+file, end='\t')
            
            resps_file = open(DIR_SPELL_CORRECTED_RESPS+file)
            spell_corrected_text = resps_file.read()
            resps_file.close()
            space_added_before_period_sents = ""
            responses = spell_corrected_text.split('\n')
            for response in responses:
                sentences = sent_tokenize(response)
                for sentence in sentences:
                    space_added_before_period_sents += add_space_between_sentence_and_period(sentence, "single") + "\n"
                space_added_before_period_sents += "\n"
            space_added_before_period_sents_file = open(DIR_SPACE_ADDED_BEFORE_PERIOD_SENTS+file, "w")
            space_added_before_period_sents_file.write(space_added_before_period_sents)
            space_added_before_period_sents_file.close()
    
if __name__ == '__main__':
    #preprocess()
    #process_after_spell_correction()
    add_empty_line_between_responses()
