from flask import *
from form_classes import *
from flask_login import *
from models import *
from datetime import *

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

    # find menu in database
    # TODO: change depending on the day to day basis
    menu = Menu.query.filter_by(date=date(2025, 4, 2)).first()
    
    # display error & return to home if student not found
    if not menu:
        print("Menu does not exist")
        return "<h3>Menu does not exist!</h3>" \
        "<form action='/'><button type='submit'>Return Home</button></form>"
    
    return render_template('menu-details.html', menu=menu)

@views.route('/menu-options', methods=['GET', 'POST'])
def view_menu_options():

    # find menu in database
    # TODO: change depending on the day to day basis
    menu = Menu.query.filter_by(date=date(2025, 4, 2)).first()
    
    # display error & return to home if student not found
    if not menu:
        print("Menu does not exist")
        return "<h3>Menu does not exist!</h3>" \
        "<form action='/'><button type='submit'>Return Home</button></form>"
    
    return render_template('menu-options.html', menu=menu)


# choose meal plan (with id)
@views.route('/meal-plan', methods=['GET', 'POST'])
def meal_plan_id():
    # form for updating meal plan
    form = MealPlanForm()

    # find student in database
    student = Student.get_student_by_id(current_user.user_id)
    
    # display error & return to home if student not found
    if not student:
        print("Student does not exist")
        return "<h3>Student does not exist!</h3>" \
        "<form action='/'><button type='submit'>Return Home</button></form>"
    
    # updating meal plan
    if form.validate_on_submit():
        print("Now changing meal plan")
        updated_plan = form.plan_id.data
        student.plan_id = updated_plan
        db.session.commit() # update in database

    return render_template("meal-plan.html", form=form, student=student)

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