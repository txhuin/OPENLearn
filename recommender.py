# This is the controller file
from flask import Flask, render_template, redirect, request, flash, session, redirect, url_for
from flask_oauth import OAuth
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.sql import func
from sqlalchemy import update, distinct
from flask import g
import json
import model
import os
import requests
import jinja2
import sys
from model import Term, Course, CourseCategory

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

@facebook.tokengetter
def get_facebook_oauth_token():
    """Retrieves Oauth token from current session"""
    return session.get('oauth_token')

@app.route("/")
def welcome():
    """The welcome page: This is where the user specifies preferences and submits it to get course listings."""
    categories = model.session.query(model.Category)
    terms = model.session.query(distinct(Term.duration)).filter(Term.duration >= 1, Term.duration <= 20).order_by(Term.duration)
    return render_template("welcome.html", categories=categories, terms=terms)

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
    return display_login()


@app.route("/login", methods=["GET"])
def display_login():
    """This is the login form."""
    if session.get('user_email'):
        flash("You have successfully logged out.")
        session.clear()
    return render_template("login.html")


@app.route("/facebook_login")
def facebook_login():
    """OAuth request to Facebook and callback function if request is successful"""
    next_url = request.args.get('next') or url_for('welcome')
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=next_url, _external=True))


@app.route("/login", methods=["POST"])
def login_user():
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
    return redirect ('/')


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('welcome')
    if resp is None:
        flash('Authentication Error')
        return redirect(next_url)
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    user = model.session.query(model.User).filter(model.User.email == me.data['email']).first()
    flash("You have successfully logged in")
    print ('Logged in as id=%s name=%s redirect=%s') % (me.data['id'], me.data['email'], request.args.get('next'))

    session['user_email'] = me.data['email']
    session['user_id'] = me.data['id']
    return redirect('/')
    if user is None:
        new_user = model.User(email=me.data['email'], password="default")
        model.session.add(new_user)
        model.session.commit()
        
        session['user_email'] = me.data['email']
        session['user_id'] = me.data['id']
    else:
        session['user_email'] = me.data['email']
        session['user_id'] = me.data['id']
    return redirect(next_url)


@app.route("/myprofile")
def display_my_profile():
    """Displays profile of the user that is logged in"""
    if session.get('user_email'):
        email = session.get('user_email')
        users = model.session.query(model.User)
        user = users.filter(model.User.email == email).one()
        return render_template("user_profile.html", user=user)

    else:
        flash("Please log in to view your profile")
        return redirect("/")


@app.route("/logout")
def logout():
    """Logs user out, and clears session. User is returned to homepage.""" 
    # session.pop('user_email')
    # session.pop('user_id')
    session["__invalidate__"] = True
    session.clear()
    return redirect("/")


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
    if session.get('user_email'):
        user_id = session.get("user_id")
        saved_bookmarks = model.session.query(model.BookmarkedCourse).filter(model.BookmarkedCourse.user_id==user_id).all()
        list_of_courses = [bookmark.course for bookmark in saved_bookmarks] 
        return render_template("bookmarkedcourses.html", saved_courses=list_of_courses)

    else:
        flash("Please log in to view your bookmarked courses.")
        return redirect("/")

@app.route("/removefrombookmarkedcourses", methods=['GET'])
def remove_bookmarked_course():
    pass

@app.route("/Randomize", methods=['GET'])
def get_random_course():
    random_course = model.session.query(model.Course).order_by(func.random()).first()
 
    return render_template("randomcourse.html", course=random_course)

@app.route("/Recommend", methods=['GET'])
def get_courses_by_criteria():
    """Queries the database based on user selections, and returns appropriate output"""
    category_chosen = int(request.args.get("category"))
    duration_chosen = request.args.get("duration")
    workload_chosen = request.args.get("workload")

    query = Course.query.join(CourseCategory).filter(CourseCategory.category_id==category_chosen)
        
    #Duration selected 
    #To do: Query database for courses that are more than 20 weeks longworkload_chosen+
    if workload_chosen != '-':
        workload_chosen = int(workload_chosen)
        query = query.filter(model.Course.course_workload_max <= workload_chosen)
        
    if duration_chosen != '-':
        if duration_chosen == "more-than-20":
            query = query.join(Term).filter(Term.duration > 20)
        else:
            duration_chosen = int(duration_chosen)
            query = query.join(Term).filter(Term.duration == duration_chosen)

    return render_template("recommended_courses.html", 
        category_chosen=category_chosen, 
        # category=query.all(), 
        workload_chosen=workload_chosen, 
        duration_chosen=duration_chosen, 
        list_of_courses=query.all())
                                                    
                                          
@app.route('/course/<int:id>')
def display_course_details(id):
    course = model.session.query(model.Course).filter(model.Course.id==id).first()

    return render_template("course_details.html", course=course)


@app.route('/rate_course', methods=['GET'])
def rate_course():
    rating = request.args.get("rating")
    course_id = request.args.get("course_id")
    user_id = session.get("user_id")

    ratings = model.session.query(model.Rating)

    old_rating = ratings.filter(
                    model.Rating.course_id == course_id,
                    model.Rating.user_id == user_id
                    ).first()

    if old_rating:
        old_rating.rating = rating
        model.session.commit()
        flash("update successful")
    
    else:
        new_rating = model.Rating(course_id=course_id, 
                                  user_id=user_id,
                                  rating=rating)
        model.session.add(new_rating)
        model.session.commit()
        flash("Rating successful")

    return display_course_details(id=course_id)

@app.after_request
def add_header(response):
    """
    Deleting cookies, setting cookies to expire and setting cache time in attempt to 
    get app to forget Facebook login credentials 
    """
    if "__invalidate__" in session:
        response.delete_cookie(app.session_cookie_name)
        response.headers['Cache-Control'] = 'public, max-age=0,no-cache, no-store'
        response.set_cookie(session['user_email'], '', expires=0)
    return response

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404
                                                    


if __name__ == "__main__":
    app.run(debug=True, port=5001)

