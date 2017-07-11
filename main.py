from flask import Flask, request, redirect, render_template, session, flash, url_for
from forms import SignupForm, LoginForm, BlogForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://diognhexsqognq:aa18612b2b57045a7b3f58942999b754dc4c2f55db9c6d47691a435505381124@ec2-184-73-199-72.compute-1.amazonaws.com:5432/devo8ico0tbo2l'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'super_secret_key'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    post = db.Column(db.String(500))
    date = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, post, owner, date=None):
        self.name = name
        self.post = post
        self.owner = owner
        if date is None:
            date = datetime.utcnow()
        self.date = date



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session and '/static/' not in request.path:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if request.method == "POST":
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                flash("Logged In")
                return redirect(url_for('blog'))
            else:
                flash("User password incorrect, or user does not exist")

    return render_template('login.html', form=form)


@app.route('/signup', methods=['POST', 'GET'])
def register():
    form = SignupForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('signup.html', form=form)
        else:

            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data

            existing_user = User.query.filter_by(email=email).first()
            if not existing_user:
                new_user = User(first_name, last_name, email, password)
                db.session.add(new_user)
                db.session.commit()
                session['email'] = new_user.email
                return redirect(url_for('blog'))

            else:
                flash("This user already exist, please login instead")
                return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    form = BlogForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('newpost.html', form=form)
        else:

            owner = User.query.filter_by(email=session['email']).first()
            blog_title = form.blog_title.data
            blog_post = form.blog_post.data

            new_blog = Blog(blog_title, blog_post, owner)
            db.session.add(new_blog)
            db.session.commit()

            return redirect(url_for('blog', id=new_blog.id))

    return render_template('newpost.html', form=form, title="Add a Blog Entry")


@app.route('/logout')
def logout():
    del session['email']
    flash("Thanks for visiting. You are now logged out.")
    return redirect('/login')


@app.route("/blog")
def blog():
    if not request.args:
        owner = User.query.filter_by(email=session['email']).first()
        blogs = Blog.query.filter_by(owner=owner).order_by(Blog.id).all()
        return render_template("blog.html", blogs=blogs)
    else:
        id = request.args.get('id')
        blog = Blog.query.filter_by(id=id).first()
        return render_template('blogpost.html', blog=blog)


@app.route("/")
def index():
    owner = User.query.filter_by(email=session['email']).first()

    # you can add the date descending order_by here in place of filtering by blog id
    # both methods do the same thing, but it's nice to know how to timestamp your entries
    blogs = Blog.query.filter_by(owner=owner).order_by(Blog.id).all()
    return render_template('blog.html', blogs=blogs)


if __name__ == '__main__':
    app.run()
