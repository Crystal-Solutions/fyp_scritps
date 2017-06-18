# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 17:58:25 2017

@author: Janaka
"""
import os
from sklearn import svm
SRC_DIR = '../data/senna_output_tagged/all/cross/'
DEST_DIR = '../data/senna_output_tagged/all/svm_output/'

def getSentsAndLabels(txt):
    org_sents = txt.split('\n\n')
    sents = []
    labels = []
    for org_sent in org_sents:
        sent = []
        hasTarget = 0
        for line in org_sent.split('\n'):
            tokens = line.strip().split();
            sent.append((tokens[0],tokens[-3],tokens[-2],tokens[-1]))
            if(tokens[-1]=='B'):
                hasTarget = 1
        sents.append((sent))
        labels.append(hasTarget)
    return sents,labels

def getWordList(data):
    word_set = set()
    for sents,labels in train_data:
        for sent in sents:
            for line in sent:
                word_set.add(line[0].lower())
    return list(word_set)

def getFeatures(wordList, sents):
    features = []
    for sent in sents:
        sent_features = []
        for w in wordList:
            count = len(list(filter(lambda tok:tok[0].lower()==w,sent)))
            sent_features.append(count)
        features.append(sent_features)
    return features


def savePredictions(i, labels):
    file = os.path.join(DEST_DIR,"out%d.txt"%i)
    f = open(file,'w')
    for l in labels:
        f.write(str(l))
        f.write('\n')
    f.close()
    
    

train_data = []
test_data = []

for file in os.listdir(SRC_DIR):
    if file.startswith("train"):
        train_fp = os.path.join(SRC_DIR, file)
        test_fp = os.path.join(SRC_DIR, 'test'+file[5:])
        train_content = open(train_fp).read()
        test_content = open(test_fp).read()
        
        train_sents_labels = getSentsAndLabels(train_content)
        test_sents_labels = getSentsAndLabels(test_content)
        
        train_data.append(train_sents_labels)
        test_data.append(test_sents_labels)
#        break;
#        print(test_fp,train_fp)

word_list = getWordList(test_data)# 


print(len(word_list))

sums = [0,0,0,0]
count = 0
errors = []
for i,((tr_sents,tr_labels),(ts_sents,ts_labels)) in enumerate(zip(train_data,test_data)):

    print(i, "______________________________",len(ts_labels))
    
    #Extract features for training
    tr_features = getFeatures(word_list,tr_sents)
    
    #Train Model
    clf = svm.SVC(kernel='linear')
    clf.fit(tr_features, tr_labels)
    
    #Extract Features for testing
    ts_features = getFeatures(word_list,ts_sents)
    ts_pridict_labels = clf.predict(ts_features)
    
    #Save predicted values
    savePredictions(i,ts_pridict_labels)
    
    tp,tn,t,p = 0,0,0,0
    for j,(tag,pred) in enumerate(zip(ts_labels, ts_pridict_labels)):
        if(tag==pred==0):
            tn+=1
        if(tag==pred==1):
            tp += 1
        if(tag==1):
            t+=1
        if(pred==1):
            p+=1
        if(tag!=pred):
            errors.append((tag,pred,ts_sents[j]))
    print("tp=%d, pred=%d, original=%d, total_sents=%d"%(tp,p,t,len(ts_labels)))
    pres = tp/p
    rec = tp/t
    f = 2*pres*rec/(pres+rec)
    acc = (tp+tn)/len(ts_labels)
    sums[0]+=pres
    sums[1]+=rec
    sums[2]+=f
    sums[3]+=acc
    
    count+=1
    print(pres,rec,f,acc)
    
    
#    break
for i in range(len(sums)):
    sums[i] = sums[i]/count
print("Average")
print("%1.5f\t%1.5f\t%1.5f\t%1.5f"%tuple(sums))