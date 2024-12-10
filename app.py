from flask import Flask, jsonify
from data.models import db
from sqlalchemy import text
from dotenv import load_dotenv
import os
from routes.login import login_bp
from routes.buy_stock import buy_bp
from routes.sell_stock import sell_bp
from routes.portfolio import port_bp

load_dotenv()
app = Flask(__name__)

db_url = "sqlite:///" + os.path.join(app.root_path, "data/data.db")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

app.register_blueprint(login_bp)
app.register_blueprint(buy_bp)
app.register_blueprint(sell_bp)
app.register_blueprint(port_bp)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/clear-db", methods=["GET"])
def clear_db():
    """
    Route to clear the database. For testing purposes only.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
    return jsonify({"message": "Database cleared"}), 200

# Health checks
@app.route('/health', methods=['GET'])
def healthcheck():
    """
    Health check route to verify the service is running.

    Returns:
        JSON response indicating the health status of the service.
    """
    app.logger.info('Health check')
    return jsonify({'status': 'healthy'}), 200

def check_database_connection():
    """
    Function to check if the database connection is functional.

    Raises:
        Exception: If there is an issue with the database connection.
    """
    app.logger.info("Checking database connection...")
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        app.logger.info("Database connection is OK.")
    except Exception as e:
        error_message = f"Database connection error: {e}"
        app.logger.error(error_message)
        raise Exception(error_message) from e

@app.route('/db-check', methods=['GET'])
def db_check():
    """
    Route to check if the database connection and meals table are functional.

    Returns:
        JSON response indicating the database health status.
    Raises:
        404 error if there is an issue with the database.
    """
    try:
        app.logger.info("Checking database connection...")
        check_database_connection()
        app.logger.info("Database connection is OK.")
        return jsonify({'database_status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)
