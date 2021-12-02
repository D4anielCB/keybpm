import sys, json, re, os, requests
from urllib.request import urlopen, Request
from urllib.parse import urlparse, quote_plus, unquote

def OpenURL(url):
	r = requests.get(url = url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100110 Firefox/11.0'})
	return r.text
	
def RT(arquivo="study.txt"):
	file = open(arquivo, "r")
	return file.read().replace("\n","").replace("\r","")
def ST(x="", o="w", tipo=True, arquivo="study.txt"):
	if o == "1":
		o = "a+"
	if type(x) == type({}) or type(x) == type([]) or type(x) == type(set([''])):
		y = json.dumps(x, indent=4, ensure_ascii=True)
	else:
		try:
			y = str(x)
		except:
			y = str(str(x).encode("utf-8"))
	file = open(arquivo, o)
	if tipo:
		file.write(y+"\n"+str(type(x)))
	else:
		file.write(y)
	file.close()

def TRTV(number):
	trtv = OpenURL("https://trailers.to/en/newest/movies?pageNumber="+str(number)).replace("\n","").replace("\r","")
	trtvre = re.compile("figure.{1,5}href=.{1,5}en\/(movie|tvshow)\/(\d+).+?(tt\d+)").findall(trtv)
	#fim={}
	#fim={"tt15763882": "5063287","tt13161356": "5038705"}
	#fim={"tt15763882": "5063287", "tt12680684": "4714806"}
	fim = eval(RT("movie.txt"))
	ST(number)
	for type,id,imdb in trtvre:
		fim[imdb]=id
	#print(fim)
	ST(fim,arquivo="movie.txt",tipo=False)
	print(number)
	TRTV(number+1)
TRTV(1)
#ST(trtvre,tipo=False)