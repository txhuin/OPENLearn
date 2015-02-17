'''This file is used to make API calls to the Coursera API to retrieve Course and Session information.'''
import requests
import json
from datetime import datetime
import time
# import model

def get_course():

	r = requests.get("https://api.coursera.org/api/catalog.v1/courses?includes=\
		categories,fields=id,shortName,name,language,shortDescription,aboutTheCourse,\
		instructor")

	# print r

	for element in r.json()['elements']:
		new_course = model.Course(
		id = element['id'],
		course_shortname = element['shortName'],
		course_name = element['name'],
		course_language = element['language'],
		course_instructor = element['instructor'],
		course_format = element['courseFormat'],
		course_workload = element['estimatedClassWorkload'],
		course_prerequesites = element['recommendedBackground'],
		course_description = element['shortDescription'],
		course_categories = element['links']['categories'])


		model.session.merge(new_course)
	model.session.commit()

def get_term_information():

	t = requests.get("https://api.coursera.org/api/catalog.v1/sessions?fields=id,courseId,homelink,status,\
		durationString,startDay")

	for element in t.json()['elements']:
		new_term = model.Term(
			id = element['id'],
			course_id = element['courseId'],
			course_link = element['homeLink'],
			duration = element['durationString'],
			startDay = element['startDay'],
			startMonth = element['startMonth'],
			startYear = element['startYear'])


		model.session.merge(new_term)
	model.session.commit()

def get_category():

	c = requests.get("https://api.coursera.org/api/catalog.v1/categories?fields=id,name,description")
	for element in c.json()['elements']:
		new_category = model.Category(
		id = element['id'],
		category_name = element['name'],
		category_description = element['description'])

		model.session.merge(new_category)
	model.session.commit()


if __name__ == '__main__':
	get_course()
	# get_session_information