# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 14:08:39 2017

@author: Shanika Ediriweera
"""
import os

import clustering_evaluator
from phrase_cluster import get_coref_resolved_phrases
from similarity_calulator import get_no_of_phrases

#folder to save annotated clusters - [annotated- extracted-using annotated targets]
CLUSTERS_PATH = "./clusters/annotated/" 

COREF_RESOLVED_TARGETS_PATH = "./targets/annotated-coref-resolved/" #folder which contains targets files - coref resolved

ANNOTATED_LABEL_LISTS_PATH = "./label_lists/annotated/"

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