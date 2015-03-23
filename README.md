# OPENLearn

OPENLearn is a social cataloguing platform that offers users the ability to explore the plethora of Massive Open Online Courses.  The database includes courses from Coursera's API. The decision to user Coursera's API was made as it offers over 900 courses spanning a diverse range of subjects. 

On OPENLearn, users can filter for courses by category, by session length, and by the number of hours they are willing to dedicate to coursework. Via the search results, users can explore details of each course such as the course format, the course description, and the prerequisites. They are then provided an external link to join the course. 

If users are interested in a course, but perhaps aren't interested in joining it right away, they can bookmark it, for later viewing. 

A fun feature of the app is the Randomize tab. If users are unsure of what course they want to take, they can also hit the Randomize button resulting in a suggestion for a random course. 

The app has real world applications as it attempts to reduce the high attrition rate of online course takers by adding a social networking dimension to online learning. The app also allows users to rate courses, and submit reviews for online courses, which creates a community that has feedback. 

## Technology Stack  
Python  
Flask 
Coursera API 
Sqlite3  
SqlAlchemy  
HTML  
CSS  
Bootstrap
JavaScript
Jinja2 (Templating engine)


## Features
Landing page 
Visitors to the site are immediately greeted with a form that allows some complex querying to take place.

![Alt text](/static/images/Homepage.jpg?raw=true "Homepage") 

**Login**
Users can sign up and log in natively, but also have the option of logging in via Facebook.Facebook OAuth was integrated to achieve this. 

**Search results**
Courses are displayed below. Users can view the details of a particular course by clicking on Course Overview. They can also bookmark a course, if they are logged in. 

**Profile page**: Each user has a profile page on which they can see which courses they took, view a list of their friends, pending friend requests, and their bookmarked courses. 

**About me** Users can add details about themselves that they wish to share. They can also edit this information. 

**Bookmarking Courses**: Users can bookmark courses they are interested in. Users can also delete bookmarks. 
![Alt text](/static/images/Homepage.jpg?raw=true "Homepage") 

**Rating a course** Users can rate courses using the star rating system. Users can also update a rating for a particular course they have already taken. 

**Writing a review** Users can submit reviews for courses. 

**Friendships** Users can add one another as friends by sending friend requests. 

**Randomize** The app also returns a random course suggestion to users if they aren't sure of what kind of courses are available




