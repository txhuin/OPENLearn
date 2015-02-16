from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy import create_engine, Boolean, Table, Text
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session


COURSESDB = os.environ.get('COURSESDB')
engine = create_engine(COURSESDB, echo=True)
session = scoped_session(sessionmaker(bind=engine, 
                                      autocommit=False,
                                      autoflush=False))


Base = declarative_base()
Base.query = session.query_property


class 