'''This file is used to make API calls to the Coursera API to retrieve Course, Term, and Category information.'''
import requests
import json
from datetime import datetime
import time
import model
import pprint
pp = pprint.PrettyPrinter(indent=4)
import re 

courses = 'https://api.coursera.org/api/catalog.v1/courses?includes=categories&fields=shortName,name,smallIcon,language,instructor,courseFormat,estimatedClassWorkload,recommendedBackground,shortDescription,aboutTheCourse,instructor'
terms = 'https://api.coursera.org/api/catalog.v1/sessions?fields=id,courseId,homeLink,durationString,startDay,startMonth,startYear'
categories = 'https://api.coursera.org/api/catalog.v1/categories?fields=id,name,description'

def get_course():

	r = requests.get(courses)
	print pp.pprint(r.json())
	for element in r.json()['elements']:
		new_course = model.Course(
			id = element['id'],
			course_shortname = element['shortName'],
			course_name = element['name'],
			course_language = element['language'])

		if 'categories' in element['links']:
			for category in element['links']['categories']:
				new_coursecategory = model.CourseCategory(
					category_id = category,
					course_id = element['id'])
			
				model.session.add(new_coursecategory)
			model.session.commit()

		if 'smallIcon' in element.keys():
			new_course.course_icon = element['smallIcon']

		if 'instructor' in element.keys():
			new_course.course_instructor = element['instructor']
			
		if 'courseFormat' in element.keys():
			new_course.course_format = element['courseFormat']
	
		if 'estimatedClassWorkload' in element.keys():
			new_course.course_workload = element['estimatedClassWorkload']

		if 'estimatedClassWorkload' in element.keys():
			if len(element['estimatedClassWorkload']) > 1:
				course_workload_strip_hours = new_course.course_workload.strip()
				course_workload_replace = course_workload_strip_hours.replace(" ", "")
				encode_into_utf = course_workload_replace.encode('utf8')
				course_workload_replace = encode_into_utf.replace("-", ",")
				stripping_all_alphabets = ''.join(c for c in course_workload_replace if c.isdigit() or c in ',')
				split_list = stripping_all_alphabets.split(",")
				try:
					if split_list:
						course_workload_min = int(split_list[0])
						course_workload_max = int(split_list[1])
						new_course.course_workload_min = course_workload_min
						new_course.course_workload_max = course_workload_max
					else:
						new_course.course_workload_min = 'None'
						new_course.course_workload_max = 'None'
				except IndexError:
					course_workload_min = None
					course_workload_max = None
					new_course.course_workload_min = course_workload_min
					new_course.course_workload_max = course_workload_max

		if 'recommendedBackground' in element.keys():
			new_course.course_prerequisites = element['recommendedBackground']
			
		if 'shortDescription' in element.keys():
			new_course.course_description = element['shortDescription']
			

		model.session.merge(new_course)
	model.session.commit()

def get_term_information():

	t = requests.get(terms)
	for element in t.json()['elements']:

		new_term = model.Term(
			id = element['id'],
			course_id = element['courseId'])
		
		if 'durationString' in element.keys():
			new_term.duration = element['durationString']
		if 'startDay' in element.keys():
			new_term.startDay = element['startDay']
		if 'startMonth' in element.keys():
			new_term.startMonth = element['startMonth']
		if 'startYear' in element.keys():
			new_term.startYear = element['startYear']
		if 'homeLink' in element.keys():
			new_term.course_link = element['homeLink']


		model.session.merge(new_term)
	model.session.commit()

def get_category():

	c = requests.get(categories)

	for element in c.json()['elements']:
		new_category = model.Category(
			id = element['id'],
			category_name = element['name'])

		if 'description' in element.keys():
			new_category.category_description = element['description']

		model.session.merge(new_category)
	model.session.commit()

if __name__ == '__main__':
	get_course()
	get_term_information()
	get_category()
