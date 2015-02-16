'''This file is used to make API calls to the Coursera API.'''
import requests
import json


def get_course():


	r = requests.get(" https://api.coursera.org/api/catalog.v1/courses/")
	r.json()

	new_course = 










	model.session.merge(new_course)
	model.session.commit()



if __name__ = '__main__':
	get_course()