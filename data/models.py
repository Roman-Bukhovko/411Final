from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
import bcrypt
import json

db = SQLAlchemy()

class User(db.Model):
    # https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/
    # https://geekpython.medium.com/easy-password-hashing-using-bcrypt-in-python-3a706a26e4bf
    username: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    password: Mapped[str] = mapped_column(nullable=False)
    tickers: Mapped[list[str]] = mapped_column(Text, nullable=False, default='{"tickers": {}}')

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
    
    def add_ticker(self, ticker, amount):
        """
        Adds some amount of a ticker to the user's list of tickers.
        
        Args:
            ticker (str): The ticker to add.
        
        Returns:
            None.
        """
        json_tickers = json.loads(self.tickers)
        if ticker not in json_tickers['tickers']:
            json_tickers['tickers'][ticker] = 0
        json_tickers['tickers'][ticker] += amount
        self.tickers = json.dumps(json_tickers)

    def remove_ticker(self, ticker, amount):
        """
        Removes some amount of a ticker from the user's list of tickers.
        
        Args:
            ticker (str): The ticker to remove.
        
        Returns:
            bool: True if the ticker was removed, False otherwise
        """
        json_tickers = json.loads(self.tickers)
        if ticker in json_tickers['tickers']:
            if json_tickers['tickers'][ticker] >= amount:
                json_tickers['tickers'][ticker] -= amount
                self.tickers = json.dumps(json_tickers)
                return True
            return False
        return False

    def get_tickers(self):
        """
        Returns the user's list of tickers.
        
        Returns:
            list[str]: The user's list of tickers.
        """
        return json.loads(self.tickers)['tickers']