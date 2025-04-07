from flask import *
from form_classes import *
from flask_login import *
from models import *

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

@views.route('/feedback-page', methods=['GET', 'POST'])
def feedback():
    return render_template('feedback-page.html')


@views.route('/feedback-page', methods=['POST'])
def submit_rating():
    rating = request.form.get('rating')
    print(f'User submitted rating: {rating}')
    # You can store this rating in your database here
    return redirect(url_for('views.feedback'))  # Or show a "Thank you" page

@views.route('/post-meal', methods=['GET', 'POST'])
def post_meal():
    return render_template('post-meal.html')


@views.route('/meal-feedback-list', methods=['GET', 'POST'])
def meal_feedback_list():
    # Sample data - a list of comments
    students = ['Student1', 'Student2', 'Student3', 'Student4']
    
    comments = {
        'student1': 'It was great food',
        'student2': 'The egg scramble was pretty dried.',
        'student3': 'It looks different from what I expected.',
        'student4': 'Its okay.',
        'student5': 'It was great food'
    }
    
    another_comments = {
        'student6': 'Great food.',
        'student7': 'I liked how the eggs tasted!',
        'student8': 'Its alright.'
    }
    avg_rating = 3.5
    return render_template('meal-feedback-list.html', comments = comments, avg_rating = avg_rating, another_comments = another_comments)