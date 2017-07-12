# build-a-blog
## A simple Flask project for LaunchCode LC-101


_Implements_:

- [Flask](http://flask.pocoo.org/) template rendering
- web form using Flask-wtf
- form validation using wtforms
- HTTP routing & endpoints
- HTML
- CSS
- request
- redirect
- render_template (in place of jinja2)
- mySQL database
- SQLAlchemy
- werkzeug to generate password hash
- Cross-Site Request Forgery (CSRF) Protection

***

# SQLAlchemy setup

open python3 in terminal
>>> from main import db,Task
>>> db
>>> db.create_all()  ### creates the DB using the specified columns
>>> new_task = Task('finish Lesson 2')
>>> db.session.add(new_task)
>>> new_task_2 = Task('finish Lesson 3')
>>> db.session.add(new_task_2)
>>> db.session.commit() ### adds the new_task variable to database
>>> tasks = task.query.all() ### selects everything from the database
>>> tasks[0].name = 'finish Lesson 2'
>>> db.session.delete(new_task_2)
>>> db.drop_all() ### drops all the tables
>>> db.create_all() ### creates the database with the new / added columns

open mysql in another terminal window
> use blog; ## uses the blog database
> show tables; ## shows the tables
> describe task; ## shows the table columns
> select * from task; ## shows the new data inserted into the table columns

***

## _Sources_

- _Project rubric_: [LC-101 Blog App Part 1](http://education.launchcode.org/web-fundamentals/assignments/build-a-blog/)
[LC-101 Blog App Part 2](http://education.launchcode.org/web-fundamentals/assignments/blogz/)

- [Live demo of the app](http://winniezzzz.herokuapp.com/)
***

(c) June 2017
