# -*- coding: utf-8 -*-
"""
Created on Mon May  8 15:19:03 2017
Reads files from /boi_pos_data and write the into
@author: Janaka
"""


SOURCE_DIR = '../boi_pos_data/'
import os
import nltk


def map_to_tagged_sentences(fileContent):
    fileContent = fileContent.strip("\n")
    return [[tuple(line.split()) for line in sentence.split("\n")] for sentence in fileContent.split("\n\n")]

    
def untag_sentences(taggedSentences):
    return [[(w,p) for (w,p,t) in sent]
                 for sent in taggedSentences]

#Tagger Model
class ConsecutiveNPChunkTagger(nltk.TaggerI): 
    def __init__(self, train_sents):
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = npchunk_features(untagged_sent, i, history) 
                train_set.append( (featureset, tag) )
                history.append(tag)
        self.classifier = nltk.MaxentClassifier.train( 
            #train_set, algorithm='megam', trace=0)
            train_set, trace=0)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)

class ConsecutiveNPChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        
        print("ab")
        tagged_sents = [[((w,p),t) for (w,p,t) in sent]
                        for sent in train_sents]
        print("cd")
        self.tagger = ConsecutiveNPChunkTagger(tagged_sents)

    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence)
        conlltags = [(w,t,c) for ((w,t),c) in tagged_sents]
        return nltk.chunk.conlltags2tree(conlltags)
    
def npchunk_features(sentence, i, history):
    word, pos = sentence[i]
    #return {"pos": pos}
    if i == 0:
        prevword, prevpos = "<START>", "<START>"
    else:
        prevword, prevpos = sentence[i-1]
    #return {"pos": pos, "word": word, "prevpos": prevpos}
    if i == len(sentence)-1:
        nextword, nextpos = "<END>", "<END>"
    else:
        nextword, nextpos = sentence[i+1]
    return {"pos": pos,
            "prevpos": prevpos,
            "nextpos": nextpos}


#File by file process
for file in os.listdir(SOURCE_DIR):
    if file.endswith(".txt"):
        filePath = os.path.join(SOURCE_DIR, file)
        print("Processing: "+filePath)
        f = open(filePath)
        taggedSentences = map_to_tagged_sentences(f.read())
        untaggedSentences = untag_sentences(taggedSentences)
        chunker = ConsecutiveNPChunker(taggedSentences)
        parsed = chunker.parse(untaggedSentences[0])
        break

print(file)