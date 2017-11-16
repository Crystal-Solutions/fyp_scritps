# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 14:08:39 2017

@author: Shanika Ediriweera
"""
import os

import clustering_evaluator
from phrase_cluster import get_coref_resolved_phrases
from similarity_calulator import get_no_of_phrases
from similarity_calulator import get_similarity_matrix
from string_similarity_clustering import cluster_similar_strings

#folder to save annotated clusters - [annotated- extracted-using annotated targets]
CLUSTERS_PATH = "./clusters/annotated/" 

COREF_RESOLVED_TARGETS_PATH = "./targets/annotated-coref-resolved/" #folder which contains targets files - coref resolved

ANNOTATED_LABEL_LISTS_PATH = "./label_lists/annotated/"
STR_SIM_LABEL_LISTS_PATH = "./label_lists/string_similarity/"

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

def write_annotated_label_lists():
    for file in os.listdir(CLUSTERS_PATH):
        phrases = get_coref_resolved_phrases(COREF_RESOLVED_TARGETS_PATH+file)
        no_of_phrases = get_no_of_phrases(phrases) #no of targets
        
        # get the true clusters from the annotated clusters
        anno_clusters = clustering_evaluator.get_annotated_cluster_obj(CLUSTERS_PATH+file)
        anno_labels  = get_labels_list(anno_clusters, no_of_phrases)
        
        print(file)
        print(anno_labels)
        f = open(ANNOTATED_LABEL_LISTS_PATH+file, 'w')
        for label in anno_labels:
            f.write(str(label)+'\n')
            
def write_string_similarity_label_lists(threshold):
    for file in os.listdir(CLUSTERS_PATH):
        phrases = get_coref_resolved_phrases(COREF_RESOLVED_TARGETS_PATH+file)
        no_of_phrases = get_no_of_phrases(phrases) #no of targets
        
        S = get_similarity_matrix(phrases)
#        S = similarity_calulator.get_w2v_similarity_matrix(phrases)

        C, no_of_clusters = cluster_similar_strings(S, threshold)
        
        cluster_labels  = get_labels_list(C, no_of_phrases)
        
        print(file)
        print(cluster_labels)
        f = open(STR_SIM_LABEL_LISTS_PATH+file, 'w')
        for label in cluster_labels:
            f.write(str(label)+'\n')
            

if __name__ == "__main__":
    write_annotated_label_lists()
#    write_string_similarity_label_lists(0.3)