from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy import create_engine, Boolean, Table, Text
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
import pickle


COURSESDB = os.environ.get('COURSESDB')
engine = create_engine(COURSESDB, echo=True)
session = scoped_session(sessionmaker(bind=engine, 
                                      autocommit=False,
                                      autoflush=False))


Base = declarative_base()
Base.query = session.query_property


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	email = Column(String(64), nullable=False)
	password = Column(String(64), nullable=False)



class BookmarkedCourse(Base):
	__tablename__ = "bookmarkedcourses"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))

	


class Course(Base):
	__tablename__ = "courses"

	course_id = Column(Integer, primary_key=True)
	short_name = Column(String(200), nullable=False)
	category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
	language = Column(String(200))
	instructor = Column(String(90))
	format = Column()
	workload = Column()
	prerequesites = Column()
	description = Column()

class Term(Base):
	__tablename__ = "terms"

	id = Column(Integer, primary_key=True)
	course_id = Column(Integer, ForeignKey()),
	course_link = Column(Integer, primary_key=True)
	duration =  Column(Integer, primary_key=True)
	startDay =  Column(Integer, primary_key=True)
	startMonth =  Column(Integer, primary_key=True)
	startYear =  Column(Integer, primary_key=True)		

class Category(Base):
	__tablename__ = "categories"

	category_id = Column(Integer, primary_key=True)
	category_name = Column
	category_description = Column()





def main():
	Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()