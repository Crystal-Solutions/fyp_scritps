import os



#Constants
SOURCE_DIR = '../dp_create_single_file/raw_data/'
DEST_DIR = '../dp_create_single_file/corrected/'


with open("dp_out.txt", 'w') as f:

    for file in os.listdir(SOURCE_DIR):
        
        with open(SOURCE_DIR +file, 'r') as file1:
            for line in file1:
                f.write(line)



