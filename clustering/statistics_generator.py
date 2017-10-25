# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 13:46:09 2017

@author: Shanika Ediriweera
"""

import nltk
import math
import os
import similarity_calulator
import clustering_evaluator

from kmedoids import kmedoids

TARGETS_PATH = "./targets/annotated/" #folder which contains targets files

SENTENCES_PATH = "./sents/" #folder which contains sentences files
#folder to save annotated clusters - [annotated- extracted-using annotated targets, extracted-using extracted targets]
CLUSTERS_PATH = "./clusters/annotated/" 

#annotated cluster files to take as true classes for clustering results metrics
anno_cluster_files = ['feedback_cs2012_1.txt', 'feedback_cs2012_2.txt', 'feedback_cs2012_3.txt', 'feedback_cs2012_4.txt', 'feedback_cs2012_5.txt', 'feedback_cs2012_6.txt',
                      'feedback_cs2062_1.txt', 'feedback_cs2202_1.txt', 'feedback_cs2202_2.txt', 'feedback_cs2202_3.txt', 'feedback_cs2202_4.txt', 'feedback_cs2202_6.txt', 
                      'feedback_cs2202_7.txt', 'feedback_cs2202_8.txt', 'feedback_cs2202_9.txt', 'feedback_cs2202_10.txt', 'feedback_cs2202_11.txt', 'feedback_cs2202_12.txt']


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

def get_all_targets():
    #not used
    all_phrases = []
    for filename in os.listdir(TARGETS_PATH):
        file = os.path.join(TARGETS_PATH, filename)
        phrases = get_phrases_from_file(file)
        for target in phrases:
            all_phrases.append(target)          
    print(all_phrases)
    print("no of targets",len(all_phrases))
    all_phrases = sorted(all_phrases)
    scores_file = open("all_targets.txt", 'w')
    for target in all_phrases:
        scores_file.write(target+"\n")
    scores_file.close()
#    no_of_phrases = similarity_calulator.get_no_of_phrases(all_phrases) #no of targets

    return all_phrases

def get_all_sents():
    #not used
    all_sents = []
    for filename in os.listdir(SENTENCES_PATH):
        file = os.path.join(SENTENCES_PATH, filename)
        print(filename)
        with open(file) as f:
            content = f.read()  
            sents = nltk.sent_tokenize(content)
        print(len(sents))
        for sent in sents:
            all_sents.append(sent)          
#    print(all_sents)
    print("no of sents",len(all_sents))

    sents_file = open("all_sents.txt", 'w')
    for sent in all_sents:
        sents_file.write(sent+"\n")
    sents_file.close()

    return all_sents

def get_avg_no_of_clusters():
    no_of_clusters_arr = []
    total_no_of_clusters = 0
    no_of_files = 0
    for filename in os.listdir(CLUSTERS_PATH):
#        print(os.path.join(TARGETS_PATH, filename))
        anno_clusters = clustering_evaluator.get_annotated_cluster_obj(CLUSTERS_PATH+filename)
        no_of_clusters= len(anno_clusters)
        no_of_clusters_arr.append(no_of_clusters)
        print("no_of_clusters", no_of_clusters)
#        anno_labels  = get_labels_list(anno_clusters, no_of_phrases)
        no_of_files += 1
        total_no_of_clusters += no_of_clusters
        print("no_of_files",no_of_files)

    avg_no_of_clusters = total_no_of_clusters/no_of_files
    print("avg_no_of_clusters",avg_no_of_clusters)
    print(no_of_clusters_arr)
    return no_of_clusters_arr, avg_no_of_clusters

#D = similarity_calulator.get_distance_matrix(phrases) #distance matrix
#S = similarity_calulator.get_similarity_matrix(phrases)
#D = similarity_calulator.get_w2v_distance_matrix(phrases) #distance matrix
#S = similarity_calulator.get_w2v_similarity_matrix(phrases)
#no_of_phrases = similarity_calulator.get_no_of_phrases(phrases) #no of targets
#M, C = cluster_kmedoids(no_of_phrases, D) # cluster using kmedoids algorithm
#cluster_labels = get_labels_list(C, no_of_phrases)

if __name__ == "__main__":
#    no_of_clusters_arr, avg_no_of_clusters = get_avg_no_of_clusters()
#    targets = get_all_targets()
    
    sents = get_all_sents()
    
#    target_set = set(targets)
#    target_set = sorted(target_set)
#    
#    targets_set_file = open("targets_set.txt", 'w')
#    for target in target_set:
#        targets_set_file.write(target+"\n")
#        print(target)
#    
#    targets_set_file.close()
    
