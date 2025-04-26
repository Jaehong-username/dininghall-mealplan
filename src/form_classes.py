# Flask forms extension packages
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import *
from wtforms.validators import *
from models import *

class RegisterForm(FlaskForm):
    email = EmailField(validators=[
                           DataRequired(), Email(), Length(min=4, max=255)], render_kw={"placeholder": "Email Address"})

    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})

    password = PasswordField(validators=[
                             DataRequired(), Length(min=8, max=255)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, email):
        existing_user_email = User.query.filter_by(
            email=email.data).first()
        if existing_user_email is not None:
            print("ERROR: EMAIL VALIDATION ERROR")
            raise ValidationError(
                'That email address already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    email = EmailField(validators=[
                           InputRequired(), Length(min=4, max=255)], render_kw={"placeholder": "Email Address"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=0, max=255)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')
    
class NewUserForm(FlaskForm):
    email = EmailField(validators=[
                           DataRequired(), Email(), Length(min=4, max=255)], render_kw={"placeholder": "Email Address"})

    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})

    password = PasswordField(validators=[
                             DataRequired(), Length(min=8, max=255)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, email):
        existing_user_email = User.query.filter_by(
            email=email.data).first()
        if existing_user_email is not None:
            print("ERROR: EMAIL VALIDATION ERROR")
            raise ValidationError(
                'That email address already exists. Please choose a different one.')

class EditUserForm(FlaskForm):
    user_id = IntegerField(validators=[DataRequired()], render_kw={"placeholder": "User ID"})
    email = EmailField(validators=[Email(), Length(min=4, max=255)], render_kw={"placeholder": "Email Address"})

    name = StringField('Name', render_kw={"placeholder": "Name"})

    password = PasswordField(validators=[Length(min=8, max=255)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Update')

    def validate_username(self, email):
        existing_user_email = User.query.filter_by(
            email=email.data).first()
        if existing_user_email is not None:
            print("ERROR: EMAIL VALIDATION ERROR")
            raise ValidationError(
                'That email address already exists. Please choose a different one.')

class newAdminForm(FlaskForm):
    user_id = IntegerField(validators=[DataRequired()], render_kw={"placeholder": "Admin user ID"})
    manager_id = IntegerField(validators=[DataRequired()], render_kw={"placeholder": "Manager user ID"})
    
    submit = SubmitField('Add Admin')
    
class newManagerForm(FlaskForm):
    user_id = IntegerField(validators=[DataRequired()], render_kw={"placeholder": "Manager user ID"})
    
    submit = SubmitField('Add Manager')
    
class newStudentForm(FlaskForm):
    user_id = IntegerField(validators=[DataRequired()], render_kw={"placeholder": "Student User ID"})
    balance = FloatField(validators=[DataRequired()], render_kw={"placeholder": "Balance ($)"})
    admin_id = IntegerField(validators=[DataRequired()], render_kw={"placeholder": "Admin ID"})
    plan_id = IntegerField(render_kw={"placeholder": "Meal plan ID"})
    
    submit = SubmitField('Add Student')
    
class newEmployeeForm(FlaskForm):
    user_id = IntegerField(validators=[DataRequired()], render_kw={"placeholder": "Employee user ID"})
    menu_id = IntegerField(render_kw={"placeholder": "Menu ID"})
    
    submit = SubmitField('Add Employee')
    
class newMenuForm(FlaskForm):
    date = DateField(validators=[DataRequired()], render_kw={"placeholder": "Date"})
    location = StringField('Location', validators=[DataRequired()], render_kw={"placeholder": "Location"})
    
    submit = SubmitField('Add Menu')

class newMealPlanForm(FlaskForm):
    price = FloatField(validators=[DataRequired()], render_kw={"placeholder": "Price ($)"})
    submit = SubmitField('Add Meal Plan')