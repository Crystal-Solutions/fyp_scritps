import os
import re

html_tags = {'B':('<b>', '</b>'), 'I':('<b><i>',  '</i></b>'),'O':('','')}

source_dir = 'J:\Raw\CS\Sem6B\FYP\scripts\stanford\processed'
dest_dir = 'J:\Raw\CS\Sem6B\FYP\scripts\stanford\html'
for file in os.listdir(source_dir):
	if file.endswith(".txt"):
		file_path = os.path.join(source_dir, file)
		print("Processing: "+file_path)
		f = open(file_path)
		txt = f.read()
		responses = txt.split('\n')
		txt_out = ""
		for resp in responses:
			for tagged_word in resp.split():
				tg = tagged_word.split('/')
				#print tg
				word = tg[0]
				tag = tg[1]
				if len(tg) ==2:
					txt_out += html_tags[tag][0]+word+html_tags[tag][1]+" ";
					#print(tagged_word,tg)
			txt_out += "\n<br/>"
		
				
		txt_out = '<html><bod>'+txt_out+'</body></html>'
		#break;
		dest_file = open(os.path.join(dest_dir, file[:-3]+"html"), "w")
		dest_file.write(txt_out.encode('utf-8').strip())
		dest_file.close()
		#break
