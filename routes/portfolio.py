from flask import request, jsonify
from data.models import User, Stock, db
import yfinance as yf

@app.route('/portfolio', methods=['GET'])
def portfolio():
    """
    Displays user's current stock portfolio and its total value.

    Args:
        None

    Returns:
        JSON: A message with the portfolio details and total value.
    """

    username = request.json.get("username")

    if not username: 
        return jsonify({"status": "error", "message": "Username is required"}), 400 
    
    user = db.session.get(User, username)
    if not user: 
        return jsonify({"status": "error", "message": "User not found"}), 404 
    
    tickers = user.get_tickers()
    return jsonify({"status": "success", "portfolio": tickers})
