from flask import Flask
from data.models import db, bcrypt
from dotenv import load_dotenv
import os
from routes.login import login_bp


load_dotenv()
app = Flask(__name__)

db_url = "sqlite:///" + os.path.join(app.root_path, "data/data.db")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(login_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
