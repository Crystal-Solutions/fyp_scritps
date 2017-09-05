# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:29:02 2017

@author: Shanika Ediriweera
"""
import ast
import numpy as np
from sklearn import metrics

RESULTS_PATH = "./results/"
EVALUATED_RESULTS = "./evaluated/"

def get_silhoutte_coefficient(distance_mat, labels):
    """
    method to calculate silhoutte coefficient score for given clustering
    """
    score = metrics.silhouette_score(distance_mat, labels, metric='precomputed')
    return score

def manual_evaluate(phrases, distances, clusters, medoids, feedback_file="test"):
    evaluated_clusters = {}
    evaluated_labels = []
    for label in clusters:
        evaluated_clusters[label] = []
    
    evaluated_file = open(EVALUATED_RESULTS+feedback_file, 'w')
    
    print('')
    print('clustering result:')
    for label in clusters:
        for point_idx in clusters[label]:
            print('cluster {0}:　{1}'.format(label, phrases[point_idx]))
            #validate this user input
            evaluated_cluster = '-1' #initially cluster number should not be true for isdigit()
            while(not(evaluated_cluster.isdigit()) or not(int(evaluated_cluster) < len(clusters))):
                evaluated_cluster = input("Enter evaluated cluster number for '"+phrases[point_idx]+"': ")
                if evaluated_cluster == '':
                    evaluated_cluster = label
                    break
            #assign user input to the evaluated_clusters obj
            evaluated_clusters[int(evaluated_cluster)].append(point_idx)
    evaluated_file.write("evaluated_clusters: \n")
    evaluated_file.write(str(evaluated_clusters))
            
#    take cluster names, can use medoids for kmedoids
    print('')
    evaluated_file.write("\n")
    print('cluster labels:')
    evaluated_file.write("evaluated_cluster_names: \n")
    for i in range(len(medoids)):
        print( "cluster "+str(i)+" medoid:", phrases[medoids[i]] )
        evaluated_label = input('Enter evaluated cluster label: ')
        if evaluated_label == '':
            evaluated_label = phrases[medoids[i]]
        evaluated_labels.append(evaluated_label)
#   save evaluated clusters to a file with cluster names
    evaluated_file.write(str(evaluated_labels))
    evaluated_file.close()
    return evaluated_clusters, evaluated_labels

def get_annotated_cluster_obj(anno_file):
    f = open(anno_file, 'r')
    lines = f.read().split('\n')
    cluster_obj_line = lines[-3]
    cluster_obj = ast.literal_eval(cluster_obj_line)
    return cluster_obj

def get_purity(labels_pred, labels_anno):
    """
    Calculate the purity score for the given cluster assignments and ground truth classes
    :param labels_pred: the cluster assignments array
    :type labels_pred: numpy.array
    
    :param labels_anno: the ground truth classes
    :type labels_anno: numpy.array
    
    :returns: the purity score
    :rtype: float
    """
    A = np.c_[(labels_pred, labels_anno)]
    n_accurate = 0.
    for j in np.unique(A[:,0]):
        z = A[A[:,0] == j, 1]
        x = np.argmax(np.bincount(z))
        n_accurate += len(z[z == x])
        
    return n_accurate / A.shape[0]


def get_ARI(labels_pred, labels_anno):
    """
    Adjusted Rand index
    """
    score = metrics.adjusted_rand_score(labels_anno, labels_pred)  
    return score

def get_mutual_information_score(labels_pred, labels_anno):
    """
    Normalized Mutual Information(NMI) & Adjusted Mutual Information(AMI)
    """
    norm_score = metrics.normalized_mutual_info_score(labels_anno, labels_pred) 
    adj_score = metrics.adjusted_mutual_info_score(labels_anno, labels_pred) 
    return norm_score, adj_score

def get_homogeneity_completeness_v_measure(labels_pred, labels_anno):
    """
    homogeneity_completeness_v_measure
    """
    h, c, v = metrics.homogeneity_completeness_v_measure(labels_anno, labels_pred) 
    return h, c, v

def get_fowlkes_mallows_score(labels_pred, labels_anno):
    """
    fowlkes_mallows_score
    """
    score = metrics.fowlkes_mallows_score(labels_anno, labels_pred) 
    return score

if __name__ == "__main__":
    file = "./clusters/annotated/feedback_cs2012_3.txt"
    c = get_annotated_cluster_obj(file)
    print(c)
    
    clus = np.array([1, 4, 4, 4, 4, 4, 3, 3, 2, 2, 3, 1, 1])
    clas = np.array([5, 1, 2, 2, 2, 3, 3, 3, 1, 1, 1, 5, 2])
    print(get_purity(clus, clas))