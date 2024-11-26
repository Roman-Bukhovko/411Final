from flask import Blueprint, request, jsonify
from data.models import User, db

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    """
    Logs in a user by checking the name and password against the database.

    Args:
        None.

    Returns:
        JSON: A message indicating whether the login was successful or not.
    """
    name = request.form.get('name')
    password = request.form.get('password')
    
    # check if fields are missing
    if not name or not password:
        return jsonify({'status': 'Missing name or password'})
    
    # check if user exists and password is correct
    user = User.query.filter_by(name=name).first()
    
    if user and user.check_password(password):
        return jsonify({'status': 'Login successful'})
    else:
        return jsonify({'status': 'Invalid credentials'})

@login_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new user by creating a new entry in the database.

    Args:
        None.
    
    Returns:
        JSON: A message indicating whether the user was created successfully or not
    """
    name = request.form.get('name')
    password = request.form.get('password')
    
    # check if fields are missing
    if not name or not password:
        return jsonify({'status': 'Missing name or password'})
    
    # check if user already exists
    user = User.query.filter_by(name=name).first()
    if user:
        return jsonify({'status': 'User already exists'})
    
    # Create new user and set the password
    user = User(name=name)
    user.set_password(password)
    
    # Save the user to the database
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'status': 'User created'})

@login_bp.route('/change-password', methods=['POST'])
def change_password():
    """
    Changes the password of an existing user.

    Args:
        None.

    Returns:
        JSON: A message indicating whether the password was changed successfully or not
    """
    name = request.form.get('name')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    
    # check if fields are missing
    if not name or not old_password or not new_password:
        return jsonify({'status': 'Missing required fields'})
    
    user = User.query.filter_by(name=name).first()
    
    if user and user.check_password(old_password):
        user.set_password(new_password)
        
        # Save the updated password to the database
        db.session.commit()
        
        return jsonify({'status': 'Password changed'})
    else:
        return jsonify({'status': 'Invalid credentials'})
