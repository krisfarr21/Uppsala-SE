from bs4 import BeautifulSoup as bs
from urllib.error import HTTPError
import urllib.request
import sys


def wiki_scraping(term):
	site_string = 'https://en.wikipedia.org/wiki/'
	term = urllib.parse.quote(term) ##Replace special characters in term
	try:
		url = urllib.request.urlopen(site_string + term) #open the url
	except HTTPError:
		print("Site not found.") #error if the term does not exist
		sys.exit(1)	#exit program
	soup = bs(url, "lxml") #create beautiful soup object and use lxml as parser
	for paragraph in soup.find_all("p"): #extract all dat with p tag
		print(paragraph.get_text())


if __name__ == '__main__':
	term = sys.argv[1]
	wiki_scraping(term)

