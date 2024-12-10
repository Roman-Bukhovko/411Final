from flask import Blueprint, request, jsonify, current_app
from data.models import User, db

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    """
    Logs in a user by checking the name and password against the database.

    Args:
        JSON: {
            'username': str,
            'password': str
        }

    Returns:
        JSON: A message indicating whether the login was successful or not.
    """
    username, password = request.json.get('username'), request.json.get('password')
    
    # sanity check
    if not username or not password:
        current_app.logger.error('Missing username or password')
        return jsonify({'status': 'Missing username or password'})

    # check if user exists and password is correct
    user = db.session.get(User, username)
    
    if user and user.check_password(password):
        current_app.logger.info(f'User {username} logged in')
        return jsonify({'status': 'Login successful'})
    else:
        current_app.logger.error('Invalid credentials')
        return jsonify({'status': 'Invalid credentials'})

@login_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new user by creating a new entry in the database.

    Args:
        JSON: {
            'username': str,
            'password': str
        }
    
    Returns:
        JSON: A message indicating whether the user was created successfully or not
    """
    username, password = request.json.get('username'), request.json.get('password')
    
    # sanity check
    if not username or not password:
        current_app.logger.error('Missing name or password')
        return jsonify({'status': 'Missing name or password'})
    
    # check if user already exists
    user = db.session.get(User, username)
    if user:
        current_app.logger.error('Username already exists')
        return jsonify({'status': 'Username already exists'})
    
    # Create new user and set the password
    user = User(username=username)
    user.set_password(password)
    
    # Save the user to the database
    db.session.add(user)
    db.session.commit()
    current_app.logger.info(f'User {username} created')
    return jsonify({'status': 'User created'})

@login_bp.route('/change-password', methods=['POST'])
def change_password():
    """
    Changes the password of an existing user.

    Args:
        JSON: {
            'username': str,
            'old_password': str,
            'new_password': str
        }

    Returns:
        JSON: A message indicating whether the password was changed successfully or not
    """
    username = request.json.get('username')
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')
    
    # sanity check
    if not username or not old_password or not new_password:
        current_app.logger.error('Missing required fields')
        return jsonify({'status': 'Missing required fields'})
    
    current_app.logger.info(f'User {username} requesting password change')

    user = db.session.get(User, username)
    
    if user and user.check_password(old_password):
        user.set_password(new_password)
        db.session.commit()
        current_app.logger.info(f'Password changed')
        return jsonify({'status': 'Password changed'})
    else:
        current_app.logger.info(f'Invalid credentials')
        return jsonify({'status': 'Invalid credentials'})
