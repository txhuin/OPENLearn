'''This file is used to make API calls to the Coursera API to retrieve Course and Session information.'''
import requests
import json
from datetime import datetime
import time


def get_course():

	for r in elements:
		r = requests.get("https://api.coursera.org/api/catalog.v1/courses?includes=fields=id,shortName,name,language,shortDescription,aboutTheCourse,\
		instructor")

	new_course = model.Course(
		id = elements['id']
		course_shortname = elements['shortName']
		course_name = elements['name']
		course_language = elements['language']
		course_instructor = elements['instructor']
		course_format = elements['courseFormat']
		course_workload = elements['estimatedClassWorkload']
		course_prerequesites = elements['recommendedBackground']
		course_description = elements['shortDescription']
		course_categories = elements['links']['categories'] )







		model.session.merge(new_course)
	model.session.commit()

def get_session_information():

	for s in elements:
		s = requests.get("https://api.coursera.org/api/catalog.v1/sessions?fields=id,courseId,homelink,status,\
		durationString,startDay")
		r.json()

		new_session = model.Session(
			id = 
		course)


def get_category():

	for c in elements:
	c = requests.get("https://api.coursera.org/api/catalog.v1/categories")
	category_id = elements['id']




if __name__ = '__main__':
	get_course()
	get_session_information