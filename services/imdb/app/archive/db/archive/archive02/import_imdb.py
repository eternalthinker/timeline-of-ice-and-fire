import pandas as pd 
import db
import datasets

DATABASE = 'imdb.db'

imdb = datasets.IMDB()
db = db.dB(DATABASE)

conn = db.connect()
cursor = conn.cursor()

episodes = imdb.all_episodes()


for ep in episodes:

    data = {}
    data['tconst'] = ep

    try:
        eps = imdb.episode(ep)
        data['seasonNumber'] = eps['seasonNumber']
        data['episodeNumber'] = eps['episodeNumber']
    except:
        pass

    try:
        rts = imdb.rating(ep)
        data['averageRating'] = rts['averageRating']
        data['numVotes'] = rts['numVotes']
    except:
        pass

    try:
        basics = imdb.title_basics(ep)
        data['title'] = basics['originalTitle']
        data['duration'] = basics['runtimeMinutes']
    except:
        pass

    print(data['tconst'])
    db.insert(cursor, 'Episode', data)
    conn.commit()

conn.close()

