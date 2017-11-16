# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 07:27:56 2017

@author: Shanika Ediriweera
"""

from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
import math
import os

import similarity_calulator
import clustering_evaluator
from kmedoids import kmedoids
import string_similarity_clustering

TARGETS_PATH = "./targets/annotated/" #folder which contains targets files
COREF_RESOLVED_TARGETS_PATH = "./targets/annotated-coref-resolved/" #folder which contains targets files - coref resolved

#folder to save annotated clusters - [annotated- extracted-using annotated targets]
CLUSTERS_PATH = "./clusters/annotated/" 

# IMPORTANT
#change the file name of the targets file to annotate
TARGETS_FILE = "feedback_cs2012_3.txt" #eg: feedback_cs2012_2.txt

# file to save clustering results accuracy metrics
SCORES_FILE = "scores.txt"

#annotated cluster files to take as true classes for clustering results metrics
anno_cluster_files = ['feedback_cs2012_1.txt', 'feedback_cs2012_2.txt', 'feedback_cs2012_3.txt', 'feedback_cs2012_4.txt', 'feedback_cs2012_5.txt', 'feedback_cs2012_6.txt',
                      'feedback_cs2062_1.txt', 'feedback_cs2202_1.txt', 'feedback_cs2202_2.txt', 'feedback_cs2202_3.txt', 'feedback_cs2202_4.txt', 'feedback_cs2202_6.txt', 
                      'feedback_cs2202_7.txt', 'feedback_cs2202_8.txt', 'feedback_cs2202_9.txt', 'feedback_cs2202_10.txt', 'feedback_cs2202_11.txt', 'feedback_cs2202_12.txt']

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

# get phrases from extracted targets - coref resolved
def get_coref_resolved_phrases(file_name):
    with open(file_name) as f:
        content = f.readlines() 
    phrases = [x.strip() for x in content]
    phrases = [x.rstrip('.') for x in phrases]
    phrases = [x.strip() for x in phrases]
    temp=[]
    for x in phrases:
        index = x.find('_')
        if index >= 0:
            x=x[:index]+' _ '+x[index+1:]
        temp.append(x)
    phrases = temp
    return phrases

# split into clusters using kmedoids
def cluster_kmedoids(no_of_phrases, distances):
    #TODO: take min of no of clusters and int(math.sqrt(no_of_phrases))+15
    no_of_clusters = int(math.sqrt(no_of_phrases))+5

    M, C = kmedoids.kMedoids(distances, no_of_clusters)
    return M, C, no_of_clusters

# split into clusters using string similarity
def cluster_string_similarity(similarities):
    C = string_similarity_clustering.cluster_similar_strings(similarities)
    return C

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

def get_clusters_with_phrases(clusters, phrases):
    """
    returns the clusters with phrases, replacing phrase ids
    """
    clusters_with_phrases = {}
    for label in clusters:
        clusters_with_phrases[label] = []
        for point_idx in clusters[label]:
            clusters_with_phrases[label].append(phrases[point_idx]) 
    return clusters_with_phrases

def clustering_evaluate(clustering_algo, similarity_method, coref_resolved=False, write_file=True, threshold = None):
    """
    method to run clustering algorithm and evauale results and write results to a file
    """
    if write_file==True:
        #initialization
        scores_file = open(SCORES_FILE, 'a')
        title = input("Enter brief description of clustering: ") #description for clustering
        scores_file.write('\n'+title+'\n')
    
    avg_silhoutte_coeff_score = 0
    avg_ARI_score = 0 
    avg_NMI_score = 0
    avg_AMI_score = 0
    avg_homogeneity = 0 
    avg_completeness = 0
    avg_v_measure = 0
    avg_fowlkes_mallows_score = 0
    avg_purity = 0
    
    # run file by file to cluster and evaluate and write results to a file
#    for file in anno_cluster_files:
    anno_cluster_files = []
    for file in os.listdir(CLUSTERS_PATH):
        anno_cluster_files.append(file)
        print(file)
        if write_file==True:
            scores_file.write(file+'\n')
        
        if coref_resolved:
            phrases = get_coref_resolved_phrases(COREF_RESOLVED_TARGETS_PATH+file)
        else:
            phrases = get_phrases_from_file(TARGETS_PATH+file) #read targets from file
            
#        print("phrases:",phrases)
        
        # claculate similarity
        if similarity_method == "cosine":
            D = similarity_calulator.get_distance_matrix(phrases) #distance matrix
            S = similarity_calulator.get_similarity_matrix(phrases)
        elif similarity_method == "w2v":
            D = similarity_calulator.get_w2v_distance_matrix(phrases) #distance matrix
            S = similarity_calulator.get_w2v_similarity_matrix(phrases)
#            print(S)
        
        no_of_phrases = similarity_calulator.get_no_of_phrases(phrases) #no of targets
        
        # run clustering algorithm
        if clustering_algo == "kmedoids":
            # cluster using kmedoids algorithm
            M, C, no_of_clusters = cluster_kmedoids(no_of_phrases, D)
            #clustering_results(C, M) #print and write to a file        
        elif clustering_algo == "string_sim":
            if threshold == None:
                C, no_of_clusters = string_similarity_clustering.cluster_similar_strings(S)
            else:
                C, no_of_clusters = string_similarity_clustering.cluster_similar_strings(S, threshold)
        clusters = get_clusters_with_phrases(C, phrases)
        for label in clusters:
            print("cluster "+str(label)+": "+str(clusters[label]))
        print("no_of_clusters: ",no_of_clusters)
        
        cluster_labels = get_labels_list(C, no_of_phrases)
        
        # get the true clusters from the annotated clusters
        anno_clusters = clustering_evaluator.get_annotated_cluster_obj(CLUSTERS_PATH+file)
        anno_labels  = get_labels_list(anno_clusters, no_of_phrases)
        no_of_anno_clusters = len(anno_clusters)
        print("no of annotated clusters: ", no_of_anno_clusters)
        print("diff of clusters: ",abs(no_of_clusters-no_of_anno_clusters))
           
        # evaluate clustering results and write to file
        # get silhoutte_coeff_score 
        silhoutte_coeff_score = clustering_evaluator.get_silhoutte_coefficient(D, cluster_labels)    
        avg_silhoutte_coeff_score += silhoutte_coeff_score
#        print("silhoutte_Coeff_score [-1, 1]: ", silhoutte_coeff_score)
        
        ARI_score = clustering_evaluator.get_ARI(cluster_labels, anno_labels)
        avg_ARI_score += ARI_score
#        print("ARI_score [-1, 1]: ", ARI_score)
        
        norm_score, adj_score = clustering_evaluator.get_mutual_information_score(cluster_labels, anno_labels)
        avg_NMI_score += norm_score
        avg_AMI_score += adj_score
        print("Normalized Mutual Information Score  [0, 1]: ", norm_score)
#        print("Adjusted Mutual Information Score  [0, 1]: ", adj_score)
        
        h, c, v = clustering_evaluator.get_homogeneity_completeness_v_measure(cluster_labels, anno_labels)
        avg_homogeneity += h
        avg_completeness += c
        avg_v_measure += v
#        print("homogeneity  [0, 1]: "+ str(h))
#        print("completeness  [0, 1]: "+ str(c))
        print("v_measure  [0, 1]: "+ str(v))
        
        fowlkes_mallows_score = clustering_evaluator.get_fowlkes_mallows_score(cluster_labels, anno_labels)
        avg_fowlkes_mallows_score += fowlkes_mallows_score
#        print("fowlkes_mallows_score  [0, 1]: ", fowlkes_mallows_score)
        
        purity = clustering_evaluator.get_purity(cluster_labels, anno_labels)
        avg_purity += purity
        print("purity  [0, 1]: "+ str(purity)+"\n")
        
        if write_file==True:
            scores_file.write("Silhoutte Coefficient Score [-1, 1]: "+ str(silhoutte_coeff_score)+'\n')
            scores_file.write("ARI_score [-1, 1]: "+ str(ARI_score)+'\n')
            scores_file.write("Normalized Mutual Information Score  [0, 1]: "+ str(norm_score)+'\n')
            scores_file.write("Adjusted Mutual Information Score  [0, 1]: "+ str(adj_score)+'\n')
            scores_file.write("homogeneity  [0, 1]: "+ str(h)+'\n')
            scores_file.write("completeness  [0, 1]: "+ str(c)+'\n')
            scores_file.write("v_measure  [0, 1]: "+ str(v)+'\n')
            scores_file.write("Fowlkes Mallows Score  [0, 1]: "+ str(fowlkes_mallows_score)+'\n')
            scores_file.write("Purity  [0, 1]: "+ str(purity)+'\n\n')
    
    # write average results to a file
    print("Average")
#    print("avg_silhoutte_coeff_score [-1, 1]:", avg_silhoutte_coeff_score/len(anno_cluster_files))
#    print("avg_ARI_score [-1, 1]:", avg_ARI_score/len(anno_cluster_files))
    print("avg_NMI_score  [0, 1]:", avg_NMI_score/len(anno_cluster_files))
#    print("avg_AMI_score  [0, 1]:", avg_AMI_score/len(anno_cluster_files))
#    print("avg_homogeneity  [0, 1]:", avg_homogeneity/len(anno_cluster_files))
#    print("avg_completeness  [0, 1]:", avg_completeness/len(anno_cluster_files))
    print("avg_v_measure  [0, 1]:", avg_v_measure/len(anno_cluster_files))
#    print("avg_fowlkes_mallows_score  [0, 1]:", avg_fowlkes_mallows_score/len(anno_cluster_files))
    print("avg_purity  [0, 1]:", avg_purity/len(anno_cluster_files))
    if write_file==True:
        scores_file.write("Average - "+title+"\n")
        scores_file.write("avg_silhoutte_coeff_score [-1, 1]:"+ str(avg_silhoutte_coeff_score/len(anno_cluster_files)))
        scores_file.write("\navg_ARI_score [-1, 1]:"+ str(avg_ARI_score/len(anno_cluster_files)))
        scores_file.write("\navg_NMI_score  [0, 1]:"+ str(avg_NMI_score/len(anno_cluster_files)))
        scores_file.write("\navg_AMI_score  [0, 1]:"+ str(avg_AMI_score/len(anno_cluster_files)))
        scores_file.write("\navg_homogeneity  [0, 1]:"+ str(avg_homogeneity/len(anno_cluster_files)))
        scores_file.write("\navg_completeness  [0, 1]:"+ str(avg_completeness/len(anno_cluster_files)))
        scores_file.write("\navg_v_measure  [0, 1]:"+ str(avg_v_measure/len(anno_cluster_files)))
        scores_file.write("\navg_fowlkes_mallows_score  [0, 1]:"+ str(avg_fowlkes_mallows_score/len(anno_cluster_files)))
        scores_file.write("\navg_purity  [0, 1]:"+ str(avg_purity/len(anno_cluster_files)))
        scores_file.close()
 
'''
    #test cluster with phrases
    S = similarity_calulator.get_similarity_matrix(phrases)
    C, no_of_clusters = string_similarity_clustering.cluster_similar_strings(S, 0.3)
    
    clus = get_clusters_with_phrases(C, phrases)
    for label in clus:
        print("cluster "+str(label)+": "+str(clus[label]))
    print("no_of_clusters:",no_of_clusters)
'''
       
if __name__ == "__main__":
#    clustering_evaluate("kmedoids", "cosine", False, False)
#    clustering_evaluate("kmedoids", "w2v", False, False)
#    clustering_evaluate("string_sim", "cosine", False, False, 0.3)
#    clustering_evaluate("string_sim", "cosine", False, False, 0.4)
#    clustering_evaluate("string_sim", "cosine", False, False, 0.5)
#    clustering_evaluate("string_sim", "w2v", False, False, 0.999)

    # coresolution resolved
#    clustering_evaluate("kmedoids", "cosine", True, False)
#    clustering_evaluate("kmedoids", "w2v", True, False)
#    clustering_evaluate("string_sim", "cosine", True, False, 0.3)
#    clustering_evaluate("string_sim", "cosine", True, False, 0.4)
    clustering_evaluate("string_sim", "cosine", True, False, 0.3)
#    clustering_evaluate("string_sim", "w2v", True, False)