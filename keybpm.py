import sys, json, re
from urllib.request import urlopen, Request
from urllib.parse import urlparse, quote_plus, unquote

#print (sys.argv[1])
print("----------------------------------")
#------------- Configuration ------------------
Remixes = False # include remixes? False = no
Keys = {"C Major": "C", "C# Major": "C#", "D Major": "D"}
Filename = "$artist - $song ($type) $key $bpm" # structure of the name of the file to be renamed
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
		return Keys[keybpm[0][1]]
	except:
		return value
#----------------------------------------------
def bpm(value):
	value = int(value)
	if value > MaxBPM:
		return str(value/2)
	else:
		return str(value)
#----------------------------------------------
file = "stay justin"
file = re.sub('\(.+', '', file, flags=re.IGNORECASE)

search = OpenURL("https://musicstax.com/search?q={0}".format(quote_plus(file)))
results = re.compile("track\/([^\/]+)\/([^\"]+)").findall(search)
if results:
	results = list(dict.fromkeys(results))
ST(results)

newresults = []
for entry in results:
	if not 'remix' in entry[0] or Remixes:
		newresults.append(entry)
		
i = 1
for entry in newresults:
	print ("{1}) {0}".format(entry[0], str(i)) )
	i+=1
choice = input('Type your choice: ')
#ST( newresults[int(choice)-1][1])
trackid = newresults[int(choice)-1][1]
track = OpenURL("https://musicstax.com/track/worst-nites/{0}".format(trackid)).replace("\r","").replace("\n","")
trackname = re.compile("artist\: \"([^\"]+).+?song\: \"([^\"]+)").findall(track)
keybpm = re.compile("eventAction\: \'BPM\',.+?eventLabel.+?(\d+).+?eventLabel\: \'([^\']+)").findall(track)
ST(keybpm)
if trackname and keybpm:
	#filename = "{0} - {1} (Inst) {3}".format(trackname[0][0], trackname[0][1], keybpm[0][0], keys(keybpm[0][1]))
	#"$artist - $song ($type) $key $bpm" 
	Filename = re.sub("\$artist", trackname[0][0], Filename, flags=re.IGNORECASE)
	Filename = re.sub("\$song", trackname[0][1], Filename, flags=re.IGNORECASE)
	Filename = re.sub("\$key", bpm(keybpm[0][0]), Filename, flags=re.IGNORECASE)
	Filename = re.sub("\$bpm", keys(keybpm[0][1]), Filename, flags=re.IGNORECASE)
	#Filename
print (Filename)
#print (url)








