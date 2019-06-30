from __future__ import division
from bs4 import BeautifulSoup
import os
import re
import numpy as np
import pdftotext
import json

PDF_NAME='VNSE19020211'
# PDF_NAME='ONEYSGNV44586300'
directory=PDF_NAME+'/'

fileName=directory+PDF_NAME+'.pdf'
os.system('pdf2txt.py -o '+PDF_NAME+'/output.html -t html '+fileName) 

htmlData = open(directory+'output.html', 'r')
soup = BeautifulSoup(htmlData)

font_spans = [ data for data in soup.select('span') if 'font-size' in str(data) ]
output = []
for i in font_spans:
	tup = ()
	fonts_size = re.search(r'(?is)(font-size:)(.*?)(px)',str(i.get('style'))).group(2)
	tup = (str(i.text).strip(),fonts_size.strip())
	output.append(tup)

# Print the list of info and its relative size
f=open(directory+'statistics.txt','w')
for out in output: print(out,file=f)

maxSize=0
watermark=[]
for tag in output:
	size=int(tag[1])
	if (size>18): 
		string=tag[0]
		wordList=string.split(' \n')
		for word in wordList: watermark.append(word)


if __name__ == '__main__':
	# file = os.listdir()
	# file = list(filter(lambda ef: ef[0] != "." and ef[-3:] == "pdf", file))
	trueOrder={}
	update={}
	for word in watermark:
		trueOrder.update({word:0})
		update.update({word:True})

	for tag in output:
		size=int(tag[1])
		for word in watermark:
			if (update[word]==True):
				c=tag[0].count(word)
				trueOrder[word]+=c
			if (size>18 and word in tag[0]): update[word]=False

	for word in watermark: trueOrder[word]-=1

	file = [fileName]
	for filename in file:
		# Covert PDF to string by page
		print(filename)

		with open(filename, "rb") as f:
		#     for i in f:
		#         print(i)
			pdf = pdftotext.PDF(f)
		if (pdf[0] != ""):
			with open(directory+PDF_NAME[:-3]+".txt", "w+") as f:
				for page in pdf:
					f.write(page)
		
		fin=open(directory+PDF_NAME[:-3]+".txt", "r")
		fout=open(directory+PDF_NAME[:-3]+"Out", "w")

		order={}
		for word in watermark: order.update({word:0})
		for line in fin:
			for word in watermark: 
				found=line.find(word)
				if (found!=-1):
					tmp=1
					if (trueOrder[word]>0):
						trueOrd=trueOrder[word]
						tmp=line.count(word)
						if (order[word]<=trueOrd and order[word]+tmp-1>=trueOrd): 
							s=line.split()
							pos=s.index(word)
							s[pos]=''
							line=''.join(s)
					else: line=line.replace(word,'')
					order[word]+=tmp
			fout.write(line)


		
			

