from bs4 import BeautifulSoup
import requests, re, lxml
from pathlib import Path
import time, sys
from random import randint
import urllib

cast_url = "http://screencrush.com/game-of-thrones-characters-ranked/"
cast_url2 = "http://screencrush.com/game-of-thrones-characters-ranked-80-11/"

def scrape_screencrush():

	# Avoid re-scraping 
	my_file = Path("./game-of-thrones-characters-ranked2.html")
	if my_file.is_file():
		html_file = open("game-of-thrones-characters-ranked2.html", 'r')
		soup = BeautifulSoup(html_file, "lxml")
		html_file.close()
	else:
		r  = requests.get(cast_url2)
		data = r.text
		html_file = open("game-of-thrones-characters-ranked2.html", "w")
		html_file.write(data)
		soup = BeautifulSoup(data, "lxml")
		html_file.close()


	# Iterate through character listicle items and scrape attributes
	i=0
	for listicle_item in soup.find_all("div", class_="single-post-image"):

		print(str(i))
		i=i+1

		img = listicle_item.find("div", class_="theframe")
		link = img['data-image']

		print(link)

		character_filename = link[61:]

		print("***" + character_filename)

		# r  = requests.get(link)

		urllib.request.urlretrieve(link, character_filename)

		time.sleep(randint(1, 2))




			






