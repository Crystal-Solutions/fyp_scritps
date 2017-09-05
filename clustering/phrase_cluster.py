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
TARGETS_PATH = "./targets/annotated/"
CLUSTERS_PATH = "./clusters/annotated/"

# IMPORTANT
#change the file name of the targets file to evaluate
TARGETS_FILE = "feedback_cs2012_3.txt" #eg: feedback_cs2012_2.txt

SCORES_FILE = "scores.txt"

anno_cluster_files = ['feedback_cs2012_3.txt', 'feedback_cs2012_5.txt',
                              'feedback_cs2202_1.txt', 'feedback_cs2202_7.txt', 'feedback_cs2202_10.txt']

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

def clustering_evaluate():
    scores_file = open(SCORES_FILE, 'a')
    
    avg_silhoutte_coeff_score = 0
    avg_ARI_score = 0 
    avg_NMI_score = 0
    avg_AMI_score = 0
    avg_homogeneity = 0 
    avg_completeness = 0
    avg_v_measure = 0
    avg_fowlkes_mallows_score = 0
    avg_purity = 0
    for file in anno_cluster_files:
        print(file)
        scores_file.write(file+'\n')
        
        phrases = get_phrases_from_file(TARGETS_PATH+file) #read targets from file
        D = similarity_calulator.get_distance_matrix(phrases) #distance matrix
        no_of_phrases = similarity_calulator.get_no_of_phrases(phrases) #no of targets
        
        # cluster using kmedoids algorithm
        M, C = cluster_kmedoids(no_of_phrases, D)
        #clustering_results(C, M) #print and write to a file        
        cluster_labels = get_labels_list(C, no_of_phrases)
            
        # get silhoutte_coeff_score 
        silhoutte_coeff_score = clustering_evaluator.get_silhoutte_coefficient(D, cluster_labels)    
        avg_silhoutte_coeff_score += silhoutte_coeff_score
        print("silhoutte_Coeff_score : ", silhoutte_coeff_score)
        scores_file.write("Silhoutte Coefficient Score : "+ str(silhoutte_coeff_score)+'\n')
        
        anno_clusters = clustering_evaluator.get_annotated_cluster_obj(CLUSTERS_PATH+file)
        anno_labels  = get_labels_list(anno_clusters, no_of_phrases)
        
        ARI_score = clustering_evaluator.get_ARI(cluster_labels, anno_labels)
        avg_ARI_score += ARI_score
        print("ARI_score : ", ARI_score)
        scores_file.write("ARI_score : "+ str(ARI_score)+'\n')
        
        norm_score, adj_score = clustering_evaluator.get_mutual_information_score(cluster_labels, anno_labels)
        avg_NMI_score += norm_score
        avg_AMI_score += adj_score
        print("Normalized Mutual Information Score : ", norm_score)
        print("Adjusted Mutual Information Score : ", adj_score)
        scores_file.write("Normalized Mutual Information Score : "+ str(norm_score)+'\n')
        scores_file.write("Adjusted Mutual Information Score : "+ str(adj_score)+'\n')
        
        h, c, v = clustering_evaluator.get_homogeneity_completeness_v_measure(cluster_labels, anno_labels)
        avg_homogeneity += h
        avg_completeness += c
        avg_v_measure += v
        print("homogeneity : "+ str(h))
        print("completeness : "+ str(c))
        print("v_measure : "+ str(v))
        scores_file.write("homogeneity : "+ str(h)+'\n')
        scores_file.write("completeness : "+ str(c)+'\n')
        scores_file.write("v_measure : "+ str(v)+'\n')
        
        fowlkes_mallows_score = clustering_evaluator.get_fowlkes_mallows_score(cluster_labels, anno_labels)
        avg_fowlkes_mallows_score += fowlkes_mallows_score
        print("fowlkes_mallows_score : ", fowlkes_mallows_score)
        scores_file.write("Fowlkes Mallows Score : "+ str(fowlkes_mallows_score)+'\n')
        
        purity = clustering_evaluator.get_purity(cluster_labels, anno_labels)
        avg_purity += purity
        print("purity : "+ str(purity)+"\n")
        scores_file.write("Purity : "+ str(purity)+'\n\n')
    
    print("Average")
    print("avg_silhoutte_coeff_score :", avg_silhoutte_coeff_score/len(anno_cluster_files))
    print("avg_ARI_score :", avg_ARI_score/len(anno_cluster_files))
    print("avg_NMI_score :", avg_NMI_score/len(anno_cluster_files))
    print("avg_AMI_score :", avg_AMI_score/len(anno_cluster_files))
    print("avg_homogeneity :", avg_homogeneity/len(anno_cluster_files))
    print("avg_completeness :", avg_completeness/len(anno_cluster_files))
    print("avg_v_measure :", avg_v_measure/len(anno_cluster_files))
    print("avg_fowlkes_mallows_score :", avg_fowlkes_mallows_score/len(anno_cluster_files))
    print("avg_purity :", avg_purity/len(anno_cluster_files))
    scores_file.write("Average\n")
    scores_file.write("avg_silhoutte_coeff_score :"+ str(avg_silhoutte_coeff_score/len(anno_cluster_files)))
    scores_file.write("avg_ARI_score :"+ str(avg_ARI_score/len(anno_cluster_files)))
    scores_file.write("avg_NMI_score :"+ str(avg_NMI_score/len(anno_cluster_files)))
    scores_file.write("avg_AMI_score :"+ str(avg_AMI_score/len(anno_cluster_files)))
    scores_file.write("avg_homogeneity :"+ str(avg_homogeneity/len(anno_cluster_files)))
    scores_file.write("avg_completeness :"+ str(avg_completeness/len(anno_cluster_files)))
    scores_file.write("avg_v_measure :"+ str(avg_v_measure/len(anno_cluster_files)))
    scores_file.write("avg_fowlkes_mallows_score :"+ str(avg_fowlkes_mallows_score/len(anno_cluster_files)))
    scores_file.write("avg_purity :"+ str(avg_purity/len(anno_cluster_files)))
    scores_file.close()
        
if __name__ == "__main__":
    clustering_evaluate()
  