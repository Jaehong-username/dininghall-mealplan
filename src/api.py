from flask import *
from flask_login import *
from json import *
from models import *
from dateutil import parser


api_bp = Blueprint('api_bp', __name__)

def get_table_by_name(name):
    if not isinstance(name, str):
        print(f"Invalid table name: {name}")  # Debug: Log invalid table names
        return None
    tables_dict = {}
    for table in db.Model.__subclasses__():
        tables_dict[table.__tablename__] = table
    # look for table and return data.
    if table is None:
        print(f"Table not found: {name}")
    return tables_dict[name]
    
def to_int_or_none(value):
    return int(value) if value else None

@api_bp.route('/api/get_admin_data', methods=['GET', 'POST'])
@login_required
def get_admin_data():
    table_id = request.form.get("table_id")
    if(current_user.is_admin() and table_id is not None):
        table = get_table_by_name(table_id)
        if table is not None:
            results = table.query.all()
            return jsonify([table_item.to_dict() for table_item in results])
        else:
            print("Could not find table " + table_id + "!")
    else:
        if(current_user.is_admin() == False):
            return jsonify({'error': 'Unauthorized request'}), 403
        elif table_id is None:
            return jsonify({'error': 'table_id not supplied'}), 404
        else:
            return jsonify({'error': 'Error retrieving data'}), 404
    return jsonify({'error': 'Unauthorized request'}), 403
    

@api_bp.route("/api/delete_object", methods=["GET", "POST"])
@login_required
def delete_object():
    table_id = request.form.get("table_id")
    key = request.form.get("id")
    if(current_user.is_admin() and table_id is not None and key is not None):

        # look for table and return data.
        table = get_table_by_name(table_id)
        if table is not None:
            # look for object by primary key
            object_to_delete = table.query.get(int(key))
            if(object_to_delete is not None):
                db.session.delete(object_to_delete)
                db.session.commit()
                return jsonify({'success': table_id + ' object deleted.'}), 200
            else:
                print("Could not find " + table_id + " to delete!")
        else:
            print("Could not find table " + table_id + "!")
    pass

@api_bp.route("/api/delete_user", methods=["GET", "POST"])
@login_required
def delete_user():
    # Get user id
    key = request.form.get("id")
    if(current_user.is_admin() and key is not None):
        user = User.query.get(int(key))
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        else:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'success': 'User deleted.'}), 200
    else:
        return jsonify({'error': 'Unauthorized request'}), 403
    pass

@api_bp.route("/api/add_user", methods=["GET", "POST"])
def add_user():
    # Get user id
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    
    if(current_user.is_admin() and email is not None and name is not None and password is not None):
        user = User(email=email, name=name, password=password)
        if user is None:
            return jsonify({'error': 'User could not be created'}), 404
        else:
            db.session.add(user)
            db.session.commit()
            return jsonify({'success': 'User created.'}), 200
    else:
        return jsonify({'error': 'Unauthorized request'}), 403
    pass

@api_bp.route("/api/add_student", methods=["GET", "POST"])
def add_student():
    # Get user id
    user_id = request.form.get("user_id")
    balance = request.form.get("balance")
    admin_id = request.form.get("admin_id")
    plan_id = request.form.get("plan_id")
    
    if(current_user.is_admin() and user_id is not None and balance is not None and admin_id is not None and plan_id is not None):
        student = Student(user_id=int(user_id),
                          balance=float(balance), 
                          admin_id=int(admin_id),
                          plan_id=int(plan_id) if plan_id is not '' else None)
        if student is None:
            return jsonify({'error': 'Student could not be created'}), 404
        else:
            db.session.add(student)
            db.session.commit()
            return jsonify({'success': 'Student created.'}), 200
    else:
        return jsonify({'error': 'Unauthorized request'}), 403
    pass

@api_bp.route("/api/add_manager", methods=["GET", "POST"])
def add_manager():
    # Get user id
    user_id = request.form.get("user_id")
    
    if(current_user.is_admin() and user_id is not None):
        manager = Manager(manager_id = int(user_id))
        if manager is None:
            return jsonify({'error': 'Manager could not be created'}), 404
        else:
            db.session.add(manager)
            db.session.commit()
            return jsonify({'success': 'Manager created.'}), 200
    else:
        return jsonify({'error': 'Unauthorized request'}), 403
    pass

@api_bp.route("/api/add_admin", methods=["GET", "POST"])
def add_admin():
    # Get user id
    user_id = request.form.get("user_id")
    manager_id = request.form.get("manager_id")
    if(current_user.is_admin() and user_id is not None):
        admin = Admin(admin_id = int(user_id), manager_id = to_int_or_none(manager_id))
        if admin is None:
            return jsonify({'error': 'Admin could not be created'}), 404
        else:
            db.session.add(admin)
            db.session.commit()
            return jsonify({'success': 'Admin created.'}), 200
    else:
        return jsonify({'error': 'Unauthorized request'}), 403
    pass

@api_bp.route("/api/add_employee", methods=["GET", "POST"])
def add_employee():
    # Get user id
    user_id = request.form.get("user_id")
    menu_id = request.form.get("menu_id")
    if(current_user.is_admin() and user_id is not None):
        employee = Employee(employee_id = int(user_id), menu_id = to_int_or_none(menu_id))
        if employee is None:
            return jsonify({'error': 'Employee could not be created'}), 404
        else:
            db.session.add(employee)
            db.session.commit()
            return jsonify({'success': 'Employee created.'}), 200
    else:
        return jsonify({'error': 'Unauthorized request'}), 403
    pass

@api_bp.route("/api/add_menu", methods=["GET", "POST"])
def add_menu():
    # Get user id
    date = request.form.get("date")
    location = request.form.get("location")
    if(current_user.is_admin() and date != None and location != None):
        menu = Menu(date=parser.parse(date), location=location)
        if menu is None:
            return jsonify({'error': 'Menu could not be created'}), 404
        else:
            db.session.add(menu)
            db.session.commit()
            return jsonify({'success': 'Menu created.'}), 200
    else:
        return jsonify({'error': 'Unauthorized request'}), 403
    
@api_bp.route("/api/add_mealplan", methods=["GET", "POST"])
def add_mealplan():
    # Get user id
    price = request.form.get("price")
    if(current_user.is_admin() and price != None):
        mealplan = Meal_Plan(price = price)
        if mealplan is None:
            return jsonify({'error': 'Meal Plan could not be created'}), 404
        else:
            db.session.add(mealplan)
            db.session.commit()
            return jsonify({'success': 'Meal Plan created.'}), 200
    else:
        return jsonify({'error': 'Unauthorized request'}), 403

@api_bp.route("/api/edit_user", methods=["GET", "POST"])
def edit_user():
    # Get user id
    user_id = request.form.get("user_id")
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    
    if(current_user.is_admin() and user_id is not None):
        user = User.query.get(int(user_id))
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        else:
            if email is not None and email is not '':
                user.email = email
            if name is not None and name is not '':
                user.name = name
            if password is not None and password is not '':
                user.set_password(password)
            
            db.session.commit()
            return jsonify({'success': 'User updated.'}), 200
    else:
        return jsonify({'error': 'Unauthorized request'}), 403
# TODO: Implement API endpoint for and editing database items via the inline forms on the dashboard.