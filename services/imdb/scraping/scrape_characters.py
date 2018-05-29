from bs4 import BeautifulSoup
import requests, re, lxml
from pathlib import Path
from classes import *

def scrape_characters(episode_id):

	if episode_id == "test":
		episode_id = "tt2085239"
		html_file = open("test_characters.html", 'r')		# This is tt5655178
		soup = BeautifulSoup(html_file, "lxml")
		html_file.close()
	else: 
		url_string = "https://www.imdb.com/title/" + episode_id + "/fullcredits?ref_=tt_cl_sm#cast"
		r  = requests.get(url_string)
		data = r.text
		soup = BeautifulSoup(data, "lxml")

	# Get episode info
	title_link = soup.find("a", class_="subnav_heading")
	episode_title = title_link.contents[0].strip()
	#print("Episode title: " + episode_title)
	e = Episode(episode_title, episode_id)
	# all_episodes.append(e)

	characters = []

	# Characters are contained in table rows within cast_list
	for table in soup.find_all("table", class_="cast_list"):
		for char_row in table.find_all("tr"):

			# Get character name
			char_name = ""
			for name_row in char_row.find_all("td", class_="character"):

				# Check if character name is enclosed in a link or not
				char_link = name_row.find("a")
				if char_link:
					char_name = char_link.contents[0]
				else:
					char_name = name_row.contents[0]
				char_name = re.sub(r'\(.*\)', '', char_name).strip() #remove bracketed info about character
				#print("Character: " + char_name)

			actor_name = None
			if char_row.find("span", class_="itemprop"):
				actor_name = char_row.find("span", class_="itemprop").contents[0].strip()
				#print("Played by: " + actor_name)

			if char_name != "":
				characters.append((char_name, actor_name))

			# Either add episode info to existing character object, or create new character with episode info
			character = get_character_by_name(char_name)
			if character:
				character.add_episode(episode_id)
				character.set_played_by(actor_name)
			else:
				if char_name != "":
					character = Character(char_name)
					character.add_episode(episode_id)
					character.set_played_by(actor_name)
					all_characters.append(character)

			# Add character to the episode's character list (added as a slug)
			#e = get_episode_by_id(episode_id)
			e.add_character(char_name)

	return characters

if __name__ == "__main__":
	print(scrape_characters('tt1480055'))



			






