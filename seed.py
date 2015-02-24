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
				course_workload_replace = course_workload_strip_hours.replace("-", ",")
				print '****************'
				print '****************'
				print '****************'
				print '****************'
				print course_workload_replace
				print '****************'
				print '****************'
				print '****************'
				print '****************'
				print '****************'
				# course_workload_strip_whitespace = course_workload_replace.strip("abcdefghijklmnopqrstuvwxyz/()")
				# course_workload_strip_whitespace1 = course_workload_strip_whitespace.strip("hours/week")
				print '****************'
				print '****************'
				print '****************'
				print '****************'
			
				print '****************'
				print '****************'
				print '****************'
				print '****************'
				print '****************'
				# chars = "abcdefghijklmnopqrstuvwxyz-"
				stripping_all_characters = ''.join(c for c in course_workload_replace if c.isdigit() or c==',')
				# pattern = re.sub("[^0-9]", "", course_workload_replace)
				# print pattern
				print stripping_all_characters
				# print type(course_workload_strip_whitespace1)
				# course_workload_split = course_workload_strip_whitespace.split("-")
				# pattern = re.compile('\w', re.UNICODE)
				# remove_using_regex = ''.join(pattern.findall(course_workload_replace))
				# print course_workload_split
				# print type(course_workload_split)
				# print '****************'
				# print '****************'
				# print '****************'
				# print '****************'
				# print '****************'
				course_workload_list = filter(None, stripping_all_characters)
				# split = pattern.split("-")
				# split_into_two = map(int, str(course_workload_list))
				# print split_into_two
				# print '****************'
				# print '****************'
				# print '****************'
				# print '****************'
				# print course_workload_list
				# print type(course_workload_list)
				# print '****************'
				# print '****************'
				# print '****************'
				# print '****************'
				# print '****************'
				
				if course_workload_list:
					course_workload_min = float(int(course_workload_list[0]))
					new_course.course_workload_min = course_workload_min
					# course_workload_max_str_list = map(str, split_into_two)
					# # if len(course_workload_list) < 2:
					# 	new_course.course_workload_max = course_workload_max_str_list[1]
					# elif len(course_workload_list) :
					# 	course_workload_max_concat = course_workload_max_str_list[1] + course_workload_max_str_list[2]
					# 	new_course.course_workload_max = course_workload_max_concat
				
					# course_workload_max = float()
		
					# new_course.course_workload_max = 
				else:
					new_course.course_workload_min = 'None'
					# new_course.course_workload_max = 'None'
			
		# if course_workload_min2:
		# 	if len(element['estimatedClassWorkload']) > 1:
		# 		new_course.course_workload_min= float(course_workload_min2[0])
		# 		new_course.course_workload_max= float(course_workload_min2[1])


			# course_workload_max = new_course.course_workload.strip()

		if 'recommendedBackground' in element.keys():
			new_course.course_prerequisites = element['recommendedBackground']
			
		if 'shortDescription' in element.keys():
			new_course.course_description = element['shortDescription']
			

		model.session.merge(new_course)
	model.session.commit()

def get_term_information():

	t = requests.get(terms)
	# print pp.pprint(t.json())
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
