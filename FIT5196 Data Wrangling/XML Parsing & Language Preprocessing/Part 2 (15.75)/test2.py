import langid
import nltk
import xlrd
from nltk.stem.porter import *
from nltk.collocations import *
import spacy

bigram_measures = nltk.collocations.BigramAssocMeasures()


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


def bi_data(data):
	bi_arr = {}
	for key in data.keys():
		rows = data[key]
		all_tokens = []
		sheet_tokens = []
		for row in rows:
			try:
				tokenizer = nltk.RegexpTokenizer("[a-zA-Z]+(?:[-'][a-zA-Z]+)?")
				tokens = tokenizer.tokenize(row["text"])
				new_tokens = [word.lower() for word in tokens if word.isalnum()]
				bigram = nltk.bigrams(new_tokens)
				tokens_l = [x for x in bigram]
				tokens_a = [x for x in new_tokens]
				all_tokens = all_tokens + tokens_a
				sheet_tokens = sheet_tokens + tokens_l
			except Exception as e: pass
		finder = BigramCollocationFinder.from_words(all_tokens)
		#a = finder.nbest(bigram_measures.pmi, 100)
		a = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:100]
		#print(finder)
		#freq = nltk.FreqDist(sheet_tokens)
		bi_arr[key] = a
	return bi_arr


data = open_file("part2/sample.xlsx")
print(bi_data(data))





