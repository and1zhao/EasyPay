import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
import PyDictionary
from PyDictionary import PyDictionary
import sys
import os

#method to remove duplicates from a list (taken from github)
def removeDupes(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

#initializes a dictionary
dictionary=PyDictionary()

#initializes a lemmatizer (makes words into base word ie running -> run)
lemmatizer = WordNetLemmatizer()

#sets stop_words (words in English Langauge that don't hold meaning ie "is")
stop_words = set(stopwords.words("english"))

#open the q's
file = open('q.txt', 'r')
nouns = []
verbs = []

#enter first line of q's u want to read; last line of q's u want to read; and intent
start = int(input('Enter the first line you want to read: '))
end = int(input('Enter the last line you want to read: '))
intent = raw_input('Enter the intent: ')

#sort nouns/verbs
for a in range(end):
	line = file.readline()
	if a >= start-1:	
		tokenized = sent_tokenize(line)
		for i in tokenized:
			addWord_N = False
			addWord_V = False
			wo = nltk.word_tokenize(i)
			tagged = nltk.pos_tag(wo)
			total = len(tagged)

			for j in range(total):
				if tagged[j][1]=="NN":
					addWord_N = True
				elif tagged[j][1] == "NNS":
					addWord_N = True
				elif tagged[j][1] == "VB":
					addWord_V = True
				elif tagged[j][1] == "VBD":
					addWord_V = True
				elif tagged[j][1] == "VBG":
					addWord_V = True
				elif tagged[j][1] == "VBN":
					addWord_V = True	
				elif tagged[j][1] == "VBP":
					addWord_V = True
				elif tagged[j][1] == "VBZ":
					addWord_V = True

				if addWord_N:
					nouns.append(tagged[j][0])
					addWord_N = False
				elif addWord_V:
					verbs.append(tagged[j][0])	
					addWord_V = False							

file.close()

#remove stop words
removed = []

for stword in stop_words:
	for n in nouns:
		if n == stword:
			removed.append(n)
	for v in verbs:
		if v == stword:
			removed.append(v)
			
#choose a seedword noun you want to match synonyms with
target_N = raw_input('Enter target noun: ')
target_N = lemmatizer.lemmatize(target_N)
wordlist_N = []

target_N += ".n.01"
w1 = wn.synset(target_N)

for var in nouns:
	keepGoing = True

	#ignore removed words
	for rmv in removed:
		if var == rmv:
			keepGoing = False

	if keepGoing:

		#compare the similarity between the current word and seedword and see if they are 50% similar (value can be changed)
		syns = wn.synsets(var)
		wc = wn.synset(syns[0].name())
		if w1.wup_similarity(wc) >= .5:
			
			#add word to list, unless it's already in there
			addWord = True

			for i in range(len(wordlist_N)):
				if var == wordlist_N[i]:
					addWord = False

			if addWord:
				wordlist_N.append(var)

#add synonyms using PyDictionary (can add other synonym databases here too)

#wordbank is all total synonyms come across, addedWords pulls the ones that have been hit multiple times
wordbank_N = []
addedWords_N = []

#go through each word in wordlist and get the synonyms
for var in wordlist_N:
	syns = dictionary.synonym(var)
	for i in range(len(syns)):

		#add the synonyms to wordbank if first occurance or add it to addeWords if second + occurance
		addWord = True

		for j in range(len(wordbank_N)):
			if syns[i] == wordbank_N[j]:
				for k in range(len(addedWords_N)):
					if syns[i] == addedWords_N[k]:
						addWord == False

				if (addWord):
					addedWords_N.append(syns[i])
				addWord = False

		if addWord:
			wordbank_N.append(syns[i])

#add these synonyms into your list
wordlist_N.extend(addedWords_N)

#remove duplicates
wordlist_N = removeDupes(wordlist_N)

#print the nounlist into "list_n.txt"
oldstdout = sys.stdout
sys.stdout = open('list_n.txt','wt')

for var in wordlist_N:
	print(var)

#run expandNoun to expand the queries using these nouns variations
sys.stdout = oldstdout
os.system("java expandNoun " + str(start) + " " + str(end) + " " + intent)	


#choose a seedword verb you want to match synonyms with
target_V = raw_input('Enter target verb: ')
target_V = lemmatizer.lemmatize(target_V, 'v')
wordlist_V = []
target_V += ".v.01"
w2 = wn.synset(target_V)

sys.stdout = oldstdout

for var in verbs:
	keepGoing = True

	#ignore removed words
	for rmv in removed:
		if var == rmv:
			keepGoing = False

	if keepGoing:

		#compare the similarity between the current word and seedword and see if they are 50% similar (value can be changed)		
		syns = wn.synsets(var)
		
		for i in range(len(syns)):
			wc = wn.synset(syns[i].name())
			if w2.wup_similarity(wc) >= .5:
				
				#add word to list, unless it's already in there
				addWord = True

				for i in range(len(wordlist_V)):
					if var == wordlist_V[i]:
						addWord = False

				if addWord:
					wordlist_V.append(var)

#add synonyms using PyDictionary (can add other synonym databases here too)

#wordbank is all total synonyms come across, addedWords pulls the ones that have been hit multiple times
wordbank_V = []
addedWords_V = []

#go through each word in wordlist and get the synonyms
for var in wordlist_V:
	syns = dictionary.synonym(var)
	for i in range(len(syns)):

		#add the synonyms to wordbank if first occurance or add it to addeWords if second + occurance

		addWord = True

		for j in range(len(wordbank_V)):
			if syns[i] == wordbank_V[j]:
				for k in range(len(addedWords_V)):
					if syns[i] == addedWords_V[k]:
						addWord == False

				if (addWord):
					addedWords_V.append(syns[i])
				addWord = False

		if addWord:
			wordbank_V.append(syns[i])

#add these synonyms into your list
wordlist_V.extend(addedWords_V)

#remove duplicates in list
wordlist_V = removeDupes(wordlist_V)

#print verbs list into "list_v.txt"
sys.stdout = open('list_v.txt','wt')

for var in wordlist_V:
	print(var)	

#run expandVerb.java to expand queries using verb varaitions
sys.stdout = oldstdout
os.system("java expandVerb " + str(start) + " " + str(end) + " " + intent)

#compile both the files at the end to make one output file "expand.txt"
os.system("java compile")


