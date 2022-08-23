from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
import csv

from settings import Base, Engine


class Movie(Base):
    __tablename__ = 'Filmes'

    id = Column(Integer,  primary_key=True)
    year = Column('year', Integer)
    title = Column('title', String(40))
    studios = Column('studios', String(40))
    producers = Column('producers', String(30))
    winner = Column('winner', Boolean)

    def __init__(self, year, title, studios, producers, winner):
        super(Movie, self).__init__()
        self.year = year
        self.title = title
        self.studios = studios
        self.producers = producers
        self.winner = winner


def load_movies(movie_csv):
    session = sessionmaker(bind=Engine)()
    file = open(movie_csv)
    lines = csv.reader(file, delimiter=';')
    next(lines)
    try:
        for line in lines:
            movie = Movie(int(line[0]),
                          line[1],
                          line[2],
                          line[3],
                          True if line[4] == 'yes' else False)
            session.add(movie)
        session.commit()
    finally:
        session.close()

