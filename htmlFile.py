from __future__ import division
from bs4 import BeautifulSoup
import os
import re
import numpy as np
import pdftotext

# pdf2txt.py -o output.html -t html file.pdf 

htmlData = open('output.html', 'r')
soup = BeautifulSoup(htmlData)

font_spans = [ data for data in soup.select('span') if 'font-size' in str(data) ]
output = []
for i in font_spans:
    tup = ()
    fonts_size = re.search(r'(?is)(font-size:)(.*?)(px)',str(i.get('style'))).group(2)
    tup = (str(i.text).strip(),fonts_size.strip())
    output.append(tup)

maxSize=0
watermark=[]
for tag in output:
	size=int(tag[1])
	if (size>18): 
		string=tag[0]
		string=string.replace('\n','')
		wordList=string.split()
		for word in wordList: watermark.append(word)


if __name__ == '__main__':
    # file = os.listdir()
    # file = list(filter(lambda ef: ef[0] != "." and ef[-3:] == "pdf", file))

    file = ["file.pdf"]
    for filename in file:
        # Covert PDF to string by page
        print(filename)

        with open(filename, "rb") as f:
        #     for i in f:
        #         print(i)
            pdf = pdftotext.PDF(f)
        if (pdf[0] != ""):
            with open(filename[:-3]+"txt", "w+") as f:
                for page in pdf:
                    f.write(page)
        
        fin=open(filename[:-3]+"txt", "r")
        fout=open(filename[:-3]+"Out", "w")

        for line in fin:
        	for word in watermark:
        		line=line.replace(word,'')
        	fout.write(line)


        
	        

