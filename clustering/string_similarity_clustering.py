# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 06:58:59 2017

@author: Shanika Ediriweera
"""
import similarity_calulator

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
    return C, no_of_clusters



if __name__ == "__main__":
    S = similarity_calulator.get_similarity_matrix(phrases)
    C, no_of_clusters = cluster_similar_strings(S)
    print("no_of_clusters: ",no_of_clusters)
    print(C)