from flask import Blueprint, request, jsonify, current_app
from data.models import User, db
import yfinance as yf

stock_bp = Blueprint('stock-info', __name__)

@stock_bp.route('/stock-info', methods=['POST'])
def stock_info():
    """
    Displays user's current stock portfolio value.

    Args:
        JSON: {
            'ticker': str,
        }

    Returns:
        JSON: {
            'status': str,
            'ticker': str,
            'last_prices': list,
            'volumes': list
        }
    """
    ticker = request.json.get("ticker")
    current_app.logger.info(f"User is checking the value of {ticker}")


    if not ticker:
        current_app.logger.error("Ticker is required")
        return jsonify({"status": "error", "message": "Ticker is required"}), 400
    
    try:
        stock = yf.Ticker(ticker)
        last_prices = stock.history(period="5d")["Close"].values
        prices_arr = last_prices.tolist()
        volumes = stock.history(period="5d")["Volume"].values
        volumes_arr = volumes.tolist()
        return jsonify({"status": "success", "ticker": ticker, "last_prices": prices_arr, "volumes": volumes_arr})
    except:
        current_app.logger.error("Invalid ticker")
        return jsonify({"status": "error", "message": "Invalid ticker"}), 404