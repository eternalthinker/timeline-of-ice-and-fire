from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from app.database import Base


class Episode(Base):
    __tablename__ = 'episodes'
    EID = Column(String, primary_key=True)
    tconst = Column(String)
    seasonNumber = Column(String)
    episodeNumber = Column(String)
    title = Column(String)
    averageRating = Column(String)
    numVotes = Column(Integer)
    duration = Column(Integer)


class EpisodeCharacters(Base):
    __tablename__ = 'episode_characters'
    EID = Column(String, ForeignKey('episodes.EID'), primary_key=True)
    CID = Column(String, ForeignKey('characters.CID'), primary_key=True)


class Character(Base):
    __tablename__ = 'characters'
    CID = Column(String, primary_key=True)
    name = Column(String)
    url = Column(String)
    actor = Column(String)
    episode_of_death = Column(String)
    means_of_death = Column(String)
    role = Column(String)
    killed_by = Column(String)


class Quote(Base):
    __tablename__ = 'quotes'
    QID = Column(String, primary_key=True)
    EID = Column(String, ForeignKey('episodes.EID'))
    quote_text = Column(String)


class CharacterQuotes(Base):
    __tablename__ = 'character_quotes'
    CID = Column(String, ForeignKey('characters.CID'), primary_key=True)
    QID = Column(String, ForeignKey('quotes.QID'), primary_key=True)
