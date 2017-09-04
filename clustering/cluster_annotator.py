# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 06:14:01 2017

@author: Shanika Ediriweera
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 07:27:56 2017

@author: Shanika Ediriweera
"""

ANNOTATED_CLUSTERS = "./clusters/annotated/"
TARGETS_PATH = "./targets/annotated/"

# IMPORTANT
#change the file name of the targets file to evaluate
TARGETS_FILE = "feedback_cs2012_2.txt" #eg: feedback_cs2012_2.txt

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
    return phrases

def annotate_clusters(phrases, feedback_file="test"):
    annotated_clusters = {}
    annotated_labels = []
    
    annotated_file = open(ANNOTATED_CLUSTERS+feedback_file, 'w')
    
    print('')
    print('Enter a cluster number for the following targets-')
    for i in range(len(phrases)):
        #validate this user input
        cluster_no = '-1' #initially cluster number should not be true for isdigit()
        while( not( cluster_no.isdigit() ) or not( int( cluster_no ) < len( annotated_clusters )+1 ) ):
            cluster_no = input("Enter cluster number for '"+phrases[i]+"': ")
        #assign user input to the annotated_clusters obj
        cluster_no = int(cluster_no)
        if cluster_no not in annotated_clusters:
            annotated_clusters[cluster_no] = []
        annotated_clusters[cluster_no].append(i)
        
        #write annotated clusters to the annotated file
        annotated_file = open(ANNOTATED_CLUSTERS+feedback_file, 'w')
        print('\nclusters-')
        annotated_file.write('clusters-\n')
        for label in annotated_clusters:
            print('\ncluster '+str(label)+'-')
            annotated_file.write('\ncluster '+str(label)+'-\n')
            for point_idx in annotated_clusters[label]:
                print('cluster {0}:　{1}'.format(label, phrases[point_idx]))
                annotated_file.write('cluster '+str(label)+': '+phrases[point_idx]+'\n')
        annotated_file.close()
        
    annotated_file = open(ANNOTATED_CLUSTERS+feedback_file, 'a')
    annotated_file.write("\n")
    annotated_file.write('clusters object-\n')
    annotated_file.write(str(annotated_clusters))
    annotated_file.close()
    
    #take cluster names
    annotated_file = open(ANNOTATED_CLUSTERS+feedback_file, 'a')
    print('')
    annotated_file.write("\n")
    print('cluster names-')
    annotated_file.write("cluster names- \n")
    for i in range(len(annotated_clusters)):
        if len(annotated_clusters[i]) == 1:
            cluster_name = phrases[annotated_clusters[i][0]]
        else:
            index = -1
            while( index not in annotated_clusters[i] ):
                cluster_name = input("Enter cluster name for cluster "+str(i)+" :")
                try: 
                    index = phrases.index(cluster_name)
                except ValueError:
                    index = -1
        annotated_labels.append(cluster_name)
    #save annotated cluster names to file
    annotated_file.write(str(annotated_labels))
    annotated_file.close()
    return annotated_clusters, annotated_labels


if __name__ == "__main__":
    phrases = get_phrases_from_file(TARGETS_PATH+TARGETS_FILE) #read targets from file

    annotated_clusters, cluster_names = annotate_clusters(phrases, TARGETS_FILE)
    
    print(annotated_clusters)
    print(cluster_names)
  