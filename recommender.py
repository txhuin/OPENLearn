# This is the controller file
from flask import Flask, request, render_template
from flask import session as user_session
import json
from flask import jsonify
import os





app = __Flask__(name)

APP_SECRET_KEY = 


@app.route("/")
def welcome():
	"""The welcome page"""
