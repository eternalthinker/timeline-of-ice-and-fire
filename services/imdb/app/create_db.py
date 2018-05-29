import sys

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import app

from app.database import  init_db, db_session
from app.models import *
from datasets import IMDB

init_db()

titles = IMDB().title_basics()
episodes = IMDB().episodes()
ratings = IMDB().ratings()

def add_all_episodes():
    
    for ep in all_episodes(episodes):
        t = titles.loc[titles['tconst']==ep].to_dict('records')[0]
        e = episodes.loc[episodes['tconst']==ep].to_dict('records')[0]
        r = ratings.loc[ratings['tconst']==ep].to_dict('records')
        db_session.add(episode_obj(ep, t, e, r))
        db_session.commit()
    db_session.close()


def all_episodes(e):

    parentTconst = 'tt0944947'
    all_episodes = e.loc[e['parentTconst']==parentTconst]
    return all_episodes['tconst'].tolist()


def episode_obj(tconst, t, e, r):

    averageRating = r[0]['averageRating'] if r else 0
    numVotes = r[0]['numVotes']
    seasonNumber = e['seasonNumber'] if len(e['seasonNumber']) == 2 else '0' + e['seasonNumber']
    episodeNumber = e['episodeNumber'] if len(e['episodeNumber']) == 2 else '0' + e['episodeNumber']
    EID = seasonNumber + episodeNumber

    return Episode(EID=EID, tconst=tconst, seasonNumber=seasonNumber,
                    episodeNumber=episodeNumber, title=t['originalTitle'],
                    averageRating=averageRating, numVotes=numVotes,
                    duration=t['runtimeMinutes'])