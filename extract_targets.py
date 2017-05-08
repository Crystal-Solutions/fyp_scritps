import nltk
from nltk.tokenize import word_tokenize

DEST_PATH = r"C:\\Users\\Ravindu Hasantha\\Dropbox\\fyp\\boi_pos_data\\"

def extract(filename):
    with open(filename+'.ann','r') as f1:
        targets =[]
        for line in f1:
            words = line.split()
            try:
                if 'Target' in words[1]:
                    
                    beginning = int(words[2])
                    diff = int(words[3])- int(words[2])-1
                    data =[]
                    data.append(beginning)
                    data.append(diff)
                    targets.append(data)
            except ValueError or IndexError:
                    continue


    targets.sort();
    #print targets

    with open(filename+'.txt','r') as f2:
        string = f2.read().replace('\n', '  ')


        
    for i in range(len(targets)):
        t = targets[i][0]
        d = targets[i][1]
        string = string[:t]+'<'+string[t:]
        string = string[:t+d+2]+'>'+string[t+d+2:]
        for i in range(len(targets)):
            targets[i][0] +=2 
    #print string


    count1 = 0
    count2=0
    count = 0
    ttt = []
    while True:
        try:
            index1 = string.index('<', count1)
            index2 = string.index('>', count2)
        except ValueError:
            break
        if index2 >= 0:

            normalwords = string[count:index1]
            phrase   = string[index1:index2]

            normalwords = normalwords.strip('<')
            normalwords = normalwords.strip('>')
            phrase = phrase.strip('<')
            phrase = phrase.strip('>')
            
            count1 = index1 +1
            count2 = index2 +1
            count = index2 +1

            n = normalwords.split()
            phrases = phrase.split()
            

            if len(n):
                for w in n:
                    w = w+' O'
                    ttt.append(w)
            if len(phrases):
               ttt.append(phrases[0]+ ' B-T')
               if len(phrases)>1:
                    for i in range(len(phrases)-1):
                        ttt.append(phrases[i+1]+ ' I-T')
                        

                        
        else: break


   # print ttt

    words = [t.split()[0] for t in ttt]
    boiTags = [t.split()[1] for t in ttt]
    pos = nltk.pos_tag(words)
    #print(pos)

    with open(DEST_PATH+filename+'-result.txt','w') as f:
        for p,t in zip(pos,boiTags):
            data = p[0]+" "+p[1]+" "+t
            f.write(data+"\n")
            #print(data)
        


#extract('feedback_cs2012_1')

for i in range (6):
    extract('feedback_cs2012_'+ str(i+1))
for i in range (2):
    extract('feedback_cs2062_'+ str(i+1))
for i in range (19):
    extract('feedback_cs2202_'+ str(i+1))
    print ('feedback_cs2202_'+ str(i+1))
