from bs4 import BeautifulSoup
import requests, re, lxml
from pathlib import Path
from classes import *

def scrape_deaths():

	# Avoid re-scraping 
	my_file = Path("./every-game-of-thrones-death.html")
	if my_file.is_file():
		html_file = open("every-game-of-thrones-death.html", 'r')
		soup = BeautifulSoup(html_file, "lxml")
		html_file.close()
	else:
		r  = requests.get("http://time.com/3924852/every-game-of-thrones-death/")
		data = r.text
		html_file = open("every-game-of-thrones-death.html", "w")
		html_file.write(data)
		soup = BeautifulSoup(data, "lxml")
		html_file.close()


	# Iterate through character listicle items and scrape attributes
	for listicle_item in soup.find_all("div", class_="listicle-item"):

		# The main character name is in a div with class "headline"
		# the first and only item ([0])
		name = listicle_item.find("div", class_="headline").contents[0].strip()

		# All other character details are in paragraphs
		details = listicle_item.find_all("p")
		
		# Role
		role = details[0].contents[1].strip()

		# Season and episode of death
		time_of_death = str(details[1].contents)
		match = re.search(r'Season ([0-9]*)', time_of_death)
		season_of_death = int(match.group(1))
		match = re.search(r'Episode ([0-9]*)', time_of_death)
		episode_of_death = int(match.group(1))

		# Means of death
		means_of_death = details[2].contents[1].strip()

		# Find character in memory
		# c = get_character_by_name(name)

		# if not c:
		# 	print(name + " from Times deaths not found in characters for given episodes----------------")
		# else:
		# 	c.set_season_of_death(season_of_death)
		# 	c.set_episode_of_death(episode_of_death)
		# 	c.set_means_of_death(means_of_death)
		# 	c.set_role(role)

		yield (name, season_of_death, episode_of_death, means_of_death, role)

if __name__ == "__main__":
	for death in scrape_deaths():
		print (death)



	





