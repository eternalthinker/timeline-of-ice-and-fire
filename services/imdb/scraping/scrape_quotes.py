from bs4 import BeautifulSoup
import requests, re, lxml
from pathlib import Path

from classes import *

def scrape_quotes(episode_id):
	quotes_list = []
	if episode_id == "test":
		episode_id = "tt5655178"
		html_file = open("test.html", 'r')		# This is tt5655178
		soup = BeautifulSoup(html_file, "lxml")
		html_file.close()
	else: 
		url_string = "https://www.imdb.com/title/" + episode_id + "/quotes/?tab=qt&ref_=tt_trv_qu"
		r  = requests.get(url_string)
		data = r.text
		soup = BeautifulSoup(data, "lxml")

	#print("\n\n\n\n")

	# Iterate through quotes and scrape attributes
	# Quotes are contained in divs with class "sodatext"
	# For the purposes of this, each "sodatext" is a quote, even if it contains a conversation with several characters.
	# If it's a conversation, the "quote" is attributed to each of them.
	i = 1
	for quote_div in soup.find_all("div", class_="sodatext"):

		quote_characters = []
		full_quote_string = ""

		# Quotes and setting details are contained in paragraphs, sometimes one of each.
		for quote in quote_div.find_all("p"):

			character_name = quote.find("span", class_="character")
			setting_info = quote.find("span", class_="fine")

			# In this case, there is a quote with some information, e.g. "Euron Greyjoy: [to Theon] Come on, you cockless coward."
			# If this is the case, the quote is at contents[4]
			if character_name and setting_info:

				character_name_string = character_name.contents[0]
				setting_string = setting_info.contents[0]
				quote_string = str(quote.contents[4])[1:].strip()

				# Add to data structures
				if not get_character_by_name(character_name_string):
					all_characters.append(Character(character_name_string))
				if not character_name_string in quote_characters:
					quote_characters.append(character_name_string)

				# Add to full quote string
				html = "<p>" + character_name_string + ": " + "[" + setting_string + "] " + quote_string + "</p>"
				full_quote_string += html

				# Testing
				# print(character_name_string, end=": ")
				# print("[" + setting_string, end="] ")
				# print(quote_string)

			# In this case, there is a quote with no extra info, e.g. "Arya Stark: That's not you.""
			# If this is the case, the quote is at contents[2]
			elif character_name:

				character_name_string = character_name.contents[0]
				quote_string = str(quote.contents[2])[1:].strip()	# Remove leading ":" and whitespace from quote

				# Add to data structures
				if not get_character_by_name(character_name_string):
					all_characters.append(Character(character_name_string))
				if not character_name_string in quote_characters:
					quote_characters.append(character_name_string)

				# Add to full quote string
				html = "<p>" + character_name_string + ": " + quote_string + "</p>"
				full_quote_string += html

				# Testing
				# print(character_name_string, end=": ")
				# print(quote_string)

				
			# In this case, it's just setting info, e.g. "[Randyll and Dickon turn to Jaime]"
			elif setting_info:
				setting_string = setting_info.contents[0]

				# Add to full quote string
				html = "<p>" + "[" + setting_string + "]" "</p>"
				full_quote_string += html

				# Testing
				#print("[" + setting_string + "]")


		# Add full quote to all_quotes
		quote_id = episode_id + "-" + str(i)
		i = i+1
		new_quote = Quote(full_quote_string, quote_characters, episode_id, quote_id)
		all_quotes.append(new_quote)

		quotes_list.append({
			'text': full_quote_string,
			'id': quote_id,
			'characters': quote_characters
		})

		# Add quote object to each character involved in the quote
		for char_name in quote_characters:
			c = get_character_by_name(char_name)
			if c:
				c.add_quote(new_quote)
			else:
				print("***********something wrong, that character doesn't exist***************")

		# Testing
		# print("")
		# print("Characters in the quote: " + str(quote_characters))
		# print("")
		# print("HTML quote: ID " + quote_id)
		# print(full_quote_string)
		# print("----------------------------------------")
		# print("")
	return quotes_list


if __name__ == "__main__":
	print(scrape_quotes('tt1480055'))