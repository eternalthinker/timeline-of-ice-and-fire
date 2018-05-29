from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from app.database import Base


class Episode(Base):
    __tablename__ = 'episodes'
    EID = Column(String, primary_key=True)
    tconst = Column(String)
    seasonNumber = Column(String)
    episodeNumber = Column(String)
    title = Column(String)
    averageRating = Column(Numeric)
    numVotes = Column(Integer)
    duration = Column(Integer)

    def __repr__(self):
        return {'EID': self.EID, 'tconst': self.tconst,
                'seasonNumber': self.seasonNumber,
                'episodeNumber': self.episodeNumber, 'title': self.title,
                'averageRating': self.averageRating, 'numVotes': self.numVotes,
                'duration': self.duration}


class EpisodeCharacters(Base):
    __tablename__ = 'episode_characters'
    EID = Column(String, ForeignKey('episodes.EID'), primary_key=True)
    CID = Column(String, ForeignKey('characters.CID'), primary_key=True)

    def __repr__(self):
        return {'EID': self.EID, 'CID': self.CID}


class Character(Base):
    __tablename__ = 'characters'
    CID = Column(String, primary_key=True)
    name = Column(String)
    url = Column(String)
    actor = Column(String)
    season_of_death = Column(String)
    episode_of_death = Column(String)
    means_of_death = Column(String)
    role = Column(String)
    killed_by = Column(String)

    def __repr__(self):
        return {'CID': self.CID, 'name': self.name, 'url': self.url,
                'actor': self.actor, 'season_of_death': self.season_of_death,
                'episode_of_death ':self.episode_of_death, 
                'means_of_death': self.means_of_death, 'role': role,
                'killed_by': self.killed_by}


class Quote(Base):
    __tablename__ = 'quotes'
    QID = Column(String, primary_key=True)
    EID = Column(String, ForeignKey('episodes.EID'))
    quote_text = Column(String)

    def __repr__(self):
        return {'QID': self.QID, 'EID': self.EID, 'quote_text': self.quote_text}


class CharacterQuotes(Base):
    __tablename__ = 'character_quotes'
    CID = Column(String, ForeignKey('characters.CID'), primary_key=True)
    QID = Column(String, ForeignKey('quotes.QID'), primary_key=True)

    def __repr__(self):
        return {'CID': self.CID, 'QID': self.QID}
