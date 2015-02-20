# This is the controller file
from flask import Flask, render_template, redirect, request, flash, session
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.sql import func
from sqlalchemy import update
import json
import model
import os
import requests
import jinja2


app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

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

    new_user = model.User(email=user_email, password=user_password)
    
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
    return render_template("login.html")
    if session.get('user_email'):
        flash("You have successfully logged out.")
        session.clear()
   
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

# @app.route("/changepassword")
# def show_change_password():
#     """Displays the change password page"""
#     return render_template("changepassword.html", email=session['email'])

# @app.route("/changepassword", methods=['POST'])
# def change_password():
#     pass
#     """Change user password"""
    

# @app.route("/bookmarkcourse")
# def bookmark_course():
#     pass
#     # user_id = model.session.query(User).filter_by(email=session_email).first().id
#     # savedcourse = BookmarkedCourse.

#     # model.session.add()
    

# @app.route("/bookmarkedcourses")
# def show_bookmarked_courses():
#     pass
#     """Show all the bookmarked courses from the database"""
    

# @app.route("/randomize")
# def randomize():
#     pass
# """The app generates a course based on random course generator"""



@app.route("/Recommend", methods=['GET', 'POST'])
def get_courses_by_criteria():
    """Queries the database based on user selections, and returns appropriate output"""
    category_chosen = request.form.get("chosencategory")
    category = model.session.query(model.Category)
    get_category = category.filter(model.Category.category_name==category_chosen).all()
    
    duration_chosen = request.form.get("chosenduration")
    durations = model.session.query(model.Term)
    get_duration = durations.filter(model.Term.duration==duration_chosen).all()

    workload_chosen = request.form.get("chosenworkload")
    workload = model.session.query(model.Course)
    get_course = courses.filter(model.Course.course_workload=workload_chosen)

    return render_template("recommended_courses.html", chosencategory=category_chosen, durationchosen=duration_chosen, terms=durations)

if __name__ == "__main__":
    app.run(debug=True)

