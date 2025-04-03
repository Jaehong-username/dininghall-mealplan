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


class MealPlanForm(FlaskForm):
    plan_id = SelectField(
        choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3')],
        validators=[DataRequired()],
        render_kw={"class": "meal-form-class"}
    )

    submit = SubmitField('Confirm Plan', render_kw={"class": "meal-plan-btn"})
