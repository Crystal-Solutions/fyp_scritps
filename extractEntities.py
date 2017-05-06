
with open('feedback_cs2202_6.ann','r') as f1:
    targets =[]
    for line in f1:
        words = line.split()
        if words[1] =='Target':
            beginning = int(words[2])
            diff = int(words[3])- int(words[2])-1
            data =[]
            data.append(beginning)
            data.append(diff)
            targets.append(data)


targets.sort();
print targets

with open('feedback_cs2202_6.txt','r') as f2:
    string = f2.read().replace('\n', '  ')
    

    
for i in range(len(targets)):
    t = targets[i][0]
    d = targets[i][1]
    string = string[:t]+'*'+string[t:]
    string = string[:t+d+2]+'*'+string[t+d+2:]
    for i in range(len(targets)):
        targets[i][0] +=2 
print string

words = string.split()


results=[]
for i in range(len(words)):
    if words[i].startswith('*') and words[i].endswith('*'):
        a = [words[i][1:-1], 'B']
    elif words[i].startswith('*'):
        a = [words[i][1:], 'B']
    elif words[i].endswith('*'):
        a = [words[i][:-1], 'I']
    else: a = [words[i], 'O']

    results.append(a)
print results

with open('result.txt','w') as f:
    for result in results:
        f.write(result[0]+" "+result[1]+"\n")

        
        


    





        


                
                
                   
               
                
