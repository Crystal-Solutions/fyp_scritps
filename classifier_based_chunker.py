# -*- coding: utf-8 -*-
"""
Created on Wed May  3 09:15:20 2017

@author: Shanika Ediriweera
"""
import nltk, re, pprint
from nltk.corpus import conll2000

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
        tagged_sents = [[((w,t),c) for (w,t,c) in
                         nltk.chunk.tree2conlltags(sent)]
                        for sent in train_sents]
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
            "word": word,
            "prevpos": prevpos,
            "nextpos": nextpos, 
            "prevpos+pos": "%s+%s" % (prevpos, pos),
            "pos+nextpos": "%s+%s" % (pos, nextpos),
            "tags-since-dt": tags_since_dt(sentence, i)}
    
def tags_since_dt(sentence, i):
    tags = set()
    for word, pos in sentence[:i]:
        if pos == 'DT':
            tags = set()
        else:
            tags.add(pos)
    return '+'.join(sorted(tags))

test_sents = conll2000.chunked_sents('targets_test.txt', chunk_types=['T'])
train_sents = conll2000.chunked_sents('targets_train.txt', chunk_types=['T'])
#print(train_sents)
result_sents = [[(w,t) for (w,t,c) in
                         nltk.chunk.tree2conlltags(sent)]
                        for sent in train_sents]
result_sents = [[nltk.tag.untag(i) for i in s] for s in result_sents]
chunker = ConsecutiveNPChunker(train_sents)
#print(chunker.evaluate(test_sents))
results = chunker.parse_all(result_sents)
