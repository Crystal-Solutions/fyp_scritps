# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 06:58:59 2017

@author: Shanika Ediriweera
"""
import similarity_calulator

# split into clusters using kmedoids
def cluster_similar_strings(similarities, threshold = 0.5):
    no_of_clusters = 0
    C = {}
    for i in range(len(similarities)):
        most_similar = i
        similarity_threshold = threshold

        for j in range(i):
            if(similarities[i][j] > similarity_threshold):
                most_similar = j
                similarity_threshold = similarities[i][j]
        if most_similar == i:
            C[no_of_clusters] = []
            C[no_of_clusters].append(i)
            no_of_clusters = no_of_clusters + 1
        else:
            for k in range(len(C)):
                if most_similar in C[k]:
                    C[k].append(i)
    return C



if __name__ == "__main__":
    S = similarity_calulator.get_similarity_matrix(phrases)
    C = cluster_similar_strings(S)
    print(C)