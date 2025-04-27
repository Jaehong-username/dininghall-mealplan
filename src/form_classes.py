# Flask forms extension packages
from flask_wtf import FlaskForm, CSRFProtect
from wtforms_alchemy import QuerySelectMultipleField
from wtforms import *
from wtforms.validators import *
from models import *

# https://flask-wtf.readthedocs.io/en/0.15.x/form/
from flask_wtf.file import FileField, FileRequired

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


class MealPlanForm(FlaskForm):
    plan_id = SelectField(
        choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3')],
        validators=[DataRequired()],
        render_kw={"class": "meal-form-class"}
    )

    submit = SubmitField('Confirm Plan', render_kw={"class": "meal-plan-btn"})

# so flask can use the hidden_tag
class OTPForm(FlaskForm):
    otp = StringField('OTP', validators=[DataRequired()])
    submit = SubmitField('Verify')
    
    


class MealForm(FlaskForm):
    name = StringField('Name', 
                       validators=[InputRequired()], 
                       render_kw={"placeholder": "Meal Name"})

    price = FloatField('Price', 
                       validators=[InputRequired()], 
                       render_kw={"placeholder": "Price"})

    number_sold = IntegerField('Number Sold', 
                               validators=[InputRequired()], 
                               render_kw={"placeholder": "Number Sold"})

    categories = QuerySelectMultipleField(
        'Categories', 
        query_factory=lambda: Meal_Category.query.all(), 
        get_label='category', 
        allow_blank=True,
        render_kw={"placeholder": "Select Categories"}
    )
    
    restrictions = QuerySelectMultipleField(
        'Dietary Restrictions', 
        query_factory=lambda: Dietary_Restriction.query.all(), 
        get_label='restriction', 
        allow_blank=True,
        render_kw={"placeholder": "Select Dietary Restrictions"}
    )
    
    menus = QuerySelectMultipleField(
        'Menus', 
        query_factory=lambda: Menu.query.all(), 
        get_label='name', 
        allow_blank=True,
        render_kw={"placeholder": "Select Menus"}
    )
    
    infos = QuerySelectMultipleField(
        'Nutritional Information', 
        query_factory=lambda: Nutritional_Information.query.all(), 
        get_label='info', 
        allow_blank=True,
        render_kw={"placeholder": "Select Nutritional Information"}
    )
    
    submit = SubmitField('Submit Meal')


class DietaryRestrictionForm(FlaskForm):
    restriction = StringField('Restriction', validators=[DataRequired(), Length(min=1, max=255)], render_kw={"placeholder": "Dietary Restriction"})
    submit = SubmitField('Add Dietary Restriction')

class NutritionalInformationForm(FlaskForm):
    info = StringField('Nutritional Information', validators=[DataRequired(), Length(min=1, max=255)], render_kw={"placeholder": "Nutritional Information"})
    submit = SubmitField('Add Nutritional Information')

class MealCategoryForm(FlaskForm):
    # Category is the label that will be displayed next to the input field on the form.
    # DataRequired() ensures that, it doesn;t leave info empty
    # adds additional html attribute. Meal Category" will appear as a faded text inside the field, 
    category = StringField('Category', validators=[DataRequired(), Length(min=1, max=64)], render_kw={"placeholder": " Meal Category"})
    submit = SubmitField('Add Category')

class ImageForm(FlaskForm):
    file = FileField(validators=[FileRequired()])
    meal_id = IntegerField('Enter Corresponding Meal ID')
    submit = SubmitField('Upload Image')

# class RegisterForm(FlaskForm):
#     email = EmailField(validators=[
#                            DataRequired(), Email(), Length(min=4, max=255)], render_kw={"placeholder": "Email Address"})

#     name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})

#     password = PasswordField(validators=[
#                              DataRequired(), Length(min=8, max=255)], render_kw={"placeholder": "Password"})

#     submit = SubmitField('Register')

#     def validate_username(self, email):
#         existing_user_email = User.query.filter_by(
#             email=email.data).first()
#         if existing_user_email is not None:
#             print("ERROR: EMAIL VALIDATION ERROR")
#             raise ValidationError(
#                 'That email address already exists. Please choose a different one.')


# class LoginForm(FlaskForm):
#     email = EmailField(validators=[
#                            InputRequired(), Length(min=4, max=255)], render_kw={"placeholder": "Email Address"})

#     password = PasswordField(validators=[
#                              InputRequired(), Length(min=0, max=255)], render_kw={"placeholder": "Password"})

#     submit = SubmitField('Login')
