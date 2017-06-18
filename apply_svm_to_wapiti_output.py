import os

SVM_DIR = '../data/senna_output_tagged/all/svm_output/'
WAPITI_DIR = '../data/senna_output_tagged/all/output/'
DEST_DIR = '../data/senna_output_tagged/all/output_svm_applied/'

TAG_COUNT = 11

for file in os.listdir(SVM_DIR):
    if file.endswith(".txt"):
        svm_file_path = os.path.join(SVM_DIR, file)
        wapiti_file_path = os.path.join(WAPITI_DIR, file)
        output_file_path =  os.path.join(DEST_DIR, file)
        
        
        #labels from svm output
        txt = open(svm_file_path).read().strip()
        labels = txt.split('\n')
        
        #sents from svm output
        txt = open(wapiti_file_path).read().strip()
        sents = txt.split('\n\n')

        #Write result to output file
        f = open(output_file_path, 'w')
        for s,label in zip(sents,labels):
            sent = s.split()
            for i in range(0,len(sent),TAG_COUNT):
                for j in sent[i:i+TAG_COUNT-1]:
                    f.write(j+" ")
                f.write('\n')
                if(label=='0'):
                    f.write('O\n')
                else:
                    f.write(sent[i+TAG_COUNT-1]+'\n')
            f.write('\n')
        f.close()
        
        print(file)
#        break