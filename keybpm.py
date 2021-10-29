import sys, json, re, os
from urllib.request import urlopen, Request
from urllib.parse import urlparse, quote_plus, unquote

fullpath = sys.argv[1]
#fullpathnofile = 
#print (sys.argv[1])
file = fullpath.split('\\')
file = file[len(file)-1]
extension = file.split('.')
extension = extension[len(extension)-1]
print("----------------------------------")
print(file)
print("----------------------------------")
#------------- Configuration ------------------
Remixes = False # include remixes? False = no
Keys = {"C Major": "C", "C# Major": "C#", "D Major": "D"}
Filename = "$artist - $song $type $key $bpm" # structure of the name of the file to be renamed
MaxBPM = 140 # set the value max o a bpm
#print(Keys["D Major"])

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
	file = open("study.txt", o)
	file.write(y+"\n"+str(type(x)))
	file.close()

def OpenURL(url, headers={}, user_data={}):
	req = Request(url)
	headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100110 Firefox/11.0'
	for k, v in headers.items():
		req.add_header(k, v)
	return urlopen(req).read().decode("utf-8").replace("\r", "")
#----------------------------------------------
def keys(value):
	try:
		value = Keys[keybpm[0][1]]
	except:
		value = value
	return value.replace(" Major","").replace(" Minor","m")
#----------------------------------------------
def bpm(value):
	value = int(value)
	if value > MaxBPM:
		value = str(value/2)
	else:
		value = str(value)
	return value.replace(".0","")
#----------------------------------------------
#file = "Foster the People - Worst Nites (Instrumental)"
fileq = re.sub('\(.+', '', file, flags=re.IGNORECASE) # variable to serach for the song
fileq = re.sub('^\d+( |\.|\-)', '', fileq, flags=re.IGNORECASE) # variable to serach for the song

instrumental = re.compile("(instrumental|inst)", re.IGNORECASE).findall(file)
acapella = re.compile("(aca|acca|acapella)", re.IGNORECASE).findall(file)
if instrumental:
	steam="(Inst)"
elif acapella:
	steam="(Acap)"
else:
	steam=""
# ==========================
def Results(q):
	search = OpenURL("https://musicstax.com/search?q={0}".format(quote_plus(q))).replace("\r","").replace("\n","")
	results = re.compile("track\/([^\/]+)\/([^\"]+).+?song-artist\"\>([^\<]+)").findall(search)
	if results:
		results = list(dict.fromkeys(results))
	return results
# ==========================
results = Results(fileq)
if not results:
	fileq = input('Not found type to search: ')
	results = Results(fileq)
#ST(results)

newresults = []
for entry in results:
	if not 'remix' in entry[0] or Remixes:
		newresults.append(entry)		
i = 1
for entry in newresults:
	print ("{2}) {1} - {0}".format(entry[0], entry[2], str(i) ) )
	i+=1
	
choice = input('Type your choice or type the name of the song if not found: ')


if re.compile("\D+").findall(choice):
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
	choice = input('Type your choice: ')
	
trackid = newresults[int(choice)-1][1]
track = OpenURL("https://musicstax.com/track/worst-nites/{0}".format(trackid)).replace("\r","").replace("\n","")
trackname = re.compile("artist\: \"([^\"]+).+?song\: \"([^\"]+)").findall(track)
keybpm = re.compile("eventAction\: \'BPM\',.+?eventLabel.+?(\d+).+?eventLabel\: \'([^\']+)").findall(track)
#ST(keybpm)
if trackname and keybpm:
	#filename = "{0} - {1} (Inst) {3}".format(trackname[0][0], trackname[0][1], keybpm[0][0], keys(keybpm[0][1]))
	#"$artist - $song ($type) $key $bpm" 
	Filename = re.sub("\$artist", trackname[0][0], Filename, flags=re.IGNORECASE)
	Filename = re.sub("\$song", trackname[0][1], Filename, flags=re.IGNORECASE)
	Filename = re.sub("\$key", keys(keybpm[0][1]), Filename, flags=re.IGNORECASE)
	Filename = re.sub("\$bpm", bpm(keybpm[0][0]), Filename, flags=re.IGNORECASE)
	Filename = re.sub("\$type", steam, Filename, flags=re.IGNORECASE)
	Filename = re.sub("  ", " ", Filename, flags=re.IGNORECASE)
	#Filename
print ("{0}.{1}".format(Filename,extension))
os.rename(fullpath, "{0}.{1}".format(Filename,extension))
#print (url)








