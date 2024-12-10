from flask import Blueprint, request, jsonify, current_app
from data.models import User, db
import yfinance as yf

sell_bp = Blueprint('sell-stock', __name__)

@sell_bp.route('/sell-stock', methods=['POST'])
def sell_stock():
    """
    Allows a user to sell shares of a specified stock.

    Args:
        JSON: {
            'username': str,
            'ticker': str,
            'quantity': str
        }

    Returns:
        JSON: A message indicating whether the sale was successful or not. 
    """
    
    username = request.json.get("username")
    ticker = request.json.get("ticker")
    quantity = request.json.get("quantity")
    if not username or not ticker or not quantity:
        current_app.logger.error("Missing fields")
        return jsonify({"status": "error", "message": "Missing fields"}), 400 
    
    quantity = int(quantity)
    
    current_app.logger.info(f"User {username} is selling {quantity} shares of {ticker}")
    user = db.session.get(User, username)
    if not user: 
        current_app.logger.error("User not found")
        return jsonify({"status": "error", "message": "User not found"}), 404 
    
    if user.remove_ticker(ticker, quantity):
        db.session.commit()
        current_app.logger.info("Stock removed from portfolio")
        return jsonify({"status": "success", "message": "Stock added to portfolio"}),  200
    
    current_app.logger.error("Insufficient shares or ticker not found")
    return jsonify({"status": "error", "message": "Insufficient shares or ticker not found"}),  400