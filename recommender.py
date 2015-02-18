# This is the controller file
from flask import Flask, request, render_template, flash, session, jsonify
import json
import model
import os
import requests
import jinja2


app = Flask(__name__)

APP_SECRET_KEY = os.environ['APP_SECRET_KEY']


@app.route("/")
def welcome():
	"""The welcome page"""
	return render_template("welcome.html")

@app.route("/signup", methods=['GET'])
def show_signup():
    return render_template("signup.html")


@app.route("/signup", methods=['POST'])
def signup():
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    user_age = request.form.get('age')
    user_zipcode = request.form.get('zipcode')

    new_user = model.User(email=user_email, password=user_password)
    if user_age:
        new_user.age = user_age
    if user_zipcode:
        new_user.zipcode = user_zipcode
    
    model.session.add(new_user)

    try:
        model.session.commit()
    except IntegrityError:
        flash("Email already in database. Please try again.")
        return show_signup()

    session.clear()
    flash("Signup successful. Please log in.")
    return show_login()
@app.route("/login", methods=["GET"])
def show_login():
    if session.get('user_email'):
        flash("You have successfully logged out.")
        session.clear()
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    users = model.session.query(model.User)
    try:
        user = users.filter(model.User.email==user_email,
                            model.User.password==user_password
                            ).one()
    except InvalidRequestError:
        flash("That email or password was incorrect.")
        return render_template("login.html")

    session['user_email'] = user.email
    session['user_id'] = user.id
    session['count'] = 0
    
    return render_template("welcome.html")


if __name__ == "__main__":
    app.run(debug=True)

