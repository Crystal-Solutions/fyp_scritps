import os
import re

def ant_to_bio(txt):
	#print(txt)
	#print("\n\n\n____Response");
	sp = re.split('<(?:Positive|Negative) gate:gateId="\\d+">', txt)
	#print(sp)
	#print("\n\n\n");
	sp2 = [re.split('</(?:Positive|Negative)>', i) for i in sp]
	#print(sp2)
	tagged_word_list = []
	for item in sp2:
		if len(item) == 1:
			for word in item[0].split(' '):
				if word!='':
					tagged_word_list.append((word,'O'));
		if len(item)==2:
			words = item[0].split();
			# first part is the tagged section
			tagged_word_list.append((words[0],'B'))
			for word in words[1:]:
				if word!='':
					tagged_word_list.append((word,'I'));
			#remaining section is the not tagged section
			for word in item[1].split(' '):
				if word!='':
					tagged_word_list.append((word,'O'));
					
	#print(tagged_word_list);
	return tagged_word_list;

try:
    source_dir = '../data/annotated/positive_negative/inline'
    dest_dir = '../data/annotated/positive_negative/bio/'
    for file in os.listdir(source_dir):
		if file.endswith(".xml"):
			file_path = os.path.join(source_dir, file)
			print("Processing: "+file_path)
			f = open(file_path)
			txt = f.read()
			txt = txt.replace('&apos;','\'');
			txt = txt.replace('\'s',' \'s');
			txt = txt.replace('\n', '. ');
			responses = [txt]#.split('\n')
			tagged_resp = map(ant_to_bio,responses)
			txt_out = ""
			for resp in tagged_resp:
				for word in resp:
					txt_out += word[0]+"\t"+word[1]+"\n"
			
			dest_file = open(os.path.join(dest_dir, file[:-3]+"tsv"), "w")
			dest_file.write(txt_out.encode('utf-8').strip())
			dest_file.close()
			#break
	#
except:
	print 'Error'
	
input()