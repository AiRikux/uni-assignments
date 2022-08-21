import os
import re
import langid

directory = './part1'

pattern1 = "(?:{\"text\":\")(?P<text>.*?)(?:\",)(?:\"created_at\":\")(?P<date>.*?)(?:\",)(?:\"id\":\")(?P<id>\d{19})(?:\"})"
pattern2 = "(?:{\"text\":\")(?P<text>.*?)(?:\",)(?:\"id\":\")(?P<id>\d{19})(?:\",)(?:\"created_at\":\")(?P<date>.*?)(?:\"})"
pattern3 = "(?:{\"id\":\")(?P<id>\d{19})(?:\",)(?:\"text\":\")(?P<text>.*?)(?:\",)(?:\"created_at\":\")(?P<date>.*?)(?:\"})"
pattern4 = "(?:{\"id\":\")(?P<id>\d{19})(?:\",)(?:\"created_at\":\")(?P<date>.*?)(?:\",)(?:\"text\":\")(?P<text>.*?)(?:\"})"
pattern5 = "(?:{\"created_at\":\")(?P<date>.*?)(?:\",)(?:\"id\":\")(?P<id>\d{19})(?:\",)(?:\"text\":\")(?P<text>.*?)(?:\"})"
pattern6 = "(?:{\"created_at\":\")(?P<date>.*?)(?:\",)(?:\"text\":\")(?P<text>.*?)(?:\",)(?:\"id\":\")(?P<id>\d{19})(?:\"})"

ids = []
lang = ['en']

# overwrite files if any exist
# create files is none exist
out = open("31282016.xml", 'w')
out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
out.write('\n')
out.close()

out = open("31282016.xml", "a")
out.write("<data>")
out.write('\n')

dates = []
text = {}

def tweet(idp, t):
	tweet = "<tweet id=\"{i}\">{txt}</tweet>".format(i=idp, txt=t)
	return tweet


for filename in os.listdir(directory):
	# ensure that file is .txt
	# http://carrefax.com/new-blog/2017/1/16/draft
	if filename.endswith(".txt") :
		f = open(directory + "/" + filename, "r", encoding="UTF-8")
		lines = f.read()
		pattern = (pattern1, pattern2, pattern3, pattern4, pattern5, pattern6)

		# for each file we test pattern
		for p in pattern:
			m = re.finditer(p, lines)

			# check all pattern found
			for n in m:
				# print(n.groupdict())

				# assuming that all dates in the correct format
				date = n['date'][:10]
				t = n['text']
				idp = n['id']

				# print(t)

				# check if id is duplicate
				if len(ids) == 0:
					pass

				else:
					for x in ids:
						if idp == x:
							id_check = False
							break
						else:
							id_check = True

					if id_check is True:
						pass

					else:
						continue

				t = t.replace('\\\\', '\\')

				# replace many backlashes with just two
				#b = re.finditer("\\+", t)
				#for a in b:
				#	print(a.group())

				# make characters
				r = re.finditer(r"(?:.?)(\\u\w{4})+", t)
				# since emojis start with \\uD83D
				#r = re.finditer(r"(\\uD83D)(\\u\w{4})+", t)
				if r == None:
					pass
				else:
					for i in r:
						#print(i.group())
						u = i.group()
						u = u.encode().decode("unicode_escape").encode('utf-16', 'surrogatepass').decode("utf-16")
						#u = u.lower()
						#print(u)
						t = t.replace(str(i.group()), u)

				# replace new line accordingly
				t = t.replace('\\n', '\n')
				t = t.replace('\\r', '\r')


				# replace necessary values with xml values
				t = t.replace('&', '&amp;')
				t = t.replace('<', '&lt;')
				t = t.replace('>', '&gt;')
				t = t.replace(r'\"', '&quot;')
				t = t.replace(r"'", "&apos;")

				# check language
				lang_check = False
				for l in lang:
					text_lang = langid.classify(t)[0]
					if text_lang == l:
						lang_check = True
						break

					else:
						lang_check = False

				if lang_check is True:
					pass

				else:
					continue

				ids.append(idp)
				dates.append(date)

				# append tweet to dictionary list
				if text.get(date, False):
					text[date].append(tweet(idp, t))

				else:
					text[date] = []
					text[date].append(tweet(idp, t))

			continue
		else:
			continue

# make sure dates value doesnt repeat
dates = set(dates)
for d in dates:
	out.write("<tweets date=\"{dd}\">".format(dd=d))
	out.write('\n')
	for tt in text[d]:
		out.write(tt)
		out.write('\n')
	out.write("</tweets>")
	out.write('\n')
out.write("</data>")
out.close()

print("Files has been converted to xml")
