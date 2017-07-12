from flask import Flask, request, redirect, render_template, session, flash, url_for
from app import app, db
from models import Blog, User
from forms import SignupForm, LoginForm, BlogForm


app.secret_key = 'super_secret_key'

@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session and '/static/' not in request.path:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if request.method == "POST":
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user is None:
                flash("User does not exist. Please register for an account.")
                return redirect(url_for('login'))
            if not user.check_password(password):
                flash("User password incorrect. Please try again.")
                return redirect(url_for('login'))
            else:
                session['username'] = form.username.data
                flash("Logged In")
                return redirect(url_for('new_post'))

    return render_template('login.html', form=form)


@app.route('/signup', methods=['POST', 'GET'])
def register():
    form = SignupForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('signup.html', form=form)
        else:

            username = form.username.data
            email = form.email.data
            password = form.password.data

            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, email, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = new_user.username
                return redirect(url_for('new_post'))

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

            owner = User.query.filter_by(username=session['username']).first()
            blog_title = form.blog_title.data
            blog_post = form.blog_post.data

            new_blog = Blog(blog_title, blog_post, owner)
            db.session.add(new_blog)
            db.session.commit()

            return redirect(url_for('blog', id=new_blog.id))

    return render_template('newpost.html', form=form, title="Add a Blog Entry")


@app.route('/logout')
def logout():
    del session['username']
    flash("Thanks for visiting. You are now logged out.")
    return redirect('/login')


@app.route("/blog")
def blog():
    if not request.args:
        blogs = Blog.query.order_by(Blog.timestamp.desc()).all()
        return render_template("blog.html", blogs=blogs)
    elif request.args.get('id'):
        id = request.args.get('id')
        blog = Blog.query.filter_by(id=id).first()
        return render_template('blogpost.html', blog=blog)
    elif request.args.get('user'):
        id = request.args.get('user')
        user = User.query.filter_by(id=id).first()
        blogs = Blog.query.filter_by(owner_id=id).all()
        return render_template('user.html', blogs=blogs, user=user)


@app.route("/")
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


if __name__ == '__main__':
    app.run()
