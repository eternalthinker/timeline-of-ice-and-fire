import sqlite3
import sys
from sqlite3 import Error

from scrape_deaths import scrape_deaths
from classes import generate_slug
from scrape_characters import scrape_characters
from scrape_quotes import scrape_quotes


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


def get_episodes(conn):
	cur = conn.cursor()
	q = '''
		SELECT * FROM episodes;
	'''
	cur.execute(q)
	return cur

def insert_character_death(conn, value):
	''' insert_character_death(conn, ('jon', 'JON SNOW', '01', '10', 'dagger', 'lord')) '''
	cur = conn.cursor()
	q = '''
		INSERT INTO characters
		(CID, name, season_of_death, episode_of_death, means_of_death, role)
		VALUES (?, ?, ?, ?, ?, ?)
	'''
	cur.execute(q, value)
	return cur.lastrowid

def insert_new_character(conn, value):
	cur = conn.cursor()
	q = '''
		INSERT INTO characters
		(CID, name, actor)
		VALUES (?, ?, ?)
	'''
	cur.execute(q, value)
	return cur.lastrowid

def update_character(conn, value):
	cur = conn.cursor()
	q = '''
		UPDATE characters
		SET actor=?
		WHERE CID=?
	'''
	cur.execute(q, value)
	return cur

def db_has_character(conn, value):
	cur = conn.cursor()
	q = '''
		SELECT CID, name from characters
		WHERE CID=?
	'''
	cur.execute(q, value)
	return (cur.fetchone() is not None)

def execute_query(conn, q, value):
	cur = conn.cursor()
	cur.execute(q, value)
	return cur

def populate_deaths(conn):
	for death in scrape_deaths():
		value = tuple([generate_slug(death[0])]) + death
		insert_character_death(conn, value)
	print('All deaths inserted in DB')

def main():
	conn = create_connection('imdb.db')
	populate_deaths(conn)
	episodes = get_episodes(conn)
	for episode_info in episodes:
		eid, tconst, season, episode = episode_info[:4]
		print("Processing Season {} Episode {} ...".format(season, episode))

		quotes = scrape_quotes(tconst)
		for quote in quotes:
			q = '''INSERT INTO quotes (QID, EID, quote_text) VALUES(?, ?, ?)'''
			execute_query( conn, q, (quote["id"], eid, quote["text"]) )
			quote_characters = quote['characters']
			quote_characters = [generate_slug(character) for character in quote_characters]
			for slug in quote_characters:
				q = '''INSERT INTO character_quotes (CID, QID) VALUES(?, ?)'''
				execute_query( conn, q, (slug, quote["id"]) )

		characters = scrape_characters(tconst)
		ep_slugs = set()
		for character in characters:
			name, actor = character
			slug = generate_slug(name)
			if slug in ep_slugs:
				print("Repeating slug in episode:", slug, name)
				continue
			ep_slugs.add(slug)
			if db_has_character(conn, (slug,)):
				update_character(conn, (actor, slug))
			else:
				insert_new_character(conn, (slug, name, actor))
			q = '''INSERT INTO episode_characters (EID, CID) VALUES(?, ?)'''
			execute_query(conn, q, (eid, slug))

	conn.commit()
	conn.close()


if __name__ == "__main__":
	main()