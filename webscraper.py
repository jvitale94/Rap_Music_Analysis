from lxml import html
import requests
from urlparse import urljoin
from bs4 import BeautifulSoup
import requests
import re
import nltk
from nltk.tokenize import RegexpTokenizer
import os
import random
import time
import socks
import socket

def scrape():
	header_list = ["Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
	"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
	"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
	"Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
	"Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)",
	"Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))",
	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)"]
	headers={"User-Agent": header_list[random.randint(0,7)]}

	artists = ['azealiabanks'] #Include other artists as you wish
	path = 'PATH TO WHERE YOU WANT TO SAVE THE FILES'

	for a in artists:
		print path+a
		first_char = a[0]
		if first_char.isdigit():
			first_char = '19'
		if not os.path.exists(a):
			print "hello"
			os.makedirs(a)
		r = requests.get('http://www.azlyrics.com/'+first_char+'/'+a+'.html', headers=headers)
		tree = html.fromstring(r.content)
		song_names = tree.xpath('//*[@id="listAlbum"]/a/text()')
		filename = a+"_song_names.txt"
		lyric_file = open(os.path.join(a, filename), "w")
		tokenizer = RegexpTokenizer(r'\w+')
		a2 = a
		#a2 is used to account for artist name changes in the song's URL
		if a == 'house':
			a2 = 'houseofpain'
		print len(song_names)
		i=0
		for l in song_names:
			i+=1
			print str(i) + ' of ' + str(len(song_names)) + ' ' + a  
			if a=='azealiabanks' and i<34:
				pass
			else:
				headers={"User-Agent": header_list[random.randint(0,7)]}
				print l
				tokens = tokenizer.tokenize(l)
				s=''
				for t in tokens:
					s+=t.lower()
				try:
					lyric_file.write(s + '\n')
				except:
					print 'problem with ' + a + ' ' + l
				song_req = requests.get('http://www.azlyrics.com/lyrics/'+a2+'/'+s+'.html', headers=headers)
				print 'Success'
				tree_song = html.fromstring(song_req.content)
				lyrics = tree_song.xpath('/html/body/div[3]/div/div[2]/div[6]/text()')
				song_file_name = s+"_"+a+"_lyric_file.txt"
				song_file = open(os.path.join(a, song_file_name), "w")
				for x in lyrics:
					song_file.write(x.encode('utf-8'))
				song_file.close()
		#This file now contains a list of songs, normalized such that they can be plugged into a URL for lyrics 
		lyric_file.close()

scrape()



