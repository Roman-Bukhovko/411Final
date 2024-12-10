from flask import Blueprint, request, jsonify
from data.models import User, Stock, db
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
    
    username = request.form.get("username")
    ticker = request.form.get("ticker")
    quantity = request.form.get("quantity")

    if not username or not ticker or not quantity:
        return jsonify({"status": "error", "message": "Missing fields"}), 400 
    
    user = db.session.get(User, username)
    if not user: 
        return jsonify({"status": "error", "message": "User not found"}), 404 
    
    if user.remove_ticker(ticker, quantity):
        db.seesion.commit()
        return jsonify({"status": "success", "message": "Stock added to portfolio"}),  200
    
    return jsonify({"status": "error", "message": "Insufficient shares or ticker not found"}),  400