# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 07:27:56 2017

@author: Shanika Ediriweera
"""

from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
import math

import similarity_calulator
import clustering_evaluator
from kmedoids import kmedoids

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

# 3 points in dataset
#data = np.array([[1,1], 
#                [2,2], 
#                [10,10]])

# distance matrix
#D1 = pairwise_distances(data, metric='euclidean')

D = similarity_calulator.get_distance_matrix()

# split into clusters
no_of_phrases = similarity_calulator.get_no_of_phrases()
#M, C = kmedoids.kMedoids(D, 2)
#M, C = kmedoids.kMedoids(D, int(math.sqrt(similarity_calulator.get_no_of_phrases())))
M, C = kmedoids.kMedoids(D, int(math.sqrt(no_of_phrases))+3)

print('medoids:')
for point_idx in M:
    print( phrases[point_idx] )

print('')
print('clustering result:')
for label in C:
    for point_idx in C[label]:
        print('label {0}:　{1}'.format(label, phrases[point_idx]))
       
# create a list of labels
labels = [None] * no_of_phrases
for label in C:
    for point_idx in C[label]:
        labels[point_idx] = label
# get silhoutte_coeff_score 
silhoutte_coeff_score = clustering_evaluator.get_silhoutte_coefficient(D, labels)

print("silhoutte_coeff_score : ",silhoutte_coeff_score)