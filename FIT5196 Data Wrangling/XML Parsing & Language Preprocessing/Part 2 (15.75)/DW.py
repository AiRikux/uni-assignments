import csv, nltk, os, xlrd, langid
from nltk.corpus import words
nltk.download('words')
nltk.download('punkt')

def get_vocab():
    wordlist = words.words()
    sorted(wordlist)
    return wordlist

def write_list_to_file(arr):
    if type(arr) is not list: return False, "The array your provided is not a list"
    with open('vocab.txt', 'w+') as f:
        for line in arr:
            f.write(line + "\n")
        f.close()

def open_csv(csv_file):
    try:
        workbook = xlrd.open_workbook(csv_file)
        data = {}
        sheets = {}
        for sheet in workbook.sheets():
            sheets[sheet.name] = { "sheet": workbook.sheet_by_name(sheet.name), "rows": [] }
        for name in sheets.keys():
            sheet = sheets[name]["sheet"]
            for row in range(sheet.nrows):
                sheets[name]["rows"].append(sheet.row(row))
            for column in sheets[name]["rows"]:
                index = sheets[name]["rows"].index(column)
                column_matched = False
                for item in column:
                    cindex = column.index(item)
                    if item.value != "" and not column_matched:
                        column_matched = True
                        text = item.value
                        id = column[cindex + 1].value
                        timestamp = column[cindex + 2].value
                        sheets[name]["rows"][index] = { "text": text, "id": id, "timestamp": timestamp }
                data[name] = sheets[name]["rows"]
        return True, data
    except Exception as e: return False, e

def uni_data(data):
    uni_arr = {}
    for key in data.keys():
        rows = data[key]
        sheet_tokens = []
        for row in rows:
            try:
                tokenizer = nltk.RegexpTokenizer("[a-zA-Z]+(?:[-'][a-zA-Z]+)?")
                tokens = tokenizer.tokenize(row["text"])
                new_tokens = [ word for word in tokens if word.isalnum() ]
                tokens_l = [x.lower() for x in new_tokens]
                sheet_tokens = sheet_tokens + tokens_l
            except Exception as e: pass
        freq = nltk.FreqDist(sheet_tokens)
        uni_arr[key] = freq
    return uni_arr

def bi_data(data):
    bi_arr = {}
    for key in data.keys():
        rows = data[key]
        sheet_tokens = []
        for row in rows:
            try:
                tokenizer = nltk.RegexpTokenizer("[a-zA-Z]+(?:[-'][a-zA-Z]+)?")
                tokens = tokenizer.tokenize(row["text"])
                new_tokens = [ word.lower() for word in tokens if word.isalnum() ]
                bigram = nltk.bigrams(new_tokens)
                tokens_l = [x for x in bigram]
                sheet_tokens = sheet_tokens + tokens_l
            except Exception as e: pass
        freq = nltk.FreqDist(sheet_tokens)
        bi_arr[key] = freq
    return bi_arr

if __name__ == "__main__":
    wordlist = get_vocab()
    write_list_to_file(wordlist)

if __name__ == "__main__":
    success, data = open_csv('part2/sample.xlsx')
    if not success: print("Failed to open CSV file, error: {}".format(data))
    else:
        unigram = uni_data(data)
        bigram = bi_data(data)
        for key in data.keys():
            uni_most_common = unigram[key].most_common(100)
            bi_most_common = bigram[key].most_common(100)
            print(bi_most_common)
            print(key)

            print("===============")

    #print(len(uni_most_common))