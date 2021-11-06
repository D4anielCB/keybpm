# -*- coding: utf-8 -*-
import sys, json, re, os, requests
from urllib.request import urlopen, Request
from urllib.parse import urlparse, quote_plus, unquote
import eyed3



folderpath = sys.argv[0].split('\\')
folderpath = folderpath[len(folderpath)-1]
folderpath = re.sub("."+folderpath, '', sys.argv[0], flags=re.IGNORECASE)

fullpath = sys.argv[1]
#fullpathnofile = 
#print (sys.argv[1])
file = fullpath.split('\\')
#file = file[len(file)-1]
fileold = file[len(file)-1]
file = re.sub('_HP2-4BAND-3090_4band_1_', ' (', fileold, flags=re.IGNORECASE)
file = re.sub('_', ' ', fileold, flags=re.IGNORECASE)
#print(file)
extension = file.split('.')
extension = extension[len(extension)-1]
print("----------------------------------")
print(file)
print("----------------------------------")
#------------- Configuration ------------------
Remixes = False # include remixes? False = no
if re.compile("remixe?s?", re.IGNORECASE).findall(file):
	Remixes = True
Keys = {"C Major": "C", "C# Major": "C#", "D Major": "D"}
Filename = "$artist - $song $type $key $bpm" # structure of the name of the file to be renamed
MaxBPM = 140 # set the value max o a bpm
#print(Keys["D Major"])



#----------------------------------------------
def getimgtrack(url):
	#requests.get(url)
	r = requests.get(url)
	return r.content
def changetag(file,artist,song,album,genre,imagetrack,year,filename,tracknum):
	if imagetrack:
		imagetrack = getimgtrack(imagetrack)
		#ST(imagetrack)
	#try:
	#ST(file)
	audiofile = eyed3.load(file).tag
	artist = re.sub(' \,.+', '', artist, flags=re.IGNORECASE)
	if tracknum:
		audiofile.track_num = int(tracknum)
	audiofile.title = song
	audiofile.genre = genre
	audiofile.artist = artist
	audiofile.album = album
	audiofile.recording_date = year
	if filename != fileold:
		audiofile.album_artist = fileold
	if imagetrack:
		#fileimg = open("as345trfgsdf345345.jfif", 'rb').read()
		#ST(imagetrack)
		audiofile.images.set(3, imagetrack, 'image/jpeg')
		#audiofile.tag.images.set(3, imagetrack , "image/jpeg" ,u"a")
		#audiofile.tag.images.set(type_=3, img_data=None, mime_type=None, description=u"", img_url=u"https://www.suasletras.com/fotos_artista/212af3ade52a5b519986ca5a200cd0b9.jpg")
	#audiofile.tag.album_artist = "Various Artists"
	#audiofile.tag.track_num = 3
	audiofile.save(version=eyed3.id3.ID3_V2_3)
	#audiofile.tag.save()
	#try:
	#	os.remove("as345trfgsdf345345.jfif")
	#except:
	#	pass
	#except:
		#pass
#----------------------------------------------
def remove_accents(s):
    filename = "".join(i for i in s if i not in "\/:*?<>|")
    return filename
#----------------------------------------------

def ST(x="", o="w"):
	if o == "1":
		o = "a+"
	if type(x) == type({}) or type(x) == type([]) or type(x) == type(set([''])):
		y = json.dumps(x, indent=4, ensure_ascii=True)
	else:
		try:
			y = str(x)
		except:
			y = str(str(x).encode("utf-8"))
	arquivo = os.path.join(folderpath,"study.txt")
	file = open(arquivo, o)
	file.write(y+"\n"+str(type(x)))
	file.close()
	

def html(x="", o="w"):
	try:
		arquivo = os.path.join(folderpath,"_keybpm_.html")
		file = open(arquivo, o)
		file.write(x)
		file.close()
	except:
		pass

def OpenURL(url):
	r = requests.get(url = url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100110 Firefox/11.0'})
	#ST(r.text)
	return r.text
	'''req = Request(url)
	headers = {}
	headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100110 Firefox/11.0'
	for k, v in headers.items():
		req.add_header(k, v)
	try:
		final = urlopen(req).read().decode('utf-8')
		#print(11111)
	except:
		final = str(urlopen(req).read()).replace('\r', '')
	#ST(final)
	return final'''
#----------------------------------------------
def Google(key):
	key=key.replace(".mp3","")+" spotify"
	#print(quote_plus(key))
	search =  OpenURL("https://www.google.com/search?q={0}".format(quote_plus(key)))
	googlere = re.compile("https:\/\/open.spotify.com.+?\/([^\&]+).+?class.+?\"\>([^\<]+)").findall(search)
	#print(googlere)
	return googlere
	#f = OpenURL("results")
#----------------------------------------------
#bb = OpenURL("https://www.google.com/search?q=urllib.error.HTTPError%3A+HTTP+Error+403%3A+Forbidden&oq=urllib.error.HTTPError%3A+HTTP+Error+403%3A+Forbidden&aqs=chrome..69i57.604j0j7&sourceid=chrome&ie=UTF-8")
#ST(bb)


def keys(value):
	try:
		value = Keys[keybpm[0][1]]
	except:
		value = value
	return value.replace(" Major","").replace(" Minor","m")
#----------------------------------------------
def bpm(value):
	value = int(value)
	if value >= MaxBPM:
		value = str(value/2)
	else:
		value = str(value)
	return value.replace(".0","")
#----------------------------------------------
#file = "Foster the People - Worst Nites (Instrumental)"
fileq = re.sub('\(.+', '', file, flags=re.IGNORECASE) # variable to serach for the song
fileq = re.sub('^\d+( |\.|\-)', '', fileq, flags=re.IGNORECASE) # variable to serach for the song

instrumental = re.compile("(instrumental|inst)", re.IGNORECASE).findall(file)
acapella = re.compile("(aca|acca|acc?apell?a|pella|vocals?)", re.IGNORECASE).findall(file)
if instrumental:
	steam="(Inst)"
elif acapella:
	steam="(Acap)"
else:
	steam=""
# ==========================
def Results(q):
	search = OpenURL("https://musicstax.com/search?q={0}".format(quote_plus(q))).replace("\r","").replace("\n","")
	#ST(search)
	results = re.compile("\/track\/([^\/]+)\/([^\"]+).+?song-artist\"\>([^\<]+)").findall(search)
	results2 = re.compile("\/track\/([^\/]+)\/([^\"]+).+?\"([^\"]+).+?song-artist\"\>([^\<]+)").findall(search)
	#ST(search)
	fim = '<style>'
	fim+=".imageholder{position: relative; float: left;}"
	fim+=".caption{ position: absolute; top: 50%; mix-blend-mode: difference;color: rgb(0, 255, 255);font-family: verdana; font-size: 28px}"
	fim+="</style>"
	i=1
	if results2:
		results = list(dict.fromkeys(results))
		for entry in results2:
			if not 'remix' in entry[0] or Remixes:
				#fim+=" <img src=\""+entry[2]+"\">"+" "+str(i)+" "+entry[0] + " - " +entry[3]+"\n"
				fim+="<a class=\"imageholder\">"
				fim+="<div class=\"caption\">{1})<br>{2}<br>{3}</div>\n".format(entry[2],str(i),entry[0],entry[3])
				fim+="<td><img src=\"{0}\" width=\"300\">\n".format(entry[2],str(i),entry[0],entry[3])
				fim+="</a>"
				i+=1
		html(fim)
	return results
# ==========================
results = Results(fileq)
#results = False
resultsG = False
if results:
	newresults = []
	for entry in results:
		if not 'remix' in entry[0] or Remixes:
			newresults.append(entry)		
	i = 1
	for entry in newresults:
		print ("{2}) {1} - {0}".format(entry[0], entry[2], str(i) ) )
		i+=1

if not results:
	resultsG = Google(fileq)

if resultsG:
	print("GOOGLE")
	#newsearch = re.sub(' ?\- ?.+', '', resultsG[0][1], flags=re.IGNORECASE)
	newsearch = re.sub(' song by', '', resultsG[0][1], flags=re.IGNORECASE)
	newsearch = re.sub(' single by', '', resultsG[0][1], flags=re.IGNORECASE)
	newsearch = re.sub(' ?\| Spotify', '', newsearch, flags=re.IGNORECASE)
	newsearch = re.sub(', .+', '', newsearch, flags=re.IGNORECASE)
	newsearch = re.sub('\(.+?\)', '', newsearch, flags=re.IGNORECASE)
	newsearch = re.sub('  ', ' ', newsearch, flags=re.IGNORECASE)
	#print(newsearch)
	#print(newsearch)
	#print(newsearch)
	results = Results(newsearch)
	if results:
		newresults = []
		for entry in results:
			if not 'remix' in entry[0] or Remixes:
				newresults.append(entry)		
		i = 1
		for entry in newresults:
			print ("{2}) {1} - {0}".format(entry[0], entry[2], str(i) ) )
			i+=1

#ST(resultsG)
if not resultsG and not results:
	fileq = input('Not found type to search: ')
	results = Results(fileq)

	newresults = []
	for entry in results:
		if not 'remix' in entry[0] or Remixes:
			newresults.append(entry)		
	i = 1
	for entry in newresults:
		print ("{2}) {1} - {0}".format(entry[0], entry[2], str(i) ) )
		i+=1
	
choice = input('Type your choice or type the name of the song if not found: ')


while re.compile("\D+").findall(choice):
	os.system('cls||clear')
	print('-----------------------------')
	results = Results(choice)
	newresults = []
	for entry in results:
		if not 'remix' in entry[0] or Remixes:
			newresults.append(entry)		
	i = 1
	for entry in newresults:
		print ("{2}) {1} - {0}".format(entry[0], entry[2], str(i) ) )
		i+=1
	choice = input('Type your choice or type the name of the song if not found: ')
#os.system('cls||clear')

	
trackid = newresults[int(choice)-1][1]
track = OpenURL("https://musicstax.com/track/worst-nites/{0}".format(trackid)).replace("\r","").replace("\n","")
trackname = re.compile("artist\: \"([^\"]+).+?song\: \"([^\"]+)").findall(track)
year = re.compile("eventAction\: \'ReleaseYear\'\,.+?eventlabel\: \'([^\']+)", re.IGNORECASE).findall(track)
#ST(track)
image = re.compile("background: url\('([^\']+)").findall(track)
ctracknum = re.compile("data-cy\=\"meta-Track\+Number-value\">(\d+)").findall(track)
#ST(ctracknum)
imagetrack = ""
tracknum = ""
if image:
	imagetrack = image[0]
if ctracknum:
	tracknum = ctracknum[0]
keybpm = re.compile("eventAction\: \'BPM\',.+?eventLabel.+?(\d+).+?eventLabel\: \'([^\']+)").findall(track)
#ST(keybpm)
if trackname and keybpm:
	ckeys=keys(keybpm[0][1])
	cbpm=bpm(keybpm[0][0])
	cartist = re.sub(' ?\,.+', '', trackname[0][0], flags=re.IGNORECASE)
	csong = trackname[0][1]
	cyear= ""
	if year:
		cyear=year[0]
	#filename = "{0} - {1} (Inst) {3}".format(trackname[0][0], trackname[0][1], keybpm[0][0], keys(keybpm[0][1]))
	#"$artist - $song ($type) $key $bpm" 
	Filename = re.sub("\$artist", cartist, Filename, flags=re.IGNORECASE)
	Filename = re.sub("\$song", csong, Filename, flags=re.IGNORECASE)
	Filename = re.sub("\$key", ckeys, Filename, flags=re.IGNORECASE)
	Filename = re.sub("\$bpm", cbpm, Filename, flags=re.IGNORECASE)
	Filename = re.sub("\$type", steam, Filename, flags=re.IGNORECASE)
	Filename = re.sub("  ", " ", Filename, flags=re.IGNORECASE)
	#Filename
	print ("{0}.{1}".format(Filename,extension))
	newname = "{0}.{1}".format(remove_accents(Filename),extension)
	#try:
	changetag(fullpath,cartist,csong,cbpm,ckeys,imagetrack,cyear,newname,tracknum)
	#except:
		#pass
	os.rename(fullpath, newname)
	try:
		os.remove("_keybpm_.html")
	except:
		pass
#file,artist,song,album
#print (url)






