# Flask forms extension packages
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import *
from wtforms.validators import *
from models import *
from wtforms_sqlalchemy.fields import QuerySelectMultipleField


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
    

# class MealForm(FlaskForm):
#     name = StringField('Name', 
#                        validators=[InputRequired()], 
#                        render_kw={"placeholder": "Meal Name"})

#     price = FloatField('Price', 
#                        validators=[InputRequired()], 
#                        render_kw={"placeholder": "Price"})

#     number_sold = IntegerField('Number Sold', 
#                                validators=[InputRequired()], 
#                                render_kw={"placeholder": "Number Sold"})

#     categories = QuerySelectMultipleField(
#         'Categories', 
#         query_factory=lambda: Meal_Category.query.all(), 
#         get_label='category', 
#         allow_blank=True,
#         render_kw={"placeholder": "Select Categories"}
#     )
    
#     restrictions = QuerySelectMultipleField(
#         'Dietary Restrictions', 
#         query_factory=lambda: Dietary_Restriction.query.all(), 
#         get_label='restriction', 
#         allow_blank=True,
#         render_kw={"placeholder": "Select Dietary Restrictions"}
#     )
    
#     menus = QuerySelectMultipleField(
#         'Menus', 
#         query_factory=lambda: Menu.query.all(), 
#         get_label='name', 
#         allow_blank=True,
#         render_kw={"placeholder": "Select Menus"}
#     )
    
#     infos = QuerySelectMultipleField(
#         'Nutritional Information', 
#         query_factory=lambda: Nutritional_Information.query.all(), 
#         get_label='info', 
#         allow_blank=True,
#         render_kw={"placeholder": "Select Nutritional Information"}
#     )
    
#     submit = SubmitField('Submit Meal')


# class DietaryRestrictionForm(FlaskForm):
#     restriction = StringField('Restriction', validators=[DataRequired(), Length(min=1, max=255)], render_kw={"placeholder": "Dietary Restriction"})
#     submit = SubmitField('Add Dietary Restriction')

# class NutritionalInformationForm(FlaskForm):
#     info = StringField('Nutritional Information', validators=[DataRequired(), Length(min=1, max=255)], render_kw={"placeholder": "Nutritional Information"})
#     submit = SubmitField('Add Nutritional Information')

# class MealCategoryForm(FlaskForm):
#     # Category is the label that will be displayed next to the input field on the form.
#     # DataRequired() ensures that, it doesn;t leave info empty
#     # adds additional html attribute. Meal Category" will appear as a faded text inside the field, 
#     category = StringField('Category', validators=[DataRequired(), Length(min=1, max=64)], render_kw={"placeholder": " Meal Category"})
#     submit = SubmitField('Add Category')
    

