import os

#source_dir = 'C:/Users/prani/Desktop/FYP/Scripts/fyp_scritps/data'
#dest_dir = 'C:/Users/prani/Desktop/FYP/Scripts/fyp_scritps/data'
source_dir = './data'
dest_dir = './data'

for file in os.listdir(source_dir):
    print file
    dest_file = open(os.path.join(dest_dir, file[:-4]+".ann"), "w");
    dest_file.close()
