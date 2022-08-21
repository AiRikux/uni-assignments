import xmltodict

with open('31282016.xml') as f:
	f = xmltodict.parse(f.read())

a = f['data']['tweets']
z = 0
for x in a:
	x = x
	b = x['@date']
	#print(b)
	for i in x['tweet']:
		#print(i)
		z += 1
		c = i['@id']
		#print(c)

#print(a[0])
print(z)
#b = f['data']

#print(len(b))
#for y in b:
#	print(y)

# test

# print(x)
# print(a)
# print(b)
