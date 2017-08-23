# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:29:02 2017

@author: Shanika Ediriweera
"""

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

def get_manual_eval_purity():
    score = 0
    return score

def get_manual_eval_ARI(labels_pred, labels_eval):
    """
    Adjusted Rand index
    """
    score = metrics.adjusted_rand_score(labels_eval, labels_pred)  
    return score


    