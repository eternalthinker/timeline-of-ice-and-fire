import sqlite3
import sys
from sqlite3 import Error
from classes import *
import os.path

sys.path.insert(0, '../db') 
sys.path.insert(0, '..') 

import config #don't think this is helping...


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "imdb.db")


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None


def add_to_db():
	print("Adding scraped information to the database")

	print(str(db_path))

	conn = create_connection(db_path)
	cur = conn.cursor()

	q = '''
			INSERT INTO characters (CID, name, url, actor, episode_of_death, means_of_death, role, killed_by)
			VALUES ("john_k", "jon man", "http", "brad pitt", "4", "sword", "knight", "paul");
		'''

	cur.execute(q)

	# Look at classes.py to see the attributes of these objects
	for c in all_characters:


		# Insert attributes into db
		print("", end="")

	for q in all_quotes:
		# Insert attributes into db
		print(".", end="")

	for e in all_episodes:
		# Insert attributes into db
		print("", end="")



 
# if __name__ == '__main__':
#     create_connection("C:\\sqlite\db\pythonsqlite.db")

