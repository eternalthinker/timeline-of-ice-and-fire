from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import app

Base = declarative_base()

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


if __name__ == '__main__':

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
    Session = sessionmaker(bind=engine) 
    session = Session()


    for q in session.query(Episode).filter(Episode.EID == '0101'):
        record = dict(q.__dict__)
        record.pop('_sa_instance_state')
        print(type(record))

    session.close()