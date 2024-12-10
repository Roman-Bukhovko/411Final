from flask import Blueprint, request, jsonify, current_app
from data.models import User, db

port_bp = Blueprint('portfolio', __name__)

@port_bp.route('/portfolio', methods=['POST'])
def portfolio():
    """
    Displays user's current stock portfolio and its total value.

    Args:
        None

    Returns:
        JSON: A message with the portfolio details and total value.
    """
    username = request.json.get("username")
    current_app.logger.info(f"User {username} is checking their portfolio")

    if not username: 
        current_app.logger.error("Username is required")
        return jsonify({"status": "error", "message": "Username is required"}), 400 
    
    user = db.session.get(User, username)
    if not user: 
        current_app.logger.error('User {username} not found')
        return jsonify({"status": "error", "message": "User not found"}), 404 
    
    tickers = user.get_tickers()

    current_app.logger.info(f'Tickers retrieved successfully')
    return jsonify({"status": "success", "portfolio": tickers})
