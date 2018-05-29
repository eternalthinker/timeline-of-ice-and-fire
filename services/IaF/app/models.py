from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from app.database import Base


class Character(Base):
    __tablename__ = 'characters'
    id = Column(String, primary_key=True)
    name = Column(String)
    slug = Column(String)
    gender = Column(String)
    culture = Column(String)
    titles = Column(String)
    aliases = Column(String)
    father = Column(String)
    mother = Column(String)
    spouse = Column(String)
    allegiances = Column(String)
    seasons = Column(String)
    actor = Column(String)

    def __repr__(self):
        return {'CID': self.CID, 'name': self.name, 'slug': self.slug, 
                'gender': self.gender, 'culture': self.culture, 'title': self.title,
                'aliases': self.aliases, 'father': self.father,
                'mother': self.mother, 'spouse': self.spouse,
                'allegiances': self.allegiances, 'seasons': self.seasons,
                'actor': self.actor}


class House(Base):
    __tablename__ = 'houses'
    id = Column(String, primary_key=True)
    name = Column(String)
    slug = Column(String)
    region = Column(String)
    coatOfArms = Column(String)
    words = Column(String)
    titles = Column(String)
    seats = Column(String)
    currentLord = Column(String)
    overlord = Column(String)
    swornMembers = Column(String)

    def __repr__(self):
        return {'HID': self.HID, 'name': self.name, 'slug': self.slug,
                'region': self.region, 'coatOfArms': self.coatOfArms,
                'words': self.words, 'titles': self.titles, 'seats': self.seats,
                'currentLord': self.currentLord, 'overlord': self.overlord,
                'swornMembers': self.swornMembers}