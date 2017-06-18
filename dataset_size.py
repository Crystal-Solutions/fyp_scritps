# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 00:54:31 2017

@author: Janaka
"""
import os

SRC_DIR = '../data/preprocessed/space_added_before_period_sents/'


resp_count = 0
#process file by file
for file in os.listdir(SRC_DIR):
    if file.endswith(".txt"):
        print(file)
        
        txt_file_path = os.path.join(SRC_DIR, file)
        f = open(txt_file_path)
        rc = len(f.read().split("\n"))
        print(rc)
        resp_count+=rc
        
print("Total:", resp_count)