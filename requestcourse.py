'''This file is used to make API calls to the Coursera API to retrieve Course and Session information.'''
import requests
import json
from datetime import datetime
import time


def get_course():

	for r in elements:
		r = requests.get("https://api.coursera.org/api/catalog.v1/courses?includes=categories,fields=id,shortName,name,language,shortDescription,aboutTheCourse,\
		instructor")
		r.json()

		new_course = model.Course(
		id = elements['id']
		course_shortname = elements['shortName'],
		course_name = elements['name'],
		course_language = elements['language'],
		course_instructor = elements['instructor'],
		course_format = elements['courseFormat'],
		course_workload = elements['estimatedClassWorkload'],
		course_prerequesites = elements['recommendedBackground'],
		course_description = elements['shortDescription'],
		course_categories = elements['links']['categories'])


		model.session.merge(new_course)
	model.session.commit()

def get_session_information():

	for s in elements:
		s = requests.get("https://api.coursera.org/api/catalog.v1/sessions?fields=id,courseId,homelink,status,\
		durationString,startDay")
		r.json()

		new_session = model.Session(
			id = elements['id'],
			course_id = elements['courseId'],
			course_link = elements['homeLink'],
			duration = elements['durationString'],
			startDay = elements['startDay'],
			startMonth = elements['startMonth'],
			startYear = elements['startYear'])


		model.session.merge(new_session)
	model.session.commit()


def get_category():

	for c in elements:
		c = requests.get("https://api.coursera.org/api/catalog.v1/categories?fields=id,name,description")
		r.json()

		new_category = model.Category(
		category_id = elements['id'],
		category_name = elements['name'],
		category_description = elements['description'])

		model.session.merge(new_category)
	model.session.commit()


if __name__ = '__main__':
	get_course()
	get_session_information