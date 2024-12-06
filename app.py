from flask import Flask
from data.models import db
from dotenv import load_dotenv
import os
from routes.login import login_bp
from routes.stock import stock_bp

load_dotenv()
app = Flask(__name__)

db_url = "sqlite:///" + os.path.join(app.root_path, "data/data.db")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

app.register_blueprint(login_bp)
app.register_blueprint(stock_bp)

db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
