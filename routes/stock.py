from flask import Blueprint, request, jsonify
from data.models import User, db
stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/add_ticker', methods=['POST'])
def add_ticker():
    """
    Adds a ticker to the user's list of tickers.

    Args:
        JSON: {
            'username': str,
            'password': str,
            'ticker': str,
            'amount': int 
        }

    Returns:
        JSON: A message indicating whether the ticker was added successfully or not.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    ticker = request.json.get('ticker')
    amount = request.json.get('amount')
    
    # sanity check
    if not username or not password or not ticker or not amount:
        return jsonify({'status': 'Missing username, password, ticker, or amount'})
    try:
        amount = int(amount)
    except ValueError:
        return jsonify({'status': 'Invalid amount'})

    # check if user exists and password is correct
    user = db.session.get(User, username)
    
    if user and user.check_password(password):
        user.add_ticker(ticker, amount)
        db.session.commit()
        return jsonify({'status': 'Sucess'})
    else:
        return jsonify({'status': 'Invalid credentials'})
    
@stock_bp.route('/remove_ticker', methods=['POST'])
def remove_ticker():
    """
    Removes some amount of a ticker from the user's list of tickers.

    Args:
        JSON: {
            'username': str,
            'password': str,
            'ticker': str,
            'amount': int
        }

    Returns:
        JSON: A message indicating whether the ticker amount was removed successfully or not.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    ticker = request.json.get('ticker')
    amount = request.json.get('amount')
    
    # sanity check
    if not username or not password or not ticker or not amount:
        return jsonify({'status': 'Missing username, password, ticker, or amount'})
    try:
        amount = int(amount)
    except ValueError:
        return jsonify({'status': 'Invalid amount'})
    # check if user exists and password is correct
    user = db.session.get(User, username)
    
    if user and user.check_password(password):
        ticker_removed = user.remove_ticker(ticker, amount)
        if not ticker_removed:
            return jsonify({'status': 'Failed'})
        db.session.commit()
        return jsonify({'status': 'Ticker amount removed'})
    else:
        return jsonify({'status': 'Invalid credentials'})
    
@stock_bp.route('/get_tickers', methods=['POST'])
def get_tickers():
    """
    Returns the user's list of tickers.

    Args:
        JSON: {
            'username': str,
            'password': str
        }

    Returns:
        JSON: The user's list of tickers.
    """
    username, password = request.json.get('username'), request.json.get('password')
    
    # sanity check
    if not username or not password:
        return jsonify({'status': 'Missing username or password'})

    # check if user exists and password is correct
    user = db.session.get(User, username)
    
    if user and user.check_password(password):
        return jsonify({'status': 'Success', 'tickers': user.get_tickers()})
    else:
        return jsonify({'status': 'Invalid credentials'})