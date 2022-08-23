from sqlalchemy import Column, Integer, String, asc
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
import re

from models.movie import Movie
from settings import Base, Engine


class Winners(Base):
    __tablename__ = 'Winners'

    id = Column(Integer,  primary_key=True)
    producer = Column('producer', String(30))
    interval = Column('interval', Integer)
    previousWin = Column('previousWin', Integer)
    followingWin = Column('followingWin', Integer)

    def __init__(self, producer, interval, previousWin, followingWin):
        super(Winners, self).__init__()
        self.producer = producer
        self.interval = interval
        self.previousWin = previousWin
        self.followingWin = followingWin


def calculate_winner():
    session = sessionmaker(bind=Engine)()
    session.query(Winners).delete()
    movies = session.query(Movie).filter(Movie.winner == True).order_by(asc(Movie.year)).all()
    for movie in movies:
        for producer in re.split(' and |, ', movie.producers):

            winner_in_db = session.query(Winners).filter(Winners.producer == producer).order_by(desc(Winners.id)).all()
            if len(winner_in_db) == 0:
                winner = Winners(producer,
                                 None,
                                 movie.year,
                                 None)
                session.add(winner)

            elif winner_in_db[0].followingWin is None:
                session.query(Winners).filter(Winners.id == winner_in_db[0].id).update({'followingWin': movie.year,
                                                                                        'interval': movie.year - winner_in_db[0].previousWin})
            else:
                winner = Winners(producer,
                                 winner_in_db[0].followingWin - movie.year,
                                 winner_in_db[0].followingWin,
                                 movie.year)
                session.add(winner)

            session.commit()
    session.close()
