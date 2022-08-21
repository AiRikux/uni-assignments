import langid
import nltk
import xlrd
from nltk.stem.porter import *
from nltk.collocations import *
import spacy

# make variables for later
ps = PorterStemmer()
model = spacy.load('en_core_web_sm')
pattern = "[a-zA-Z]+(?:[-'][a-zA-Z]+)?"
bigram_measures = nltk.collocations.BigramAssocMeasures()

# get stopwords as a list
with open("part2/stopwords_en.txt") as f:
	content = f.readlines()
	stopwords = [x.strip() for x in content]

def open_file(file):
	try:
		# set up sheets dictionary to store values per sheet
		data = {}
		sheets = {}
		# open workbook using xlrd
		workbook = xlrd.open_workbook(file)
		# get sheet as an object
		for sheet in workbook.sheets():
			sheets[sheet.name] = {"sheet": workbook.sheet_by_name(sheet.name), "rows": []}
		# go through sheets dictionary
		for name in sheets.keys():
			sheet = sheets[name]["sheet"]
			# get row range in sheets for it to loop thru to get values in the row
			for row in range(sheet.nrows):
				sheets[name]["rows"].append(sheet.row(row))
			# loop through values in the row to differentiate columns
			for column in sheets[name]["rows"]:
				# get index to get info later
				index = sheets[name]["rows"].index(column)
				column_matched = False
				for item in column:
					# get item index
					col_index = column.index(item)
					# make sure its not empty cell
					# wont continue to loop when text is found
					if item.value != "" and not column_matched:
						column_matched = True
						text = item.value
						# use index to get id and time
						idc = column[col_index + 1].value
						timestamp = column[col_index + 2].value
						# append to replace "column" index
						sheets[name]["rows"][index] = {"text": text, "id": idc, "timestamp": timestamp}
			data[name] = sheets[name]["rows"]
		return data
	except Exception as e:
		return e


def lang_check(data):
	try:
		new_data = {}
		if type(data) is not dict:
			return "The array you provided is not a dictionary"
		for key in data.keys():
			new_data[key] = []
			rows = data[key]
			index = 0
			for row in rows:
				# remove empty row
				if type(row) is not dict:
					continue
				# remove titles
				if row['text'] == 'text' and row['id'] == 'id' and row['timestamp'] == 'created_at':
					continue
				text = str(row['text'])
				lang_test = langid.classify(text)
				# check if its english
				if lang_test[0] != 'en':
					continue
				# add row to dictionary
				new_data[key].append(row)
				index += 1
		return new_data
	except Exception as e:
		return e

# bigrams but with PorterStemmer and stopwords
def bigrams_vocab(data):
	bi_arr = {}
	table_tokens = []
	for key in data.keys():
		rows = data[key]
		sheet_tokens = []
		for row in rows:
			try:
				tokenizer = nltk.RegexpTokenizer("[a-zA-Z]+(?:[-'][a-zA-Z]+)?")
				tokens = tokenizer.tokenize(row["text"])
				new_tokens = []
				for word in tokens:
					word = word.lower()
					if word.isalnum() == False:
						continue
					elif word.lower() in stopwords:
						continue
					else:
						word = ps.stem(word)
					# make sure after transform is still in limit
					if len(word) < 3:
						continue
					else:
						new_tokens.append(word)
				bigram = nltk.bigrams(new_tokens)
				tokens_a = [x.lower() for x in new_tokens]
				tokens_l = [x for x in bigram]
				sheet_tokens = sheet_tokens + tokens_l
				table_tokens = table_tokens + tokens_a
			except Exception as e:
				pass
		freq = nltk.FreqDist(sheet_tokens)
		bi_arr[key] = freq
	#print(table_tokens)
	finder = BigramCollocationFinder.from_words(table_tokens)
	a = finder.nbest(bigram_measures.pmi, 200)
	return a


def update_stopwords(data):
	all_tokens = []
	to_stopword = []
	for key in data.keys():
		rows = data[key]
		sheet_tokens = []
		for row in rows:
			tokenizer = nltk.RegexpTokenizer("[a-zA-Z]+(?:[-'][a-zA-Z]+)?")
			tokens = tokenizer.tokenize(row["text"])
			print(tokens)
			new_tokens = [ps.stem(word) for word in tokens]
			tokens_l = [x.lower() for x in new_tokens]
			sheet_tokens = sheet_tokens + tokens_l
			all_tokens = all_tokens + tokens_l

		a = set(sheet_tokens)
		to_stopword = to_stopword + list(a)
	to_stopword = nltk.FreqDist(to_stopword)
	for key in to_stopword.keys():
		if to_stopword[key] < 5:
			stopwords.append(key)
	freq = BigramCollocationFinder.from_words(all_tokens)
	freq = freq.apply_freq_filter(3)
	# print(type(freq.keys()))
	for key in freq.keys():
		# print(str(key) + " " + str(freq[key]))
		# print("-----")
		if langid.classify(key)[0] != 'en':
			continue
		if len(key) < 3:
			continue
		if key in stopwords:
			continue
		print(key)
		text = str(key) + ":" + str(freq[key])
		print(text)

def get_vocab(data):
	vocab = {}
	for key in data.keys():
		rows = data[key]
		sheet_tokens = []
		for row in rows:
			try:
				tokenizer = nltk.RegexpTokenizer("[a-zA-Z]+(?:[-'][a-zA-Z]+)?")
				tokens = tokenizer.tokenize(row["text"])
				new_tokens = []
				for word in tokens:
					word = word.lower()
					if word.isalnum() == False:
						continue
					elif word.lower() in stopwords:
						continue
					else:
						word = ps.stem(word)
					# make sure after transform is still in limit
					if len(word) < 3:
						continue
					else:
						new_tokens.append(word)
				tokens_l = [x.lower() for x in new_tokens]
				sheet_tokens = sheet_tokens + tokens_l
			except Exception as e:
				pass
		freq = nltk.FreqDist(sheet_tokens)
		vocab[key] = freq
	return vocab


# make unigram
def uni_data(data):
	uni_arr = {}
	for key in data.keys():
		rows = data[key]
		sheet_tokens = []
		for row in rows:
			try:
				tokenizer = nltk.RegexpTokenizer("[a-zA-Z]+(?:[-'][a-zA-Z]+)?")
				tokens = tokenizer.tokenize(row["text"])
				new_tokens = []
				for word in tokens:
					word = word.lower()
					if word.isalnum() == False:
						continue
					elif word in stopwords:
						continue
					else:
						word = ps.stem(word)
					# make sure transformed word doesn't decrease len later
					if len(word) < 3:
						continue
					else:
						new_tokens.append(word)
				tokens_l = [x.lower() for x in new_tokens]
				sheet_tokens = sheet_tokens + tokens_l
			except Exception as e:
				pass
		freq = nltk.FreqDist(sheet_tokens)
		uni_arr[key] = freq
	return uni_arr


# make bigram
def bi_data(data):
	bi_arr = {}
	for key in data.keys():
		rows = data[key]
		sheet_tokens = []
		for row in rows:
			try:
				tokenizer = nltk.RegexpTokenizer("[a-zA-Z]+(?:[-'][a-zA-Z]+)?")
				tokens = tokenizer.tokenize(row["text"])
				new_tokens = [word.lower() for word in tokens if word.isalnum()]
				bigram = nltk.bigrams(new_tokens)
				tokens_l = [x for x in bigram]
				sheet_tokens = sheet_tokens + tokens_l
			except Exception as e: pass
		freq = nltk.FreqDist(sheet_tokens)
		bi_arr[key] = freq
	return bi_arr


# make file for unigram
def make_uni(data):
	unigram = uni_data(data)
	f = open("31282016_100uni.txt", "w")
	for key in data.keys():
		uni_100 = unigram[key].most_common(100)
		line = key + ":" + str(uni_100)
		f.write(line)
		f.write('\n')
	f.close()


# make file for bigrams
def make_bi(data):
	bigram = bi_data(data)
	f = open("31282016_100bi.txt", "w")
	for key in data.keys():
		bi_100 = bigram[key].most_common(100)
		line = key + ":" + str(bi_100)
		f.write(line)
		f.write('\n')
	f.close()


if __name__ == "__main__":
	print(len(stopwords))
	data = open_file("part2/sample.xlsx")
	print("finished open file")
	data = lang_check(data)
	print("finished language check")
	#update_stopwords(data)
	#print(bigrams_vocab(data))
	#for key in data.keys():
	#	bigrams = bigram[key].most_common(100)
	#	print(bigrams)
	#bigrams_vocab(data)
	#get_vocab(data, "part2/stopwords_en.txt")
	#make_bi(data)
	for key in data.keys():
		print(make_uni(data)[key])


