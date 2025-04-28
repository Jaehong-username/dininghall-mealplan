from flask import *
from form_classes import *
from flask_login import *
from models import *
from datetime import *
from wtforms_alchemy import QuerySelectMultipleField

# for 2FA
import pyotp  
import qrcode
import io
from base64 import b64encode

# import related to uploading images
import os
from werkzeug.utils import secure_filename

# variables related to image uploads
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}

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
            if user.twofa_secret is None:
                login_user(user)
                return redirect(url_for('views.dashboard'))
            else:
                session['pre_2fa_user_id'] = user.user_id
                return redirect(url_for('views.two_factor'))
      else:
          message = "ERROR: Incorrect username or password!"
    return render_template('login.html', form=form, message=message)


@views.route('/2fa', methods=['GET', 'POST'])
def two_factor():

    #create an instance of the otp form
    form = OTPForm()

    if form.validate_on_submit():
        otp = form.otp.data
        user_id = session.get('pre_2fa_user_id')

        if not user_id:
            flash("Session expired, please login again.", "danger")
            return redirect(url_for('views.login'))

        user = User.query.get(user_id)

        if not user or not hasattr(user, 'twofa_secret') or user.twofa_secret is None:
            flash("User 2FA setup incomplete. Please register again.", "danger")
            return redirect(url_for('views.login'))

        totp = pyotp.TOTP(user.twofa_secret)

        if totp.verify(otp):

            # actually log them in now
            login_user(user)  

            # remove temp session
            session.pop('pre_2fa_user_id', None)  
            flash("Successfully logged in!", "success") 
            return redirect(url_for('views.dashboard'))
        else:
            flash("Invalid OTP code. Try again.", "danger")
            return redirect(url_for('views.two_factor'))

    return render_template('verify-otp.html', form=form)

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

        # check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            message = "An account with that email already exists. Please log in."
            return render_template('register.html', form=form, message=message)

        # if not continue: 
        # generate a 2FA secret key
        secret = pyotp.random_base32()

        new_user = User(form.email.data, form.name.data, form.password.data)

        # save the secret to the db
        new_user.twofa_secret = secret  

        db.session.add(new_user)
        
        db.session.commit()

        # finding admin for initializer of user
        admin = Admin.query.first()
        
        ### Create a student account for the user too.
        new_student = Student(new_user.user_id, admin.admin_id, None, 500.00)        
        db.session.add(new_student)
        db.session.commit()
  
        #if User.test_login(form.email.data, form.password.data) is None:
        #    message = "ERROR: Could not create account!"
        #else:
        #    return redirect(url_for('views.login'))
        

        # generate QR code for google authenticator
        uri = pyotp.TOTP(secret).provisioning_uri(name=form.email.data, issuer_name="DiningHallManager")
        qr = qrcode.make(uri)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        img_str = b64encode(buf.getvalue()).decode('ascii')

        # show QR code after registration
        return render_template('2fa.html', qr_code=img_str)  
    
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
        flash("Menu does not exist")
        return redirect(request.url)  
    
    # getting menu type (breakfast, lunch, or dinner) to know what to display
    type = request.args.get('type')

    # getting menu location to know what to display
    location = request.args.get('location')
    
    return render_template('menu-details.html', menu=menu, type=type, location=location)


@views.route('/menu-options', methods=['GET', 'POST'])
def view_menu_options():
    # find menu in database according to today's date
    # menu = Menu.query.filter_by(date=date.today()).first()

    # for now, using a temp date for testing
    menu = Menu.query.filter_by(date=date(2025, 4, 2)).first()
    
    # display error & return to home if menu not found
    if not menu:
        flash("Menu does not exist")
        return redirect(request.url)   
    
    return render_template('menu-options.html', menu=menu)


# choose meal plan (with id)
@views.route('/meal-plan', methods=['GET', 'POST'])
@login_required
def meal_plan_id():
    # form for updating meal plan
    form = MealPlanForm()
    
    # updating meal plan choices
    form.plan_id.choices = [(plan.id, f'Level {plan.id}') for plan in Meal_Plan.query.all()]

    # find student in database
    student = Student.get_student_by_id(current_user.user_id)
    
    # display error & return to home if student not found
    if not student:
        flash("Student does not exist")
        return redirect(request.url)   
    
    # updating meal plan
    if form.validate_on_submit():
        print("Now changing meal plan")
        updated_plan = Meal_Plan.query.get(form.plan_id.data)
        student.plan_id = updated_plan.id
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


@views.route('/admin-portal', methods=['GET', 'POST'])
@login_required
def admin_portal_main():
    admin = Admin.get_admin_by_id(current_user.user_id)
    if(admin is None):
        abort(401)
    else:
       return render_template('admin-portal-main.html')

@views.route('/admin-portal/users', methods=['GET', 'POST'])
@login_required
def admin_portal_users():
    admin = Admin.get_admin_by_id(current_user.user_id)
    if(admin is None):
        abort(401)
    else:
        user_forms = {}

        user_forms["new_user_form"] = NewUserForm()
        user_forms["edit_user_form"] = EditUserForm()
        user_forms["new_admin_form"] = newAdminForm()
        user_forms["new_manager_form"] = newManagerForm()
        user_forms["new_student_form"] = newStudentForm()
        user_forms["new_employee_form"] = newEmployeeForm()

        return render_template('admin-portal-users.html', user_forms = user_forms)

@views.route('/admin-portal/menus', methods=['GET', 'POST'])
@login_required
def admin_portal_menus():
    admin = Admin.get_admin_by_id(current_user.user_id)
    if(admin is None):
        abort(401)
    else:
        
        
        return render_template('admin-portal-menus.html', new_menu_form = newMenuForm())

@views.route('/admin-portal/mealplans', methods=['GET', 'POST'])
@login_required
def admin_portal_mealplans():
    admin = Admin.get_admin_by_id(current_user.user_id)
    if(admin is None):
        abort(401)
    else:
        return render_template('admin-portal-mealplans.html', new_mealplan_form = newMealPlanForm())

@views.route('/feedback-page', methods=['GET', 'POST'])
def feedback():
    return render_template('feedback-page.html')


@views.route('/feedback-page', methods=['POST'])
def submit_rating():
    rating = request.form.get('rating')
    print(f'User submitted rating: {rating}')
    # You can store this rating in your database here
    return redirect(url_for('views.feedback'))  # Or show a "Thank you" page

# to access the meal's official image for a menu, it will follow the format: static/uploads/meal/<meal_id>
@views.route('/post-meal', methods=['GET', 'POST'])
def post_meal():
    meals = Meal.query.all()
    form = ImageForm()
    
    # checking if form went through
    if form.validate_on_submit():
        file = form.file.data
        
        if file:
            filename = secure_filename(file.filename)

            # error checking name (if empty) or if correct extension type
            if filename == '' or not allowed_file(file.filename):
                flash('Incompatible file. Please try again.')
                return redirect(request.url)
            
            # otherwise continue with data

            # first, rename according to meal option
            root, ext = os.path.splitext(filename)
            meal_id = str(form.meal_id.data)
            new_filename = meal_id + ext

            # create new file path
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_path)

            # details of meal
            selected_meal = Meal.query.get(meal_id)

            # updating extension
            selected_meal.file_extension = ext
            db.session.commit()
            
            return render_template('post-meal.html', filename=filename, form=form, meals=meals, selected_meal=selected_meal)

    return render_template('post-meal.html', form=form, meals=meals)


@views.route('/meal-feedback-list', methods=['GET', 'POST'])
def meal_feedback_list():
    # Sample data - a list of comments
    students = ['Student1', 'Student2', 'Student3', 'Student4']
    
    comments = {
        'Student 1': 'It was great food',
        'Student 2': 'The egg scramble was pretty dry.',
        'Student 3': 'It looks different from what I expected.',
        'Student 4': 'Its okay.',
        
    }
    
    another_comments = {
        'Student 5': 'It was yummy food.',
        'Student 6': 'Good food.',
        'Student 7': 'I liked how the eggs tasted!',
        'Student 8': 'Its alright.'
    }
    avg_rating = 3.5
    return render_template('meal-feedback-list.html', comments = comments, avg_rating = avg_rating, another_comments = another_comments)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# upload file images
@views.route('/feedback-page', methods=['GET', 'POST'])
def upload_file():
    form = ImageForm()
    
    # checking if form went through
    if form.validate_on_submit():
        file = form.file.data
        
        if file:
            filename = secure_filename(file.filename)

            # error checking name (if empty) or if correct extension type
            if filename == '' or not allowed_file(file.filename):
                flash('Incompatible file. Please try again.')
                return redirect(request.url)
            
            # otherwise continue with data
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return render_template('feedback-page.html', filename=filename, form=form)

    return render_template('feedback-page.html', form=form)

# image handling
@views.route('/uploads/meals/<name>')
def image_file(name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)

@views.route('/meal-data',  methods=['GET'])
def meal_data():
    #gives you the first one using first()
    most_sold_meal = Meal.query.order_by(Meal.number_sold.desc()).first()
    least_sold_meal = Meal.query.order_by(Meal.number_sold.asc()).first()
    
    most_total_revenue = most_sold_meal.price * most_sold_meal.number_sold
    least_total_revenue = least_sold_meal.price * least_sold_meal.number_sold
    
    return render_template('meal-data.html', most_sold_meal = most_sold_meal, least_sold_meal = least_sold_meal, most = most_total_revenue, least = least_total_revenue)