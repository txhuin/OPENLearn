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


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	email = Column(String(64), nullable=False)
	password = Column(String(64), nullable=False)



class BookmarkedCourse(Base):
	__tablename__ = "bookmarkedcourses"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	# course = Column


class Course(Base):
	__tablename__ = "courses"

	course_id = Column(Integer, primary_key=True)








def main():
	Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()