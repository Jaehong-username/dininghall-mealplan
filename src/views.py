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
        return render_template('admin-portal-menus.html')

@views.route('/admin-portal/mealplans', methods=['GET', 'POST'])
@login_required
def admin_portal_mealplans():
    admin = Admin.get_admin_by_id(current_user.user_id)
    if(admin is None):
        abort(401)
    else:
        
        return render_template('admin-portal-mealplans.html')