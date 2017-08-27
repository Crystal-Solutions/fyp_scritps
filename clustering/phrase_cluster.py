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

RESULTS_PATH = "./results/"
EVALUATED_RESULTS = "./evaluated/"
TARGETS_PATH = "./extracted/"

# IMPORTANT
#change the file name of the targets file to evaluate
TARGETS_FILE = "feedback_cs2012_3.txt" #eg: feedback_cs2012_2.txt

SCORES_FILE = "scores.txt"

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

# get phrases from extracted targets
def get_phrases_from_file(file_name):
    with open(file_name) as f:
        content = f.readlines()  
    phrases = [x.strip() for x in content]
    # split the lines from tab and remove the position to take the phrase
    phrases = [line.split('\t')[0] for line in phrases]
    phrases = [x.strip() for x in phrases]
    return phrases

# split into clusters using kmedoids
def cluster_kmedoids(no_of_phrases, distances):
    no_of_clusters = int(math.sqrt(no_of_phrases))+2

    M, C = kmedoids.kMedoids(distances, no_of_clusters)
    return M, C

def clustering_results(clusters, medoids=None):
    results_file = open(RESULTS_PATH+TARGETS_FILE, 'w')
    
    if medoids != None:
        print('medoids:')
        results_file.write('medoids:\n')
        for point_idx in medoids:
            print( phrases[point_idx] )
            results_file.write( phrases[point_idx]+'\n' )
            
    print('')
    results_file.write('\n')
    print('clustering result:')
    results_file.write('clustering result:\n')
    for label in clusters:
        for point_idx in clusters[label]:
            print('cluster {0}:　{1}'.format(label, phrases[point_idx]))
            results_file.write('cluster '+str(label)+': '+phrases[point_idx]+'\n')
            
    results_file.close()

# create a list of labels
def get_labels_list(clusters, no_of_phrases):
    """
    returns a list of labels when the cluster object is geven
    """
    labels = [None] * no_of_phrases
    for label in clusters:
        for point_idx in clusters[label]:
            labels[point_idx] = label
    return labels



if __name__ == "__main__":
    scores_file = open(SCORES_FILE, 'a')
    scores_file.write(TARGETS_FILE+'\n')
    
    phrases = get_phrases_from_file(TARGETS_PATH+TARGETS_FILE) #read targets from file
    D = similarity_calulator.get_distance_matrix(phrases) #distance matrix
    no_of_phrases = similarity_calulator.get_no_of_phrases(phrases) #no of targets
    
    # cluster using kmedoids algorithm
    M, C = cluster_kmedoids(no_of_phrases, D)
    
    clustering_results(C, M) #print and write to a file
    
    labels = get_labels_list(C, no_of_phrases)
        
    # get silhoutte_coeff_score 
    silhoutte_coeff_score = clustering_evaluator.get_silhoutte_coefficient(D, labels)    
    print("silhoutte_coeff_score : ", silhoutte_coeff_score)
    scores_file.write("silhoutte_coeff_score : "+ str(silhoutte_coeff_score)+'\n')
    
    evaluated_clusters, evaluated_cluster_names = clustering_evaluator.manual_evaluate(phrases, D, C, M, TARGETS_FILE)
    
    print(evaluated_clusters)
    print(evaluated_cluster_names)
    
    evaluated_labels = get_labels_list(evaluated_clusters, no_of_phrases)
    ARI_score = clustering_evaluator.get_manual_eval_ARI(labels, evaluated_labels)
    print("ARI_score : ", ARI_score)
    scores_file.write("ARI_score : "+ str(ARI_score)+'\n\n')
    
    scores_file.close()
  