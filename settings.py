from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Engine = create_engine('sqlite://')

Base = declarative_base()


