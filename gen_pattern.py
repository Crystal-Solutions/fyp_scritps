# -*- coding: utf-8 -*-
"""
Created on Thu May 25 20:31:00 2017

@author: Shanika Ediriweera
"""

pattern_file = open('generated_pattern.txt','w')

"""
generate pattern for word2vec unigrams for 1 word window
"""
def gen_w2v_unigram_single():   
    for i in range(7,307):
        line = 'U:w2v-f' + str(i-6) + '-1 X=%X[ 0,' + str(i) + ']'
        pattern_file.write(line+"\n")
        print(line)
            
    
"""
generate pattern for word2vec unigrams for 1 word window commented
"""
def gen_w2v_unigram_single_commented():   
    for i in range(7,307):
        line = '#U:w2v-f' + str(i-6) + '-1 X=%X[ 0,' + str(i) + ']'
        pattern_file.write(line+"\n")
        print(line)
        

"""
generate pattern for word2vec unigrams for 3 word window
"""
def gen_w2v_unigram_3window():   
    for i in range(7,307):
        line1 = 'U:w2v-f' + str(i-6) + '-1 L=%X[-1,' + str(i) + ']'
        line2 = 'U:w2v-f' + str(i-6) + '-1 X=%X[ 0,' + str(i) + ']'
        line3 = 'U:w2v-f' + str(i-6) + '-1 R=%X[ 1,' + str(i) + ']'
        pattern_file.write(line1 + "\n" + line2 + "\n" + line3 + "\n\n")
        print(line1 + "\n" + line2 + "\n" + line3+ "\n")


"""
generate pattern for word2vec unigrams for 3 word window commented
"""
def gen_w2v_unigram_3window_commented():   
    for i in range(7,307):
        line1 = '#U:w2v-f' + str(i-6) + '-1 L=%X[-1,' + str(i) + ']'
        line2 = '#U:w2v-f' + str(i-6) + '-1 X=%X[ 0,' + str(i) + ']'
        line3 = '#U:w2v-f' + str(i-6) + '-1 R=%X[ 1,' + str(i) + ']'
        pattern_file.write(line1 + "\n" + line2 + "\n" + line3 + "\n")
        print(line1 + "\n" + line2 + "\n" + line3+ "\n")


"""
generate pattern for word2vec unigrams for 5 word window
"""
def gen_w2v_unigram_5window():   
    for i in range(7,307):
        line1 = 'U:w2v-f' + str(i-6) + '-1LL=%X[-2,' + str(i) + ']'
        line2 = 'U:w2v-f' + str(i-6) + '-1 L=%X[-1,' + str(i) + ']'
        line3 = 'U:w2v-f' + str(i-6) + '-1 X=%X[ 0,' + str(i) + ']'
        line4 = 'U:w2v-f' + str(i-6) + '-1 R=%X[ 1,' + str(i) + ']'
        line5 = 'U:w2v-f' + str(i-6) + '-1RR=%X[ 2,' + str(i) + ']'
        pattern_file.write(line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n" + line5 + "\n\n")
        print(line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n" + line5 +"\n")
        
        
"""
generate pattern for word2vec unigrams for 5 word window commented
"""
def gen_w2v_unigram_5window_commented():   
    for i in range(7,307):
        line1 = '#U:w2v-f' + str(i-6) + '-1LL=%X[-2,' + str(i) + ']'
        line2 = '#U:w2v-f' + str(i-6) + '-1 L=%X[-1,' + str(i) + ']'
        line3 = '#U:w2v-f' + str(i-6) + '-1 X=%X[ 0,' + str(i) + ']'
        line4 = '#U:w2v-f' + str(i-6) + '-1 R=%X[ 1,' + str(i) + ']'
        line5 = '#U:w2v-f' + str(i-6) + '-1RR=%X[ 2,' + str(i) + ']'
        pattern_file.write(line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n" + line5 + "\n\n")
        print(line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n" + line5 +"\n")
        
        
"""
generate pattern for word2vec bigrams for 3 word window
U:wrd-2 L=%X[-1,0]/%X[ 0,0]
"""
def gen_w2v_bigram_3window():   
    for i in range(7,307):
        line1 = 'U:w2v-f' + str(i-6) + '-2 L=%X[-1,' + str(i) + ']/%X[ 0,' + str(i) + ']'
        line2 = 'U:w2v-f' + str(i-6) + '-2 R=%X[ 0,' + str(i) + ']/%X[ 1,' + str(i) + ']'
        pattern_file.write(line1 + "\n" + line2 + "\n\n")
        print(line1 + "\n" + line2 + "\n")


"""
generate pattern for word2vec bigrams for 3 word window commented
U:wrd-2 L=%X[-1,0]/%X[ 0,0]
"""
def gen_w2v_bigram_3window_commented():   
    for i in range(7,307):
        line1 = '#U:w2v-f' + str(i-6) + '-2 L=%X[-1,' + str(i) + ']/%X[ 0,' + str(i) + ']'
        line2 = '#U:w2v-f' + str(i-6) + '-2 R=%X[ 0,' + str(i) + ']/%X[ 1,' + str(i) + ']'
        pattern_file.write(line1 + "\n" + line2 + "\n\n")
        print(line1 + "\n" + line2 + "\n")


"""
generate pattern for word2vec bigrams for 5 word window
"""
def gen_w2v_bigram_5window():   
    for i in range(7,307):
        line1 = 'U:w2v-f' + str(i-6) + '-2LL=%X[-2,' + str(i) + ']/%X[ -1,' + str(i) + ']'
        line2 = 'U:w2v-f' + str(i-6) + '-2 L=%X[-1,' + str(i) + ']/%X[ 0,' + str(i) + ']'
        line3 = 'U:w2v-f' + str(i-6) + '-2 R=%X[ 0,' + str(i) + ']/%X[ 1,' + str(i) + ']'
        line4 = 'U:w2v-f' + str(i-6) + '-2RR=%X[ 1,' + str(i) + ']/%X[ 2,' + str(i) + ']'
        pattern_file.write(line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n\n")
        print(line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 +"\n")
        
        
"""
generate pattern for word2vec bigrams for 5 word window commented
"""
def gen_w2v_bigram_5window_commented():   
    for i in range(7,307):
        line1 = '#U:w2v-f' + str(i-6) + '-2LL=%X[-2,' + str(i) + ']/%X[ -1,' + str(i) + ']'
        line2 = '#U:w2v-f' + str(i-6) + '-2 L=%X[-1,' + str(i) + ']/%X[ 0,' + str(i) + ']'
        line3 = '#U:w2v-f' + str(i-6) + '-2 R=%X[ 0,' + str(i) + ']/%X[ 1,' + str(i) + ']'
        line4 = '#U:w2v-f' + str(i-6) + '-2RR=%X[ 1,' + str(i) + ']/%X[ 2,' + str(i) + ']'
        pattern_file.write(line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n\n")
        print(line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 +"\n")


"""
generate pattern for word2vec trigrams for 5 word window
"""
def gen_w2v_trigram_5window():   
    for i in range(7,307):
        line1 = 'U:w2v-f' + str(i-6) + '-3 L=%X[-2,' + str(i) + ']/%X[ -1,' + str(i) + ']/%X[ 0,' + str(i) + ']'
        line2 = 'U:w2v-f' + str(i-6) + '-3 X=%X[-1,' + str(i) + ']/%X[ 0,' + str(i) + ']/%X[ 1,' + str(i) + ']'
        line3 = 'U:w2v-f' + str(i-6) + '-3 R=%X[ 0,' + str(i) + ']/%X[ 1,' + str(i) + ']/%X[ 2,' + str(i) + ']'
        pattern_file.write(line1 + "\n" + line2 + "\n" + line3 + "\n" + "\n\n")
        print(line1 + "\n" + line2 + "\n" + line3 + "\n" +"\n")

"""
generate pattern
"""
def generate_pattern():
    pattern_file.write("#Word 2 vec features\n\n")
    #gen_w2v_unigram_single()
    #gen_w2v_unigram_single_commented()
    #gen_w2v_unigram_3window()
    #gen_w2v_unigram_5window()
    #gen_w2v_bigram_3window()
    #gen_w2v_bigram_5window()
    gen_w2v_trigram_5window()
    
    
generate_pattern()
pattern_file.close()

'''
U:w2v-1 X=%X[ 0,0]

U:wrd-1 L=%X[-1,0]
U:wrd-1 X=%X[ 0,0]
U:wrd-1 R=%X[ 1,0]

U:wrd-1LL=%X[-2,0]
U:wrd-1 L=%X[-1,0]
U:wrd-1 X=%X[ 0,0]
U:wrd-1 R=%X[ 1,0]
U:wrd-1RR=%X[ 2,0]

U:wrd-2 L=%X[-1,0]/%X[ 0,0]
U:wrd-2 R=%X[ 0,0]/%X[ 1,0]

U06:%x[-2,0]/%x[-1,0]
U07:%x[-1,0]/%x[0,0]
U08:%x[0,0]/%x[1,0]
U09:%x[1,0]/%x[2,0]

U10:%x[-2,0]/%x[-1,0]/%x[0,0]
U11:%x[-1,0]/%x[0,0]/%x[1,0]
U12:%x[0,0]/%x[1,0]/%x[2,0]
'''