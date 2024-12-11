from flask import Blueprint, request, jsonify, current_app
from data.models import User, db
import yfinance as yf

pv_bp = Blueprint('portfolio-value', __name__)

@pv_bp.route('/portfolio-value', methods=['POST'])
def portfolio_value():
    """
    Displays user's current stock portfolio value.

    Args:
        JSON: {
            'username': str,
        }

    Returns:
        JSON: A message with the portfolio value.
    """
    username = request.json.get("username")

    if not username:
        current_app.logger.error("Username is required")
        return jsonify({"status": "error", "message": "Username is required"}), 400
    
    current_app.logger.info(f"User {username} is checking their portfolio value")
    user = db.session.get(User, username)

    if not user:
        current_app.logger.error("User not found")
        return jsonify({"status": "error", "message": "User not found"}), 404
    
    tickers = user.get_tickers()
    total_value = 0
    for ticker in tickers:
        current_app.logger.info(f'Fetching data for {ticker}')
        stock = yf.Ticker(ticker)
        total_value += stock.history(period="1d")["Close"].values[0] * tickers[ticker]
    
    total_value = int(total_value)

    current_app.logger.info(f'Total portfolio value for user {username} is: ${total_value}')
    return jsonify({"status": "success", "portfolio_value": total_value})

