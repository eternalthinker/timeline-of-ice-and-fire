from bs4 import BeautifulSoup
import requests, re, lxml
from pathlib import Path

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


#Character object
class Character:
	def __init__(self, name, role, season_of_death, episode_of_death, means_of_death):
		self.name = name
		self.role = role
		self.season_of_death = season_of_death
		self.episode_of_death = episode_of_death
		self.means_of_death = means_of_death


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

	# Construct Character object 
	# (can do something with this later, or just save attributes to db)
	chrctr = Character(name, role, season_of_death, episode_of_death, means_of_death)

	# Testing
	print(str(chrctr.__dict__))

	





