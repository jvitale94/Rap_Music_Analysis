from __future__ import division
import os,sys,re,math,nltk

path = "PATH TO EVERYTHING DIRECTORY IN DATA, WHICH CAN BE FOUND HERE https://github.com/jvitale94/NLP_Data"

artists = ['2pac',			'Geto_Boys',		'NWA',
'50cent',			'Ghostface_Killah',	'Nas',
'Action_Bronson',		'Grandmaster_Flash',	'Nelly',
'Aesop_Rock',		'House_of_Pain',		'Nicki_Minaj',
'Amil',		'Ice_Cube',		'Notorious_BIG',
'Angel_Haze',		'Iggy_Azaelia',		'Outkast',
'Azaelia_Banks',		'J_Cole',			'Public_Enemy',
'Beastie_Boys',		'Jay_Z',			'Queen_Latifah',
'Big_Daddy_Kane',		'Jean_Grae',		'Raekwon',
'Camron',			'Jedi_Mind_Tricks',	'Rah_Digga',
'Chance_The_Rapper',	'Kanye_West',		'Rakim',
'Charli_Baltimore',	'Kendrick_Lamar',		'Redman',
'Childish_Gambino',	'Khia',			'Roxanne_Shante',
'Cypress_Hill',		'LL_Cool_J',		'Run_DMC',
'DMX',			'Lauryn_Hill',		'Run_The_Jewels',
'Da_Brat',			'Lil_Kim',			'Salt_N_Peppa',
'Danny_Brown',		'Lil_Mama',		'Scarface',
'De_La_Soul',		'Lil_Wanye',		'Shawnna',
'Drake',			'Lisa_Lopes',		'Slick_Rick',
'Dre',			'Ludacris',		'Snoop_Dogg',
'EL_P',			'M.I.A.',			'Sugarhill_Gang',
'Earl_Sweatshirt',		'MC_Lyte',			'TI',
'Eminem',			'MS_Jade',			'The_Roots',
'Eve',			'Mac_Miller',		'Tribe_Called_Quest',
'Foxy_Brown',		'Machine_Gun_Kelly',	'Trina',
'Frank_Ocean',		'Macklemore',		'Tyler_The_Creator',
'Freddie_Gibbs',		'Mia_X',			'Wutang_Clan',
'Future',			'Missy_Elliott',		'Yelawolf',
'Gangsta_Boo',		'Monie_Love',		'Yo_Yo',
'Geazy',			'Mos_Def',			'Young_Jeezy',]

#returns dictionary for a directory of the files in the directory and the text of the file
def load_files(path):
	dictionary = {}
	for subdir, dirs, files in os.walk(path):
		for file in files:
			loc = os.path.join(subdir, file)
			lyrics = open(loc, 'r')
			lyrics = lyrics.read()
			dictionary[file] = lyrics
	return dictionary

#MAKES A SINGLE FILE OF ALL LYRICS IN A GROUP
def make_text_file(path,s):
	alllyrics = open(s+".txt", "w")
	for subdir, dirs, files in os.walk(path):
		for file in files:
			loc = os.path.join(subdir, file)
			lyrics = open(loc, 'r')
			lyrics = lyrics.read()
			alllyrics.write(lyrics.lower())#.decode('utf-8','ignore').encode("utf-8")
	alllyrics.close()

#counts the average number of words in a song
def words_per_song(dic):
	num_words = 0
	for k in dic:
		num_words += len(dic[k].split())
	return num_words/len(dic)

#Returns number of words in a dictionary
def num_words_in_dict(dic):
	num_words = 0
	for k in dic:
		num_words += len(dic[k].split())
	return num_words

#tokenizes a string
def tokenize_string(s):
	try:
		x = nltk.wordpunct_tokenize(s.decode('utf8'))
		return x
	except:
		x = nltk.wordpunct_tokenize(s)
		return x

#returns dictionary of word counts for a dictionary of an artist's songs
def count_words(dic):
	word_counts = {}
	for k in dic:
		tokens = tokenize_string(dic[k])
		if tokens == None:
			print "NONE"
			return None
		for w in tokens:
			if w.lower() not in word_counts:
				word_counts[w.lower()] = 0
			word_counts[w.lower()]+=1
	return word_counts

#Counts the frequency of curses for a rap artist
def count_curses(tok, n):
	curses = ['ass', 'dick', 'pussy', 'fuck', 'motherfuck', 'motherfucker', 'fucking', 'bitch', 
				'shit', 'nigga', 'nigger', 'cunt',  'damn']
	num_curses = 0
	for c in curses:
		try:
			num_curses += tok[c]
		except:
			pass
	return str(num_curses/n)

#Counts the frequency of political words for a rap artist
def count_politics(tok, n):
	political_words = ['america', 'black', 'rise', 'power', 'government', 'equal', 'possible', 
					'liar', 'choice', 'realize', 'fightin', 'free', 
					'silence', 'brave', 'snakes', 'lies', 'will', 'alive']
	num_curses = 0
	for c in political_words:
		try:
			num_curses += tok[c]
		except:
			pass
	return str(num_curses/n)

def count_sex(tok, n):
	sex_words = ['sex', 'bitch', 'dick', 'suck', 'cunt', 'fuck', 'ass', 'bed', 'long', 'girlfriend', 'blow', 'penis', 
				'thirsty', 'thirst', 'pimp', 'hammer', 'jerk', 'drum', 'pussy', 'cum', 'donkey', 'mouth', 'breast'
					'raw', 'smacked', 'grind', 'hoe']
	num_curses = 0
	for c in sex_words:
		try:
			num_curses += tok[c]
		except:
			pass
	return str(num_curses/n)

#Returns the top cursers in the dataset
def top_cursers():
	print "\nTop Cursers:"
	curse_artists = {}
	for a in artists:
		d = load_files(path+a)
		numberwords = num_words_in_dict(d)
		toks = count_words(d)
		c = count_curses(toks,numberwords)
		#print a, c
		curse_artists[a] = c
	top = sorted(curse_artists, key=curse_artists.get, reverse=True)[:10]
	for t in top:
		print t, curse_artists[t]
	return top

#Returns the most political artists in the dataset
def top_political():
	print "\nTop Political:"
	pol_artists = {}
	for a in artists:
		d = load_files(path+a)
		numberwords = num_words_in_dict(d)
		toks = count_words(d)
		c = count_politics(toks,numberwords)
		#print a, c
		pol_artists[a] = c
	top = sorted(pol_artists, key=pol_artists.get, reverse=True)[:10]
	for t in top:
		print t, pol_artists[t]
	return top

def top_sex():
	print "\nTop Sex:"
	sex_artists = {}
	for a in artists:
		d = load_files(path+a)
		numberwords = num_words_in_dict(d)
		toks = count_words(d)
		c = count_sex(toks,numberwords)
		sex_artists[a] = c
	top = sorted(sex_artists, key=sex_artists.get, reverse=True)[:10]
	for t in top:
		print t, sex_artists[t]
	return top


#Computes the cosine similarity of two artists
def cosine_sim(a1, a2):
	art1 = load_files("/Users/jakevitale/Documents/CompSci/Classes/NLP/Final_Project/Data/Everything/"+a1)
	art2 = load_files("/Users/jakevitale/Documents/CompSci/Classes/NLP/Final_Project/Data/Everything/"+a2)
	dic1 = count_words(art1)
	dic2 = count_words(art2)
	score = 0
	denom1 = 0
	denom2 = 0
	for k in dic1:
		if k in dic2:
			score += dic1[k]*dic2[k]
	for k in dic1:
		denom1 += dic1[k]*dic1[k]
	for k in dic2:
		denom2 += dic2[k]*dic2[k]
	denom1 = math.sqrt(denom1)
	denom2 = math.sqrt(denom2)
	score = score/(denom1*denom2)
	return score

#returns the most similar artists in the dataset
def most_similar():
	sims = {}
	for a in artists:
		print a
		for b in artists:
			print b
			if a!=b:
				sims [(a,b)] = cosine_sim(a,b)
	newA = sorted(sims, key=sims.get, reverse=True)
	thefile = open('similarities.txt', 'w')
	for ar in newA:
		thefile.write("Artists:%s Similarity:%s\n" % (ar, sims[ar]))
	thefile.close()

#Takes in a file of embedding coordinates in a vector space, parses the text to create words 
#mapped to coordinates, and then finds the closest words to target words in the space
def embedding_similarity(filename, list_of_words):
	x = open(filename, 'r')
	embeds = x.read()
	lines = embeds.splitlines()
	e = {}
	for l in lines:
		s = l.split()
		#if negative
		try:
			a = s[0][6:]
			b = float(s[1][11:])
			c = float(s[2][:-1])
			e[a] = (b,c)
		#if positive
		except:
			a = s[0][6:]
			b = float(s[2])
			c = float(s[3][:-1])
			e[a] = (b,c)

	for w in list_of_words:
		find_closest(e, w)

#Given a dictionary of keys to coordinates, it finds the words that are withing a distance of a target word
def find_closest(e, key):
	c = []
	try:
		x1 = e[key][0]
		y1 = e[key][1]
		for k in e:
			x2 = e[k][0]
			y2 = e[k][1]
			if dist(x1, x2, y1, y2)<0.3 and k!=key:
				c.append(k)
		print key, c, "\n"
	except:
		print key + " does not exist"

def make_embeddings_all_data(list_of_words):
	path = '/Users/jakevitale/Documents/CompSci/Classes/NLP/Final_Project/word2vec/embeddings/embeddings_labels_'
	print '\nMALE'
	embedding_similarity(path+'male.txt', list_of_words)
	print '\nFEMALE'
	embedding_similarity(path+'female.txt', list_of_words)
	print '\nBLACK'
	embedding_similarity(path+'black.txt', list_of_words)
	print '\nWHITE'
	embedding_similarity(path+'white.txt', list_of_words)
	print '\n1980'
	embedding_similarity(path+'1980.txt', list_of_words)
	print '\n1990'
	embedding_similarity(path+'1990.txt', list_of_words)
	print '\n2000'
	embedding_similarity(path+'2000.txt', list_of_words)
	print '\n2010'
	embedding_similarity(path+'2010.txt', list_of_words)
	print '\nALL'
	embedding_similarity(path+'all.txt', list_of_words)



def dist(x1,x2,y1,y2):
	import math
	return math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

if __name__=='__main__':
	#There was never a set main method for my project. I added methods as I needed to produce results at different times


	# I ran these already to make the text files of categories of artists
	# make_text_file("/Users/jakevitale/Documents/CompSci/Classes/NLP/Final_Project/Data/Everything/", "all")
	# make_text_file("/Users/jakevitale/Documents/CompSci/Classes/NLP/Final_Project/Data/Gender/Female", "female")
	# make_text_file("/Users/jakevitale/Documents/CompSci/Classes/NLP/Final_Project/Data/Gender/Male", "male")
	# make_text_file("/Users/jakevitale/Documents/CompSci/Classes/NLP/Final_Project/Data/Race/White", "white")
	# make_text_file("/Users/jakevitale/Documents/CompSci/Classes/NLP/Final_Project/Data/Race/Black", "black")
	# make_text_file("/Users/jakevitale/Documents/CompSci/Classes/NLP/Final_Project/Data/Year/1980", "1980")
	# make_text_file("/Users/jakevitale/Documents/CompSci/Classes/NLP/Final_Project/Data/Year/1990", "1990")
	# make_text_file("/Users/jakevitale/Documents/CompSci/Classes/NLP/Final_Project/Data/Year/2000", "2000")
	# make_text_file("/Users/jakevitale/Documents/CompSci/Classes/NLP/Final_Project/Data/Year/2010", "2010")



	
