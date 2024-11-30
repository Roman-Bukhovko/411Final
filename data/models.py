from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    # https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/
    # https://geekpython.medium.com/easy-password-hashing-using-bcrypt-in-python-3a706a26e4bf
    __tablename__ = "User"
    username: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    password: Mapped[str] = mapped_column(nullable=False)

    def set_password(self, plain_password):
        """
        Hashes the plain password and stores it in the password field.
        
        Args:
            plain_password (str): The plain password to hash.
        
        Returns:
            None.
        """
        self.password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, plain_password):
        """
        Checks if the hashed password matches the plain password.
        
        Args:
            plain_password (str): The plain password to check.
        
        Returns:
            bool: True if the password matches, False otherwise
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.password.encode('utf-8'))
