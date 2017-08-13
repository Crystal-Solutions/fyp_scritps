# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:29:02 2017

@author: Shanika Ediriweera
"""

from sklearn import metrics
#from sklearn.metrics import pairwise_distances
#from sklearn import datasets
#dataset = datasets.load_iris()
#X = dataset.data
#y = dataset.target

#import numpy as np
#from sklearn.cluster import KMeans
#kmeans_model = KMeans(n_clusters=3, random_state=1).fit(X)
#labels = kmeans_model.labels_
#a=metrics.silhouette_score(X, labels, metric='euclidean')
#
#print(a)

def get_silhoutte_coefficient(distance_mat, labels):
    """
    method to calculate silhoutte coefficient score for given clustering
    """
    score = metrics.silhouette_score(distance_mat, labels, metric='precomputed')
    return score