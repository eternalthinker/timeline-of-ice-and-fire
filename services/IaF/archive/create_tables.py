from db import *
from iceNfire_data import *

DATABASE = 'got.db'
ice = ice_and_fire()
db = dB(DATABASE)
conn = db.connect()
cursor = conn.cursor()
chars = ice.poV   #for only point of characters
# chars = ice.char_url_list for all 436 characters
c =  characters()
house_list = houses().get_house()


for url in chars:
    n = c.get_character(url)
    db.insert(cursor, 'characters', n.__dict__)
    conn.commit()


for house in house_list:
    db.insert(cursor, 'houses', house.__dict__)
    conn.commit()
conn.close()

