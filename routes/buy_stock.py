from flask import Blueprint, request, jsonify
from data.models import User, Stock, db
import yfinance as yf

buy_bp = Blueprint('buy-stock', __name__)

@app.route('/buy-stock', methods=['POST'])
def buy_stock():
    """
    Allows a user to purchase shares of a specified stock.

    Args:
        JSON: {
            'username': str,
            'ticker': str,
            'quantity': str
        }

    Returns:
        JSON: A message indicating whether the purchase was successful or not. 
    """

    username = request.json.get("username")
    ticker = request.json.get("ticker")
    quantity = request.json.get("quantity")

    if not username or not ticker or not quantity:
        return jsonify({"status": "error", "message": "Missing fields"}), 400 
    
    user = db.session.get(User, username)
    if not user: 
        return jsonify({"status": "error", "message": "User not found"}), 404 
    
    user.add_ticker(ticker, quantity)
    db.seesion.commit()
    return jsonify({"status": "success", "message": "Stock added to portfolio"}),  200