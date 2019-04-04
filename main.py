import string
import re
from pickle import dump
from unicodedata import normalize
from numpy import array 


# Loading Training file into memory
def load_file(filename):

    # Open file as read  Only mode
    file = open(filename, mode = 'rt', encoding = 'utf-8')

    # Reading all text
    text = file.read()

    #Close file
    file.close()

    return text

"""Each line contains a single pair of phrases, first English and then German,separated by a tab character.
We must split the loaded text by line and then by phrase. to_phrase() funtion can be used for this task"""

#Split a loaded document into  sentence
def to_pair(doc):
    lines = doc.strip().split('\n')
    pairs = [line.strip('\t') for line in lines]
    return pairs

"""Now clean each sentance. Process:
1. Remove all non-printable characters
2. Remove all punctuation characters
3. Normalize all Unicode character to ASCII (E.g Latin Characters)
4. Normalize the case to lowercase.
5. Remove any remaining tokens that are not alphabatic"""

# clean a list of lines
def clean_pairs(lines):
	cleaned = list()
	# prepare regex for char filtering
	re_print = re.compile('[^%s]' % re.escape(string.printable))
	# prepare translation table for removing punctuation
	table = str.maketrans('', '', string.punctuation)
	for pair in lines:
		clean_pair = list()
		for line in pair:
			# normalize unicode characters
			line = normalize('NFD', line).encode('ascii', 'ignore')
			line = line.decode('UTF-8')
			# tokenize on white space
			line = line.split()
			# convert to lowercase
			line = [word.lower() for word in line]
			# remove punctuation from each token
			line = [word.translate(table) for word in line]
			# remove non-printable chars form each token
			line = [re_print.sub('', w) for w in line]
			# remove tokens with numbers in them
			line = [word for word in line if word.isalpha()]
			# store as string
			clean_pair.append(' '.join(line))
		cleaned.append(clean_pair)
	return array(cleaned)
 

# Save a list to clean text into a file
def save_clean_text(sentance, filename):
    dump(sentance, open(filename, 'wb'))
    print('Saved: %s'% filename)

#loading dataset
filename = r"C:\Users\ravne\Downloads\NLP Project\deu.txt"
doc = load_file(filename)

#Split into English Grammer pairs
pairs = to_pair(doc)

#Clean Sentances
clean_pairs = clean_pairs(pairs)

#Save clean Pairs into files
save_clean_text(clean_pairs, 'english-german.pkl')

#Spot Checking
for i in range(100):
    print('[%s] => [%s]' % (clean_pairs[i,0], clean_pairs[i,1]))

    