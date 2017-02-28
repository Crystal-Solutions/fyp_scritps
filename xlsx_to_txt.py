import os
import pandas as pd


def process_line(str):
    to_remove = {'<br>':"\n", '<br />':"\n", '<p>':" ", '</p>':" "}
    for tag in to_remove.keys():
        str = str.replace(tag, to_remove[tag]);
    return str;
    

source_dir = '../data/original/'
dest_dir = '../data/text'
for file in os.listdir(source_dir):
    if file.endswith(".xlsx"):
        file_path = os.path.join(source_dir, file)
        print("Processing: "+file_path)
        #Load to pandas and save as a text.
        df = pd.read_excel(file_path, 0, skiprows=5, parse_cols='C')
        txt = ""
        for index, row in df.iterrows():
            if len(row.values) != 1:
                print "Error: multiple values for a response";
            txt += "<Response> %s </Response>\n"%process_line(row.values[0])
        dest_file = open(os.path.join(dest_dir, file[:-4]+"txt"), "w");
        dest_file.write(txt.encode('utf-8').strip())
        dest_file.close()
        #break



#Apply Map
#dfTagged = df.applymap( lambda x: "<Response>"+x+"</Response>" )
