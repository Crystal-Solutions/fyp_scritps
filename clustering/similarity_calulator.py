# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 14:14:18 2017

@author: Shanika Ediriweera
"""
import nltk
import string
import numpy as np
#import os

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

#documents = [open(f) for f in text_files]
#tfidf = TfidfVectorizer().fit_transform(documents)
# no need to normalize, since Vectorizer will return normalized tf-idf
#pairwise_similarity = tfidf * tfidf.T

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

#vect = TfidfVectorizer(min_df=1)
#tfidf = vect.fit_transform(phrases)
#a = (tfidf * tfidf.T).A
#print(a)


#path = './tf-idf'
#token_dict = {}
token_list = []


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens:
        stems.append(PorterStemmer().stem(item))
    return stems


def get_similarity_matrix():
    for item in phrases:
        token_list.append(item.lower().translate(str.maketrans('','',string.punctuation)))
    
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    tfs = tfidf.fit_transform(token_list)
    sim_mat = (tfs * tfs.T).A
#    print(sim_mat)
    return sim_mat

def get_distance_matrix():
    sim_mat = get_similarity_matrix()
    dist_arr = [[(1-y) for y in x] for x in sim_mat]
    dist_mat = np.asmatrix(dist_arr)
#    print(dist_mat)
    return dist_mat

def get_no_of_phrases():
    return len(phrases)

if __name__ == "__main__":
    sim_mat = get_similarity_matrix()
    print(sim_mat)
    mat = get_distance_matrix()
    print(mat)
    
#for dirpath, dirs, files in os.walk(path):
#    for f in files:
#        fname = os.path.join(dirpath, f)
#        print("fname=", fname)
#        with open(fname) as pearl:
#            text = pearl.read()
#            token_dict[f] = text.lower().translate(None, string.punctuation)

#tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
#tfs = tfidf.fit_transform(token_dict.values())

#str = 'all great and precious things are lonely.'
#response = tfidf.transform([str])
#print(response)
#
#feature_names = tfidf.get_feature_names()
#for col in response.nonzero()[1]:
#    print(feature_names[col], ' - ', response[0, col])