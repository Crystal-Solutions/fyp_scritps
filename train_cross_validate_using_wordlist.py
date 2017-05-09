# -*- coding: utf-8 -*-
"""
Created on Wed May 10 00:39:40 2017

@author: Janaka
"""

import os
from itertools import chain
import nltk
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import RandomizedSearchCV
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
from nltk.corpus import ConllCorpusReader


#Constants
DATA_DIR = '../data/wordlist/'


#Code for feature extraction --------------------------------------------------
def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    
    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],        
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True
        
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True
                
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]

# -----------------------------------------------------------------------------



fileNames = []
for file in os.listdir(DATA_DIR):
    if file.endswith(".txt"):
        fileNames.append(file)
        

columntypes = ['words', 'pos', 'chunk']
reader = ConllCorpusReader(root=DATA_DIR, fileids=fileNames, columntypes=columntypes,)


for name in fileNames:
    trainFiles = fileNames[:]
    trainFiles.remove(name)
    train_sents = []
    for file in trainFiles:
        s = reader.iob_sents(file)
        train_sents+=s
#        print(len(s))
        
    test_sents = reader.iob_sents(name)
    print("train_sentence_count="+str(len(train_sents)))
    print("test_sentence_count="+str(len(test_sents)))
    
    #data to train
    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]
    
    X_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]
    
    #Train
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs', 
        c1=0.1, 
        c2=0.1, 
        max_iterations=100, 
        all_possible_transitions=True
    )
    crf.fit(X_train, y_train)
    
    
    #Evaluate
    labels = list(crf.classes_)
#    labels.remove('O')
    print(labels)
    
    y_pred = crf.predict(X_test)
    print(metrics.flat_f1_score(y_test, y_pred, 
                          average='weighted', labels=labels))
    
    sorted_labels = sorted(
        labels, 
        key=lambda name: (name[1:], name[0])
    )
    print(metrics.flat_classification_report(
        y_test, y_pred, labels=sorted_labels, digits=3
    ))
    

