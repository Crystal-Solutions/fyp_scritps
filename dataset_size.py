# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 00:54:31 2017

@author: Janaka
"""
import os

SRC_DIR = 'J:/Raw/CS/Sem6B/FYP/sequence_labeling/annotated_original/'


resp_count = 0
set_count = 0
#process file by file
counts = {}
for file in os.listdir(SRC_DIR):
    if file.endswith(".ann"):
        print(file)
        if(open(os.path.join(SRC_DIR, file)).read()==""):
            print("skip",file)
            continue
    
        course_name = file[9:file.find("_",9)]
        if(course_name not in counts):
            counts[course_name] = (0,0,0)
        
        txt_file_path = os.path.join(SRC_DIR, file[:-3]+"txt")
        f = open(txt_file_path)
        content = f.read()
        rc = len(content.split("\n\n")) #Response Count
        sc = len(content.split("\n")) #Sentence Count
        print(rc,sc)
        resp_count+=rc
        set_count+=1
        
        counts[course_name] = counts[course_name][0]+ 1,counts[course_name][1]+ rc,counts[course_name][2]+ sc
        
print("Total:", resp_count, set_count)
print("Average:",resp_count/set_count)

for (k, v) in counts.items():
    print(k)
    print(v)
    print(v[2]/v[1])