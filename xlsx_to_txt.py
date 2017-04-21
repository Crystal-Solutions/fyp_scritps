import os
import pandas as pd
import re

def process_line(str):
    to_remove = {'<br>':". ", '<br />':". ", '<p>':" ", '</p>':" ", '\n':'. ', '&#039;':'\''}
    for tag in to_remove.keys():
        str = str.replace(tag, to_remove[tag]);

    for i in range(5):
        str = str.replace(". .", ".");
        str = str.replace(".  .", ".");
        str = str.replace("..", ".");
        str = str.replace(" .", ".");
    return str;

try:
    source_dir = '../data/original/'
    dest_dir = '../data/text'
    for file in os.listdir(source_dir):
        if file.endswith(".xlsx"):
            file_path = os.path.join(source_dir, file)
            print("Processing: "+file_path)
            #Load to pandas and save as a text.
            df = pd.read_excel(file_path, 0, skiprows=0, parse_cols='C')
            txt = ""
            for index, row in df.iterrows():
                if len(row.values) != 1:
                    print "Error: multiple values for a response";
                if row.values[0]== "":
                    print("empty");
                    continue;
                if row.values[0] == "Responses":
                    print("Responses");
                    continue;
                txt += "%s\n"%process_line(row.values[0])
            dest_file = open(os.path.join(dest_dir, file[:-4]+"txt"), "w");
            dest_file.write(txt.encode('utf-8').strip())
            dest_file.close()
            #break
except:
    print("Error");


raw_input()
#Apply Map
#dfTagged = df.applymap( lambda x: "<Response>"+x+"</Response>" )
