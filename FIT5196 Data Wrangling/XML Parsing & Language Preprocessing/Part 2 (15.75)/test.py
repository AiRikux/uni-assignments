all_tokens = []
to_stopword = []
for key in data.keys():
	rows = data[key]
	sheet_tokens = []
	for row in rows:
		tokenizer = nltk.RegexpTokenizer("[a-zA-Z]+(?:[-'][a-zA-Z]+)?")
		tokens = word_tokenize(row["text"])
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
freq = nltk.FreqDist(all_tokens)
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

=================

bi_arr = {}
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
				tokens_l = [x for x in bigram]
				sheet_tokens = sheet_tokens + tokens_l
			except Exception as e:
				pass
		freq = nltk.FreqDist(sheet_tokens)
		bi_arr[key] = freq
	return bi_arr