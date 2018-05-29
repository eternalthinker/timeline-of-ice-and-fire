class Character:
	def __init__(self, slug, name="some name", played_by="some actor", quotes=[]):
					self.slug = slug
					self.name = name
					self.played_by = played_by
					self.quotes = quotes																		#List of strings, these are html


# 		self.quotes = []		# List of Quote objects for every quote the character says (or is part of, in conversation)