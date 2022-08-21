import re

a = "#COVID19 #health #inflammation \n\nMelatonin possesses an anti-influenza potential\nthrough its immune modulatory effect\n\nMelatonin production by the pineal gland\nis affected by the colour temperature of light,\nstress hormones, medications, food additives.\n\nhttps://t.co/eMzVgZgzOW\n."
a = "Funding for wildlife and habitats welcomed \nhttps://t.co/PJT2xh2pm3\n#Australia #Australian #AustralianConservationFoundation #Bushfires #Conservation #Covid19 #Emergency #Environment #EnvironmentProtection #Government #Investment #KangarooIsland #Minister #MorrisonGovernment https://t.co/CUgsUPknN9"
a = "#COVID19 #health #inflammation \n\nMelatonin possesses an anti-influenza potential\nthrough its immune modulatory effect\n\nMelatonin production by the pineal gland\nis affected by the colour temperature of light,\nstress hormones, medications, food additives.\n\nhttps://t.co/eMzVgZgzOW\n. "

a = "\ud83d\udce2"
#a = a.encode("UTF-8").decode()
print(type(a))
#print(bytes(a).decode("unicode_escape"))

print(type(a))

print ("\ud83d\ude04".encode('utf-16','surrogatepass').decode('utf-16'))
a = "[#COVID19] \\uD83C\\uDDEC\\uD83C\\uDDF7 Greece prohibits flights from Qatar. \\n\\n\\uD83E\\uDDA0 A Qatar Airways’ aircraft landed in Athens with 96 passengers infected by the COVID-19. \\n\\n❗️ Following this event, Greece decided to refuse all flights from Qatar. https://t.co/NN3LdKAgc9"

print(a.encode("utf-16", 'surrogatepass').decode("utf-16"))
print(a.encode().decode("unicode_escape").encode('utf-16','surrogatepass').decode("utf-16"))

c = "🌸✋\\uD83C\\uDF3C\\uD83D\\uDE37💮\\uD83D\\uDC50🌸\\uD83D\\uDE37\\uD83C\\uDF3C✋💮".encode().decode("unicode_escape").encode('utf-16','surrogatepass').decode("utf-16")
print(c)

d = "\uD83D\uDC4C\uD83C\uDFFB\uD83D\uDC4D\uD83C\uDFFB\uD83D\uDC99".encode('utf-16','surrogatepass').decode('utf-16')

i = "some words 00"

e = i.replace("00", d)

print(e)

f = "\\uD83D\\uDC4D\\uD83C\\uDFFB | KEEP UP THE GOOD WORK\\n\\nWe thought we would share this message of encouragement for our Covid-19 Response Initiative from BBC NI’s Stephen Watson \\uD83D\\uDCFA @winkerwatson1 \\n\\n \\uD83D\\uDC4C\\uD83C\\uDFFB\\uD83D\\uDC4D\\uD83C\\uDFFB\\uD83D\\uDC99 ⚽️\\n\\n#YouveSupportedUs\\n#OurTurnToSupportYou\\n#BeJustAndFearNot"

f = f.replace('\\uD83D', '31282016\\uD83D')

r = re.finditer("(\\\\uD83D)(\\\\u\w{4})+", f)

for i in r:
	print(repr(i.group()))
	u = i.group().encode().decode("unicode_escape").encode('utf-16','surrogatepass').decode("utf-16")
	print(repr(u))
	f = f.replace(i.group(), u)
	#f = re.sub(repr(i.group()), u, f)
f = f.replace('31282016', '')
print(repr(f))
