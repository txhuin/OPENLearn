from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy import create_engine, Boolean, Table, Text
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
import pickle



engine = create_engine("sqlite:///courses.db", echo=True)
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
	course = Column(String(500), nullable=False)

	user = relationship("User", backref=backref("bookmarkedcourses", order_by=id))

class Course(Base):
	__tablename__ = "courses"

	id = Column(Integer, primary_key=True)
	course_shortname = Column(String(200), nullable=False)
	course_name = Column()
	# category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
	course_language = Column(String(200))
	course_instructor = Column(String(90))
	course_format = Column()
	course_workload = Column()
	course_prerequesites = Column()
	course_description = Column()
	course_categories = Column

class Term(Base):
	__tablename__ = "terms"

	id = Column(Integer, primary_key=True)
	course_id = Column(Integer, ForeignKey()),
	course_link = Column(String(1000))
	duration =  Column(Integer, primary_key=True)
	startDay =  Column(Integer, primary_key=True)
	startMonth =  Column(Integer, primary_key=True)
	startYear =  Column(Integer, primary_key=True)		

class Category(Base):
	__tablename__ = "categories"

	id = Column(Integer, primary_key=True)
	category_name = Column
	category_description = Column()

class CourseCategory(Base):
	__tablename__ = "course_categories"
	id = Column(Integer, primary_key=True)
	category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
	course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)



def main():
	Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()