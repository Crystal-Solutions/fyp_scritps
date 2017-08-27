Clustering Annotation (New)
=====================
Allocation - 
Janaka - feedback_cs2012_4, feedback_cs2062_1, feedback_cs2202_2, feedback_cs2202_8, feedback_cs2202_11, 
Pranidhith - feedback_cs2012_1, feedback_cs2202_4, feedback_cs2202_3, feedback_cs2202_5, feedback_cs2202_12,
Ravindu -feedback_cs2012_2 , feedback_cs2012_6, feedback_cs2202_6, feedback_cs2062_2, feedback_cs2202_9
Shanika - feedback_cs2012_3, feedback_cs2012_5, feedback_cs2202_1, feedback_cs2202_7, feedback_cs2202_10,  

1) open python script - cluster_annotator.py
2) change variable TARGETS_FILE to the file you are evaluating
	#eg: TARGETS_FILE = "feedback_cs2012_1.txt" 
3) run the script
4) enter a cluster number for phrases one by one when prompted. (if it does not belong to a existing cluster give the next number)
5) partial clustering will be saved in "/annotated" folder. can open it for reference
6) type cluster names for the clusters when promted. (should be a target in the cluster)

**IMPORTANT: Be careful not to run others' files. that would overwrite if they have already evaluated.


Clustering Evaluation 
=====================
Allocation - 
Janaka - feedback_cs2012_4, feedback_cs2062_1, feedback_cs2202_2, feedback_cs2202_8, feedback_cs2202_11, 
Pranidhith - feedback_cs2012_1, feedback_cs2202_4, feedback_cs2202_3, feedback_cs2202_5, feedback_cs2202_12,
Ravindu -feedback_cs2012_2 , feedback_cs2012_6, feedback_cs2202_6, feedback_cs2062_2, feedback_cs2202_9
Shanika - feedback_cs2012_3, feedback_cs2012_5, feedback_cs2202_1, feedback_cs2202_7, feedback_cs2202_10,  

1) open python script - phrase_cluster.py
2) change variable TARGETS_FILE to the file you are evaluating
	#eg: TARGETS_FILE = "feedback_cs2012_1.txt" 
3) run the script
4) clustering result will be saved in "/results" folder. can open it for reference
5) enter the correct cluster number for phrases one by one when prompted. (enter if current cluster number is correct)
6) type cluster names for the clusters when promted. (enter to take the medoid as the cluster name)

*IMPORTANT: cluster 0 contains the outliers. if the target does not have cluster put it to the cluster 0

**IMPORTANT: Be careful not to run others' files. that would overwrite if they have already evaluated.