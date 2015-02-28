# This is the controller file
from flask import Flask, render_template, redirect, request, flash, session, redirect
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.sql import func
from sqlalchemy import update
import json
import model
import os
import requests
import jinja2
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/")
def welcome():
	"""The welcome page: This is where the user specifies preferences and submits it to get course listings."""
	return render_template("welcome.html")

@app.route("/signup", methods=['GET'])
def display_signup():
    """Display sign up form"""
    return render_template("signup.html")

@app.route("/signup", methods=['POST'])
def signup():
    """Once the user submits information on the sign up form, new user is added to database"""
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
def display_login():
    """This is the login form."""
    if session.get('user_email'):
        flash("You have successfully logged out.")
        session.clear()
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    """The user submits their login credentials and is added to the Flask session"""
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
    
    return render_template("welcome.html")


@app.route("/myprofile")
def display_my_profile():
    """Displays profile of the user that is logged in"""
    email = session.get('user_email')
    users = model.session.query(model.User)
    user = users.filter(model.User.email == email).one()
    return render_template("user_profile.html", user=user)


@app.route("/logout")
def logout():
    """Logs user out, and clears session. User is returned to homepage.""" 
    session.clear()
    return redirect("/")

@app.route("/changepassword", methods=['GET'])
def show_change_password():
    """Displays the change password page"""
    return render_template("changepassword.html", email=session['user_email'])

@app.route("/changepassword", methods=['POST'])
def change_password():
    pass
    """Change user password"""
    
@app.route("/bookmarkcourse/<int:id>")   
def bookmark_course(id):
    """Allows user to bookmark course to view later"""
    user_id = session.get("user_id")
    bookmarkedcourse = model.BookmarkedCourse(
        user_id = user_id,
        course_id=id)
    
    model.session.add(bookmarkedcourse)
    model.session.commit()

    return redirect("/bookmarkedcourses")
    
@app.route("/bookmarkedcourses", methods = ['GET'])
def show_bookmarked_courses():
    """Returns list of all courses that the logged in user has bookmarked"""
    user_id = session.get("user_id")
    saved_bookmarks = model.session.query(model.BookmarkedCourse).filter(model.BookmarkedCourse.user_id==user_id).all()
    list_of_courses = [bookmark.course for bookmark in saved_bookmarks] 

    return render_template("bookmarkedcourses.html", saved_courses=list_of_courses)

@app.route("/Randomize", methods=['GET'])
def get_random_course():
    random_course = model.session.query(model.Course).order_by(func.random()).first()
 
    return render_template("randomcourse.html", randomcourse=random_course)

@app.route("/Recommend", methods=['GET'])
def get_courses_by_criteria():
    """Queries the database based on user selections, and returns appropriate output"""
    category_chosen = request.args.get("category")
    duration_chosen = request.args.get("duration")
    workload_chosen = request.args.get("workload")

    if category_chosen!= None and duration_chosen == '-' and workload_chosen == '-':
        get_category = model.session.query(model.Category).filter(model.Category.category_name==category_chosen).first()
        get_courses_associated_with_category = model.session.query(model.CourseCategory).filter(model.CourseCategory.category_id==get_category.id).all()
        list_of_course_objects_by_category = [course.course_assoc for course in get_courses_associated_with_category]
    
    #Duration selected 
    #To do: Query database for courses that are more than 20 weeks longworkload_chosen+
    elif category_chosen != None and duration_chosen == '-' and workload_chosen != '-':
        workload_chosen = int(workload_chosen)
        get_category = model.session.query(model.Category).filter(model.Category.category_name==category_chosen).first()
        get_courses_associated_with_category = model.session.query(model.CourseCategory).filter(model.CourseCategory.category_id==get_category.id).all()
        list_of_course_objects_by_category = [course.course_assoc for course in get_courses_associated_with_category]

    elif category_chosen != None and workload_chosen == '-' and duration_chosen != '-':
        # get_category = model.session.query(model.Category).filter(model.Category.category_name==category_chosen).first()
        # get_courses_associated_with_category = model.session.query(model.CourseCategory).filter(model.CourseCategory.category_id==get_category.id).all()
        # list_of_course_objects_by_category = [course.course_assoc for course in get_courses_associated_with_category]
        get_courses_associated_with_duration = model.session.query(model.Term).filter(model.Term.duration==duration_chosen).all()
        list_of_course_objects_by_category = [course.course_association for course in get_courses_associated_with_duration]
        print list_of_course_objects_by_category
        print '(@*#@*#@*#@(*#'
        print '(@*#@*#@*#@(*#'
        print '(@*#@*#@*#@(*#'
        print '(@*#@*#@*#@(*#'
        print '(@*#@*#@*#@(*#'
        # get_category = model.session.query(model.Term).filter(model.Term.duration==duration_chosen).all()
        # get_courses_associated_with_duration = model.session.query(model.Course).filter(model.Course.id==get_category.course_id).all()
        # list_of_courses_by_category = [course.course_name for course in get_courses_associated_with_duration]

        # if duration_chosen == "More than 20 weeks":
        #     all_courses1= []
        #     course1= model.session.query(model.Course.course_name).filter(model.Course.id==329).all()
        #     course2 = model.session.query(model.Course.course_name).filter(model.Course.id==444).all()
        #     course3 = model.session.query(model.Course.course_name).filter(model.Course.id==449).all()
        #     course4 = model.session.query(model.Course.course_name).filter(model.Course.id==503).all()
        #     course5 = model.session.query(model.Course.course_name).filter(model.Course.id==584).all()
        #     all_courses1.append(course1)
        #     all_courses1.append(course2)
        #     all_courses1.append(course3)
        #     all_courses1.append(course4)
        #     all_courses1.append(course5)
        #     print all_courses1
            
        # else:
        #     get_duration = model.session.query(model.Term.course_id).filter(model.Term.duration==duration_chosen).all()
        #     all_courses1 = []
        #     for i in get_duration:
        #         get_course_name = model.session.query(model.Course.course_name).filter(model.Course.id==i[0]).all()
        #         all_courses1.extend(get_course_name)
        #     encoded_durations = [[s.encode('utf8') for s in get_course_name] for get_course_name in all_courses1]
        #     duration_results = [item for sublist in encoded_durations for item in sublist]
        
    # elif workload_chosen == '-' and duration_chosen != '-':
        
    #     get_workload = model.session.query(model.Course.course_name).filter(model.Course.course_workload_max <= workload_chosen).all() 
    #     get_workload_list = [item[0] for item in get_workload]
    #     encode_workload_list = [s.encode("utf8") for s in get_workload_list]

    return render_template("recommended_courses.html", category=list_of_course_objects_by_category, workload_chosen=workload_chosen)
                                                    
                                          
@app.route('/course/<int:id>')
def display_course_details(id):
    course = model.session.query(model.Course).filter(model.Course.id==id).first()

    return render_template("course_details.html", course=course)
                                                     
                                                
                                                    
#To-do:
# Add a details option to each course rendered
# Add Facebook OAuth login functionality
# Add rate this course functionality
# Add course takers also enjoyed (Nearest Neighbour algorithm)
# Prediction of rating for each course? (Pearson coefficient)
# Migrate to Postgresql for deployment


    



if __name__ == "__main__":
    app.run(debug=True, port=5001)

