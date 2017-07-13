from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email, Length, EqualTo


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Please enter a valid username."),
                                                   Length(min=3, message="Username must be 3 characters or more")])
    email = StringField('Email', validators=[DataRequired("Please enter your email."),
                                             Email("Please enter a valid email")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password."),
                                                     Length(min=3, message="Passwords must be 3 characters or more"),
                                                     EqualTo('verify_password', message="Passwords does not match")])
    verify_password = PasswordField('Verify Password', validators=[DataRequired("Please verify your password.")])
    submit = SubmitField('Signup')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Please enter a valid username ."),
                                                   Length(min=3, message="Username must be 3 characters or more")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
    submit = SubmitField('Sign In')


class BlogForm(FlaskForm):
    blog_title = StringField('Title for your new blog', validators=[DataRequired("Please enter a name for your blog")])
    blog_post = StringField('Your new blog:', widget=TextArea(), validators=[DataRequired("Oops! Looks like your blog is blank.")])
    submit = SubmitField('Add Entry')
