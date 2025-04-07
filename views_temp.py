from flask import *
from form_classes import *
from flask_login import *
from models import *
from wtforms_sqlalchemy.fields import QuerySelectMultipleField


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')


@views.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    message = ""
    if form.validate_on_submit():
        user = User.test_login(form.email.data, form.password.data)
        # User was found with matching credentials
        if user is not None:
            login_user(user)
            return redirect(url_for('views.dashboard'))
        else:
            message = "ERROR: Incorrect username or password!"
    return render_template('login.html', form=form, message=message)


@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    ## check if user is a student
    student = Student.get_student_by_id(current_user.user_id)
    
    return render_template('dashboard.html', student = student)


@views.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))

#Accessing /register triggers this function.
@views.route('/register', methods=['GET', 'POST']) # specifies which HTTP methods the route should accept.
def register():
    form = RegisterForm()
    message = ""
    
    if form.validate_on_submit():
        print("Form submitted!")
        new_user = User(form.email.data, form.name.data, form.password.data)
        db.session.add(new_user)
        
        db.session.commit()
        
        ### Create a student account for the user too.
        new_student = Student(new_user.user_id, "500")
        db.session.add(new_student)
        db.session.commit()
        
        if User.test_login(form.email.data, form.password.data) is None:
            message = "ERROR: Could not create account!"
        else:
            return redirect(url_for('views.login'))
    
    return render_template('register.html', form=form,  message=message)

@views.route('/dining-halls', methods=['GET', 'POST'])
def view_dining_halls():
    return render_template('dining-halls.html')

@views.route('/menu-details', methods=['GET', 'POST'])
def view_today_menus():
    return render_template('menu-details.html')

@views.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@views.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('forgot-password.html')

@views.route('/email-confirmation', methods=['GET', 'POST'])
def confirm_email():
    return render_template('confirm-email.html')

@views.route('/change-password', methods=['GET', 'POST'])
def change_password():
    return render_template('change-password.html')



# Assume that Manager is a subclass of User and can be retrieved using the current_user
@models_bp.route('/post-food-information', methods=['POST']) #when a post request is made to post-dietary-restrictions
@login_required
def post_food_information():
    # Only allow Managers to post dietary restrictions
    if not isinstance(current_user, Manager):
        return jsonify({'message': 'You must be a manager to perform this action'}), 403
    
    #messages
    success_message = None
    error_message = None

    #instantiate the form!
    form = DietaryRestrictionForm()
    
    # if form validation was successful!
    if form.validate_on_submit():
        # Check if the dietary restriction already exists, saving some memory
        existing_dietary_restriction = DietaryRestrictionForm.query.filter_by(restriction=form.restriction.data).first()
        if existing_dietary_restriction:
            error_message = 'This dietary restriction already exists.'
            return render_template('post-diet-restrict.html', form = form, error_message=error_message)
            #return jsonify({'message': 'This dietary restriction already exists.'}), 400
        
        # Create a new dietary restriction and add it to the database
        new_dietary_restriction = DietaryRestrictionForm(restriction=form.restriction.data)
        db.session.add(new_dietary_restriction)
        db.session.commit()
        
        success_message = 'Dietary restriction added successfully!'
        #return jsonify({'message': 'Dietary restriction added successfully!'}), 201

    # If it's a GET request or form is not valid, render the form again
    #return render_template('add_dietary_restriction.html', form=form)
    return render_template('post-diet-restrict.html', form=form, success_message = success_message)
    

def post_nutritional_information():
    # Only allow Managers to post dietary restrictions
    if not isinstance(current_user, Manager):
        return jsonify({'message': 'You must be a manager to perform this action'}), 403
    
    #messages
    success_message = None
    error_message = None

    #instantiate the form!
    form = NutritionalInformationForm()
    
    # if form validation was successful!
    if form.validate_on_submit():
        # Check if the dietary restriction already exists, saving some memory
        existing_nutritional_info = NutritionalInformationForm.query.filter_by(restriction=form.info.data).first()
        if existing_nutritional_info:
            error_message = 'This nutritional information already exists.'
            return render_template('post-nutri-info.html', form = form, error_message=error_message)
            #return jsonify({'message': 'This dietary restriction already exists.'}), 400
        
        # Create a new dietary restriction and add it to the database
        existing_nutritional_info = NutritionalInformationForm(restriction=form.info.data)
        db.session.add(existing_nutritional_info)
        db.session.commit()
        
        success_message = 'Nutritional Information added successfully!'
        #return jsonify({'message': 'Dietary restriction added successfully!'}), 201

    # If it's a GET request or form is not valid, render the form again
    #return render_template('add_dietary_restriction.html', form=form)
    return render_template('post-nutri-info.html', form=form, success_message = success_message)




@views.route('/post-meal', methods=['GET', 'POST'])
def add_meal():
    form = MealForm()
    
    err = ""
    res = ""
    
    if form.validate_on_submit():
        # Create a new meal instance
        meal = Meal(
            name=form.name.data,
            price=form.price.data,
            number_sold=form.number_sold.data
        )

        # Handle the many-to-many relationships (categories, restrictions, menus, and nutritional information)
        meal.categories = form.categories.data
        meal.restrictions = form.restrictions.data
        meal.menus = form.menus.data
        meal.infos = form.infos.data

        # Add the meal to the database
        db.session.add(meal)
        db.session.commit()

        
        #flash('Meal successfully added!', 'success')
        res = 'Meal successfully added!', 'success'
        return render_template('add_meal.html', form=form, res = res)  # Redirect to some page where meals are listed

    return render_template('add_meal.html', form=form, err = err)