from autocorrect import spell
import os



#Constants
SOURCE_DIR = '../data/wordlist/'
DEST_DIR = '../data/spell_corrected_wordlist/'

def autoCorrect(filename):

    words = []
    correctedArray = []
    nounPhrase = []
    BIO = []

    getArrays(filename, words, nounPhrase, BIO)
    print(words)
    spellCorrect(words, correctedArray)
    writeToFile(filename, correctedArray, nounPhrase, BIO)


def getArrays(filename, words, nounPhrase, BIO):
    print(filename)

    file_path = os.path.join(DEST_DIR, filename)
    with open(file_path, 'r') as file:
        for line in file:

            if line == '\n':
                words.append('\n')
                nounPhrase.append('\n')
                BIO.append('\n')

            else:
                wordsInLine = line.split()
                words.append(wordsInLine[0])
                nounPhrase.append(wordsInLine[1])
                BIO.append(wordsInLine[2])
    print(nounPhrase)

def spellCorrect(wArray, correctedArray):
    for i in wArray:
        if not i.isalnum():

            if len(i)==1:
                x = i

            elif not i[-1].isalnum():
                subString = i[:-1]
                checkWord = spell(subString)
                x = checkWord+i[-1]

            elif not i[0].isalnum():
                subString = i[0:]
                checkWord = spell(subString)
                x = i[0]+checkWord

            else:
                x = i

        elif i.isdigit():
                x = i

        else:
            x = spell(i)

        correctedArray.append(x)

    print(correctedArray)


def writeToFile(fname, wrds, np, boi):
    #with open("a " + fname + '-result.txt', 'w') as f:
    file_path = os.path.join(DEST_DIR, fname)
    f = open(file_path, 'w')
    for w, n, b in zip(wrds, np, boi):
        if w=="\n":
            f.write('\n')
            continue
        else:
            f.write(w + " " + n + " " + b + " " + "\n")
    f.close()

for file in os.listdir(SOURCE_DIR):
    print(file)
    autoCorrect(file)