# -*- coding: utf-8 -*-
"""
Created on Wed May 17 15:23:46 2017
Take the output result files from Wapiti and Annotated files.
Create a composed annotated data set which can be viewd from brat where the predictions got wrong
@author: Janaka
"""

#def print_def(file_name):
import os
import shutil
import re
SRC_DIR = '../data/senna_output_tagged/all/output_svm_applied/'
DIFF_DEST_DIR = '../data/annotated_compared_with_results/'
ARCH_DEST_DIR = 'I:/fyp_archive/'
if os.path.isdir(DIFF_DEST_DIR):
    shutil.rmtree(DIFF_DEST_DIR)
shutil.copytree('../data/annotated/',DIFF_DEST_DIR)

#Archive Process Setup
trial_name = input("Enter name for the trial:")
f = open(ARCH_DEST_DIR+"meta.txt")
sample_index = int(f.read())
f.close()
f = open(ARCH_DEST_DIR+"meta.txt",'w')
f.write(str(sample_index+1))
f.close()
#create a folder to archive
trial_name = str(sample_index)+'_'+trial_name
archive_folder = ARCH_DEST_DIR+trial_name+'/'
os.mkdir(archive_folder)    
shutil.copytree(SRC_DIR,archive_folder+'output')

#Copy files
PATTERN_FILE = '../data/senna_output_tagged/all/pattern.txt'
RESULT_FILE = '../data/senna_output_tagged/all/accuracy/cross.txt'
shutil.copy(PATTERN_FILE,archive_folder)
shutil.copy(RESULT_FILE,archive_folder)
summary_text = ""

difs = [] #(file, startI, word, originalTag, predictedTag)
totals = [0,0,0]
sampe_count = 0
for file in os.listdir(SRC_DIR):
    if file.endswith(".txt"):
        summary_text+="\n\n"+file+"\n"
        file_path = os.path.join(SRC_DIR, file)
        print(file_path)
        txt = open(file_path).read().strip()
        tags = txt.split('\n')
        tags = list(filter(len,tags))
        tagList = []
        wordList = []
        for i in range(0,len(tags)-1,2):
            spts = tags[i].split()
            pred_tag = tags[i+1].strip()
            or_tag = spts[-1]
        
            if(spts[-1]!=pred_tag):
                sample_txt = tags[i].split()
                difs.append((spts[-3],spts[-2],spts[0],spts[-1],pred_tag))
                
            #Identify sequences
            tagList.append((or_tag,pred_tag))
            wordList.append(spts[0])
            
            
            
        #Encode to string
        count = 0
        txt = ""
        for i,j in tagList:
            txt+=i+j+'-'
        txt+="END-"
        tp = re.finditer("(BB-)(II-)*((BB|OO|BO|OB|END)-)",txt) #True Positive
        t = re.finditer("(B\w-)(I\w-)*",txt) #True
        p = re.finditer("(\wB-)(\wI-)*",txt) #Positive
        counts = []
        lsts = []
        for i in (tp,t,p):
            lst = list(i)
            lsts.append(lst)
            counts.append(len(lst))
            print(len(lst),end=", ")
            summary_text+=str(len(lst))+"\t"


        c_tp, c_t, c_p = counts
        precision = c_tp/c_p
        recall = c_tp/c_t
        if c_tp!=0:
            f1_value = 2*precision*recall/(precision+recall)
        else:
            f1_value = 0
        print("\n%1.4f"%(precision),"%1.4f"%(recall),"%1.4f"%(f1_value),end="\n\n")
        summary_text+="\n"+"%1.4f, %1.4f, %1.4f"%(precision,recall,f1_value)
        totals[0]+=precision
        totals[1]+=recall
        totals[2]+=f1_value
        sampe_count+=1


print("Average Precision, Recall, F1_Score")
summary_text+="\n\nAverage  Precision, Recall, F1_Score\n"
average_result = trial_name+", "
for i in totals:
    print("%1.4f"%(i/sampe_count), end=", ")
    summary_text+="%1.4f, "%(i/sampe_count)
    average_result+="%1.6f, "%(i/sampe_count)

print("\n\nProcessing Differences")

#        break
s = list(set(difs))
print("Number of Differences:",len(difs)-len(s))

#Mark all differences in a file
save_diffs = True
ti = 10000
if save_diffs:
    for i in s:
    #    print(i)
        f = open(DIFF_DEST_DIR+i[0]+'.ann','a')
        start,end,txt = int(i[1]),len(i[2])+int(i[1]),i[2]
        f.write("T"+str(ti)+'\tError'+i[-1]+' '+str(start)+' '+str(end)+'\t'+txt+'\n')
        f.close()
        ti+=1
#    break


f = open(archive_folder+'summary.txt','w')
f.write(summary_text)
f.close()

f = open(ARCH_DEST_DIR+'/all_results.csv','a')
f.write('\n'+average_result)
f.close()

print(summary_text)
