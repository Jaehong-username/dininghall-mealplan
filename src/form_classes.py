from flask_wtf import FlaskForm, CSRFProtect
from wtforms import *
from wtforms.validators import *
class RegisterForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired(message="Name is required!"), Length(1,255)])
    email = EmailField("Email address:", validators=[DataRequired("Email address is required!"), Email(message="Invalid Email address!"), Length(1,255)])
    password = PasswordField("Password:", validators=[DataRequired(message="Password is required!"), Length(1, 255)])
    submit = SubmitField('Log in')
    
class LoginForm(FlaskForm):
    email = EmailField("Email address:", validators=[DataRequired("No email provided!"), Email(message="Invalid Email address!"), Length(1,255)])
    password = PasswordField("Password:", validators=[DataRequired(message="Invalid password!"), Length(1, 255)])
    submit = SubmitField('Log in')