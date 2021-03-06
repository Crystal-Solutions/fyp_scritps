# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 14:14:18 2017

@author: Shanika Ediriweera
"""
import nltk
import string
import numpy as np
import gensim
#import os

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

GENSIM_W2V_MODEL = './models/model.bin'

#extracted phrases list - example
phrases = ["Lectures", "you", "lecturer explains most of the concepts using examples",
           "what's on the board", "board", "lectures", "All the 7 lectures", "content",
           "The way of described the oop concepts", "practical examples that used to explain concepts",
           "exercises which were done during the lecture time", "teaching style", "lectures",
           "Examples", "in class activities (writing programms)", "lectures", "first 7 lectures",
           "Teaching", "lectures", "giving time to think for an answer", "basic OOP concepts",
           "polymorphism", "lecture session", "lectures", "lectures", "lecture series", 
           "lots of things", "a lot", "OOP", "Java", "Practicing codes in the class", "It",
           "teaching style", "everything", "Coding demonstrations", "lectures", "teaching method",
           "Discussing a question using java everyday", "lectures", "lecturer's teaching method",
           "They", "fundamental concepts of oop", "basic principals of java", "concepts",
           "lecture slides", "in class activities", "Recap segment", "oop", "slides", "inclass test",
           "explanations", "lectures", "game", "It", "content", "OOP concepts with examples", 
           "In class exercises", "Homework given every day", "lecturer", "lot of new things",
           "In class activities", "lectures", "current way of teaching"]


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens:
        stems.append(PorterStemmer().stem(item))
    return stems


def get_similarity_matrix(phrases):
    token_list = []
    for item in phrases:
        token_list.append(item.lower().translate(str.maketrans('','',string.punctuation)))
    
#    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    tfidf = TfidfVectorizer(tokenizer=tokenize)
    tfs = tfidf.fit_transform(token_list)
    sim_mat = (tfs * tfs.T).A
#    print(sim_mat)
    return sim_mat

def get_w2v_similarity_matrix(phrases):
    model = gensim.models.Word2Vec.load(GENSIM_W2V_MODEL) 
    token_list = []
    for item in phrases:
#        token_list.append(item.lower().translate(str.maketrans('','',string.punctuation)))
        item = item.replace(",", " ")
        token_list.append(item.lower())

    sim_mat = []
    for w1 in token_list:
        sim_mat_w1 = []
        for w2 in token_list:
            sim_mat_w1.append(model.n_similarity(w1.split(),w2.split()))
        sim_mat.append(sim_mat_w1)
    return sim_mat

def get_distance_matrix(phrases):
    sim_mat = get_similarity_matrix(phrases)
    dist_arr = [[(1-y) for y in x] for x in sim_mat]
    dist_mat = np.asmatrix(dist_arr)
    return dist_mat

def get_w2v_distance_matrix(phrases):
    sim_mat = get_w2v_similarity_matrix(phrases)
    dist_arr = [[(1-y) for y in x] for x in sim_mat]
    dist_mat = np.asmatrix(dist_arr)
    return dist_mat

def get_no_of_phrases(phrases):
    return len(phrases)

import phrase_cluster
if __name__ == "__main__":
    
    phrases = phrase_cluster.get_phrases_from_file("./targets/annotated/feedback_cs2012_3.txt")
    sim_mat = get_similarity_matrix(phrases)
#    print("sim mat",sim_mat)
    w2v_sim_mat = get_w2v_similarity_matrix(phrases)
    print("w2w mat===========================", w2v_sim_mat)
    print("end")
    mat = get_w2v_distance_matrix(phrases)
#    print(mat)
    