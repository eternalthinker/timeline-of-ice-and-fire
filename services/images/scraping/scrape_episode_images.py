from bs4 import BeautifulSoup
import requests, re, lxml
from pathlib import Path
import time, sys
from random import randint
import urllib

cast_url = "https://www.hbo.com/game-of-thrones/cast-and-crew"

def scrape_images():

	# Avoid re-scraping 
	my_file = Path("./game-of-thrones-cast-and-crew.html")
	if my_file.is_file():
		html_file = open("game-of-thrones-cast-and-crew.html", 'r')
		soup = BeautifulSoup(html_file, "lxml")
		html_file.close()
	else:
		r  = requests.get(cast_url)
		data = r.text
		html_file = open("game-of-thrones-cast-and-crew.html", "w")
		html_file.write(data)
		soup = BeautifulSoup(data, "lxml")
		html_file.close()


	# Iterate through character listicle items and scrape attributes
	i=0
	for listicle_item in soup.find_all("div", class_="modules/Cast--castMember"):

		print(str(i))
		i=i+1

		img = listicle_item.find("img", src=True)
		link = "https://www.hbo.com" + img['src']

		print(link)

		r  = requests.get(link)
		time.sleep(randint(1, 2))




			






