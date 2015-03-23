from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, PickleType
from sqlalchemy import create_engine, Boolean, Table, Text
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from hashlib import md5
import urllib, hashlib

engine = create_engine("sqlite:///mooc.db", echo=True)
session = scoped_session(sessionmaker(bind=engine, 
                                      autocommit=False,
                                      autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

# Friendships are many to many, self-referential relationships. 
# A user can have many friends. A user can also be a friend.
class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	email = Column(String(1000), nullable=False, unique=True)
	nickname = Column(String(64), nullable=True, unique=True)
	password = Column(String(1000), nullable=False)
	about_me = Column(String(600), nullable=True)
	last_seen = Column(DateTime)

	# this will be where user did the friending
	friendships1 = relationship('Friendship',primaryjoin='User.id==Friendship.user_id', lazy='dynamic')

	# this will be where user was the recipient of the friending
	friendships2 = relationship('Friendship',primaryjoin='User.id==Friendship.friend_id', lazy='dynamic')

	def avatar(self, size):
		default = "identicon"
		gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
		gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
		return gravatar_url


class Friendship(Base):
	__tablename__ = "friendships"

	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	friend_id = Column(Integer, ForeignKey("users.id"))
	pending = Column(Boolean, default=True)

	user = relationship('User', foreign_keys='Friendship.user_id', primaryjoin='Friendship.user_id==User.id')
	friend = relationship('User', foreign_keys='Friendship.friend_id', primaryjoin='Friendship.friend_id==User.id')

class BookmarkedCourse(Base):
	__tablename__ = "bookmarkedcourses"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	course_id = Column(String(500), ForeignKey('courses.id'))

	user = relationship("User", backref=backref("bookmarkedcourses", order_by=id))
	course = relationship("Course", backref=backref("bookmarkedcourses", order_by=id))


class Course(Base):
	__tablename__ = "courses"

	id = Column(Integer, primary_key=True)
	course_shortname = Column(String(200), nullable=False)
	course_name = Column(String(500), nullable=False)
	course_icon = Column(String(1000))
	course_language = Column(String(200))
	course_instructor = Column(String(90), nullable=True)
	course_format = Column(String(10000), nullable=True)
	course_workload = Column(String(1000), nullable=True)
	course_workload_max = Column(Integer, nullable=True)
	course_workload_min = Column(Integer, nullable=True)
	course_prerequisites = Column(String(1000), nullable=True)
	course_description = Column(String(10000), nullable=True)
	course_categories = relationship("CourseCategory", backref="course")



class Term(Base):
	__tablename__ = "terms"

	id = Column(Integer, primary_key=True)
	course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
	course_link = Column(String(1000), nullable=True)
	duration =  Column(Integer, nullable=True)
	startDay =  Column(Integer, nullable=True)
	startMonth =  Column(Integer, nullable=True)
	startYear =  Column(Integer, nullable=True)	

	course_association = relationship("Course", backref=backref("terms", order_by=id))	


class Category(Base):
	__tablename__ = "categories"

	id = Column(Integer, primary_key=True, nullable=False)
	category_name = Column(String(500), nullable=False)
	category_description = Column(String(5000), nullable=True)

class CourseCategory(Base):
	__tablename__ = "course_categories"

	id = Column(Integer, primary_key=True)
	category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
	course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

	course_assoc = relationship("Course", backref=backref("course_category_names", order_by=id))

class Rating(Base):
	__tablename__ = "ratings"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
	rating = Column(Integer, nullable=True)

	user = relationship("User", backref=backref("ratings", order_by=id))
	course = relationship("Course", backref=backref("ratings", order_by=id))

class Review(Base):
	__tablename__ = "reviews"

	id = Column(Integer, primary_key=True)
	course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	review = Column(String(10000), nullable=True)

	user = relationship("User", backref=backref("reviews", order_by=id))
	course = relationship("Course", backref=backref("reviews", order_by=id))

class Activity(Base):
	__tablename__ = "activities"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	activity_type = Column(String)
	object_id = Column(Integer, ForeignKey("courses.id"))

	# User activity types: rated a course, reviewed a course, bookmarked a course
	# Object types: course

class Comment(Base):
	__tablename__ = "comments"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
	comment = Column(String(10000))







