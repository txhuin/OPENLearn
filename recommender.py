# This is the controller file
from flask import Flask, render_template, redirect, request, flash, session, redirect, url_for, jsonify
from flask_oauth import OAuth
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.sql import func
from sqlalchemy import update, distinct, or_
from flask import g
import json
import redis
import model
import os
import requests
import jinja2
import sys
from model import Term, Course, CourseCategory, BookmarkedCourse, Category, User, Review, Rating
from datetime import date

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
# app.redis = redis.StrictRedis(host=)

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
    workloads = model.session.query(model.Course)
    return render_template("welcome.html", categories=categories, terms=terms, workloads=workloads)


@app.route("/signup", methods=['GET'])
def display_signup():
    """Display sign up form"""
    return render_template("signup.html")

@app.route("/signup", methods=['POST'])
def signup():
    """Once the user submits information on the sign up form, new user is added to database"""
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    user_nickname = request.form.get('nickname')

    new_user = model.User(email=user_email, password=user_password, nickname=user_nickname)
    
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

    users = model.session.query(User)
    try:
        user = users.filter(User.email == user_email,
                            User.password == user_password
                            ).one()
    except InvalidRequestError:
        flash("That email or password was incorrect.")
        return render_template("login.html")

    session['user_email'] = user.email
    session['user_id'] = user.id
    session['user_nickname'] = user.nickname
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
    user = model.session.query(User).filter(User.email == me.data['email']).first()
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
        users = model.session.query(User)
        user = users.filter(User.email == email).one()
        heading = "My Profile"

        bookmarks = model.session.query(BookmarkedCourse)
        user_bookmarks = bookmarks.filter(BookmarkedCourse.user_id == user.id).all()
      
        return render_template("myprofile.html", user=user, heading=heading)

    else:
        flash("Please log in to view your profile")
        return redirect("/")


@app.route("/logout")
def logout():
    """Logs user out, and clears session. User is returned to homepage.""" 
    session["__invalidate__"] = True
    session.clear()
    return redirect("/")

@app.route("/all_users")
def show_all_users():
    users = model.session.query(model.User)
    user_list = users.filter(model.User.email.isnot(None)).all()
    return render_template("all_users.html", users=user_list)

    
@app.route("/user_profile", methods=["GET"])
def show_user_profile():
    user_in_session = session.get('user_id')
    # user_id = model.session.query(User).filter(User.id == user_in_session).first()
    #user logged in 

    nickname = request.args.get("nickname")   
    users = model.session.query(User)
    user = users.filter(User.nickname == nickname).one()
    heading = "%s's Profile" % (nickname)

    ratings = model.session.query(Rating)
    user_ratings = ratings.filter(Rating.user_id == user.id).all()

    bookmarks = model.session.query(BookmarkedCourse)
    user_bookmarks = bookmarks.filter(BookmarkedCourse.user_id == user.id).all()

    friendship = model.session.query(model.Friendship).filter(model.Friendship.user_id == user_in_session, model.Friendship.pending==False).all()
    friendship2 = model.session.query(model.Friendship).filter(model.Friendship.friend_id == user.id, model.Friendship.pending==False).all()
    var = False
    if friendship and friendship2:
        var = True


 
    return render_template("user_profile.html", user=user, 
                                                heading=heading,
                                                ratings=user_ratings,
                                                bookmarks=user_bookmarks,
                                                var=var
                                            )


@app.route('/send_friend_request/<nickname>', methods=['GET'])
def send_friend_request(nickname):
    user = User.query.filter_by(nickname=nickname).first()

    if user is None:
        flash('User %s not found.' % nickname)
        return redirect("/myprofile")

    elif user.nickname == session.get('user_nickname'):
        flash('You can\'t friend yourself!')
        return redirect("/myprofile")

    else: 
        friend_request = model.session.query(model.Friendship)
        user_as_sender_request = friend_request.filter(model.Friendship.user_id == session.get('user_id'), model.Friendship.friend_id == user.id).first()
        friend_as_sender_request = friend_request.filter(model.Friendship.user_id == user.id, model.Friendship.friend_id == session.get('user_id')).first()

        if user_as_sender_request == None and friend_as_sender_request == None:
            new_friendship = model.Friendship(user_id=session.get('user_id'), friend_id=user.id)
            model.session.add(new_friendship)
            model.session.commit()
            flash("Friend request send to %s" % nickname) 
            return redirect("/myprofile")

        else:
            flash("You already have a friendship with this person.")
            return redirect("/myprofile")


@app.route('/friend_requests')
def friend_request():
    query_database = model.session.query(model.Friendship)
    query_user = query_database.filter(model.Friendship.user_id == session.get('user_id'), model.Friendship.pending == True).all()
    query_user1 = query_database.filter(model.Friendship.friend_id == session.get('user_id'), model.Friendship.pending == True).all()
    friendslist = []
    for i in query_user1:
        friend_object = model.session.query(User).filter(User.id == i.user_id).all()
        friendslist.extend(friend_object)

    return render_template("friend_requests.html", user_friend_requests=query_user, friend_requests_for_user=query_user1, friendslist=friendslist)


@app.route('/friends')
def list_of_friends():
    query_friendship = model.session.query(model.Friendship.user_id).filter(model.Friendship.friend_id == session.get("user_id"), model.Friendship.pending == False )
    query_user_as_sender = model.session.query(model.Friendship.friend_id).filter(model.Friendship.user_id == session.get("user_id"), model.Friendship.pending == False )
    list_of_friends = []
    list_of_friends.extend(query_friendship)
    list_of_friends.extend(query_user_as_sender)
    list_of_friends1 = [i[0] for i in list_of_friends]
    list_of_user_objects = []
    for i in list_of_friends1:
        user = model.session.query(User).filter(User.id == i).all()
        list_of_user_objects.extend(user)

    return render_template("friends.html", friends=list_of_user_objects)

@app.route('/accept_request/<int:friend_id>')
def accept_request(friend_id):
    query_database = model.session.query(model.Friendship)
    friendships = query_database.filter(model.Friendship.friend_id == session.get('user_id'), model.Friendship.user_id == friend_id)
    first_f = friendships.first()

    new_friendship =friendships.update({'pending': False})

    return redirect ("/friends")

@app.route('/deny_request/<int:friend_id>')
def deny_request(friend_id):
    query_database = model.session.query(model.Friendship)
    friendships = query_database.filter(model.Friendship.friend_id == session.get('user_id'), model.Friendship.user_id == friend_id)
    first_f = friendships.first()

    delete_friend_request = friendships.delete()

    return redirect('/')


@app.route("/bookmarkcourse/<int:id>")   
def bookmark_course(id):
    """Allows user to bookmark course to view later"""
    if session.get('user_email'):
        user_id = session.get("user_id")
        bookmarkedcourse = model.BookmarkedCourse(user_id = user_id, course_id=id)
        model.session.add(bookmarkedcourse)
        model.session.commit()
        activityofuser = model.Activity(user_id=user_id, activity_type="bookmarked", object_id=id)
        model.session.add(activityofuser)
        model.session.commit()
        flash("Course successfully added")
        return redirect("/mybookmarkedcourses")

    else:
        flash("You need to log in to do that")
        return redirect("/mybookmarkedcourses")

    
@app.route("/mybookmarkedcourses", methods = ['GET'])
def show_own_bookmarked_courses():
    """Returns list of all courses that the logged in user has bookmarked"""
    if session.get('user_email'):
        user_id = session.get("user_id")
        saved_bookmarks = model.session.query(BookmarkedCourse).filter(BookmarkedCourse.user_id == user_id).all()
        list_of_courses = [bookmark.course for bookmark in saved_bookmarks] 
        return render_template("bookmarkedcourses.html", saved_courses=list_of_courses)

    else:
        flash("Please log in to view your bookmarked courses.")
        return redirect("/")

@app.route("/othersbookmarkedcourses/<int:id>", methods=['GET'])
def show_other_users_bookmarked_courses(id):
    # if a user and another user are friends allow user to view the other user's bookmarked courses. 
    query_friendship = model.session.query(model.Friendship).filter(model.Friendship.friend_id == session.get("user_id"), model.Friendship.pending == False, model.Friendship.user_id == id ).first()
    query_user_as_sender = model.session.query(model.Friendship).filter(model.Friendship.user_id == session.get("user_id"), model.Friendship.pending == False, model.Friendship.friend_id == id ).first()
    user = model.session.query(model.User).filter(model.User.id == id).first()

    if query_friendship != None or query_user_as_sender != None:
        user =  model.session.query(User).filter(User.id == id).first()
        saved_bookmarks = model.session.query(BookmarkedCourse).filter(BookmarkedCourse.user_id == id).all()
        list_of_courses = [bookmark.course for bookmark in saved_bookmarks] 
        
        return render_template("otherbookmarkedcourses.html", saved_courses=list_of_courses, user=user)

    else:
        flash("You are not this user's friend. Send them a friend request in order to view their bookmarked courses.")
        return render_template("user_profile.html", user=user)
    

@app.route("/removefrombookmarkedcourses/<int:id>", methods=['GET'])
def remove_bookmarked_course(id):
    user_id = session.get("user_id")
    delete_bookmark = model.session.query(BookmarkedCourse).filter(BookmarkedCourse.course_id==id).delete()
    saved_bookmarks = model.session.query(BookmarkedCourse).filter(BookmarkedCourse.user_id==user_id).all()
    list_of_courses = [bookmark.course for bookmark in saved_bookmarks] 

    return render_template("bookmarkedcourses.html", saved_courses=list_of_courses)

@app.route("/Randomize", methods=['GET'])
def get_random_course():
    random_course = model.session.query(Course).order_by(func.random()).first()
 
    return render_template("randomcourse.html", course=random_course)

@app.route("/Recommend", methods=['GET'])
def get_courses_by_criteria():
    """Queries the database based on user selections, and returns appropriate output"""
    category_chosen = int(request.args.get("category"))
    duration_chosen = request.args.get("duration")
    workload_chosen = request.args.get("workload")

    blue = model.session.query(Category).filter(Category.id == category_chosen).first()

    query = Course.query.join(CourseCategory).filter(CourseCategory.category_id == category_chosen)
        
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
        list_of_courses=query.all(), duration_chosen=duration_chosen, workload_chosen=workload_chosen, cat=blue)
                                                    
                                          
@app.route('/course/<int:id>')
def display_course_details(id):
    course = model.session.query(Course).filter(Course.id == id).first()
    terms = model.session.query(Term).filter(Term.course_id == id).first()
    review = model.session.query(Review).filter(Review.course_id == id)

    return render_template("course_details.html", course=course, 
        terms=terms, review=review.all())


@app.route('/rate_course', methods=['GET'])
def rate_course():
    rating = request.args.get("star")
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
            user_id=user_id, rating=rating)
        model.session.add(new_rating)
        model.session.commit()
        
        flash("Rating successful")

    return display_course_details(id=course_id)

@app.route('/writereview/<int:id>', methods=['GET'])
def display_review_form(id):
    if session.get('user_email'):
        course_id = int(id)
        user_id = session.get("user_id")

        course = model.session.query(Course).filter(Course.id == id).first()
        reviews = model.session.query(model.Review)
        

        old_review = reviews.filter(
                    model.Review.course_id == course_id,
                    model.Review.user_id == user_id
                    ).first()

        if old_review:
                review = old_review.review 
                return render_template("review_form.html", course=course, review=review)

        else:
            return render_template("review_form.html", course=course)

    else:
        flash("You need to log in to do that")
        return redirect('/')

@app.route('/submitreview/<int:id>', methods=['GET'])
def submit_review(id):
    review = request.args.get("review")
    course_id = int(id)
    user_id = session.get("user_id")

    new_review = model.Review(course_id=course_id, user_id=user_id, review=review)
    model.session.add(new_review)
    model.session.commit()

    flash("Review successfully added.")
    return redirect("/mybookmarkedcourses")

@app.route('/updatereview/<int:id>', methods=['GET'])
def update_review(id):

    review = request.args.get("review")
    course_id = int(id)
    user_id = session.get("user_id")
    delete_bookmark = model.session.query(Review).filter(Review.course_id, Review.user_id == course_id, user_id).delete()

@app.route('/aboutme', methods=['POST'])
def about_me():
    if session.get('user_email'):
        about_me = request.form["aboutme"]
        user_id = session.get("user_id")
     
        model.session.query(User).filter(User.id == user_id).update({'about_me': about_me})
        model.session.commit()

        return redirect('/myprofile')

@app.route('/edit', methods=['GET'])
def edit_about_me():
    user_id = session.get("user_id")
    user = model.session.query(User).filter(User.id == user_id).update({'about_me': '' })
    model.session.commit()

    return redirect('/myprofile')   

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

@app.route('/api/v1.0/courses', methods=['GET'])
def api_get_courses():
    if request.method == 'GET':
        results = model.session.query(Course).all()

        json_results =[]
        for result in results:
            d = {'course_shortname': result.course_shortname,
                 'course_name': result.course_name,
                 'course_language': result.course_language,
                 'course_instructor': result.course_instructor
            }
            json_results.append(d)

        return jsonify(items=json_results)


@app.route('/api/v1.0/courses/<int:course_id>', methods=['GET'])
def api_get_course_by_id(course_id):
    if request.method == 'GET':
        result = model.session.query(Course).filter_by(id=course_id).first()
        json_result = {
                 'course_shortname': result.course_shortname,
                 'course_name': result.course_name,
                 'course_language': result.course_language,
                 'course_instructor': result.course_instructor,
                 'course_workload' : result.course_workload,
                 'course_prerequisites': result.course_prerequisites
            }

        return jsonify(items=json_result)
        


@app.route('/api/v1.0/reviews/', methods=['GET'])
def api_get_reviews():
    if request.method == 'GET':

        results = model.session.query(Review).all()
        json_results = []
        for result in results:
            d = {
            'course_id': result.course_id,
            'user_id': result.user_id,
            'review': result.review
            }

            json_results.append(d)

        return jsonify(items=json_results)


@app.route('/api/v1.0/reviews/<int:course_id>', methods=['GET'])
def api_get_review_by_course(course_id):
    if request.method == 'GET':
        result = model.session.query(Review).filter_by(course_id=course_id).all()

        json_result = {
        'course_id': result.course_id,
        'user_id': result.user_id,
        'review': result.review
        }

        return jsonify(items=json_result)


                                                  
if __name__ == "__main__":
    app.run(debug=True, port=5001)
