from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def set_password(self, plain_password):
        """
        Hashes the plain password and stores it in the password field.
        
        Args:
            plain_password (str): The plain password to hash.
        
        Returns:
            None.
        """
        self.password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, plain_password):
        """
        Checks if the hashed password matches the plain password.
        
        Args:
            plain_password (str): The plain password to check.
        
        Returns:
            bool: True if the password matches, False otherwise
        """
        return bcrypt.check_password_hash(self.password, plain_password)
