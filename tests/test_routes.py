import pytest
import json
from app import create_app
from data.models import db, User
from unittest.mock import patch

@pytest.fixture
def test_client():
    """
    Fixture to set up a test client and a database.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        

#########################
#Login Unit Tests
#########################

def test_register(test_client):
    """
    Test user registration. 
    """
    response = test_client.post('/register', data=json.dumps({
        "username": "unique_test",
        "password": "password"
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == "User created"

def test_register_duplicate(test_client):
    """
    Test user registration for duplicate users
    """

    #Register a user
    response = test_client.post('/register', data=json.dumps({
        "username": "new_test",
        "password": "password"
    }), content_type='application/json')
    
    assert response.status_code == 200
    assert response.json['status'] == 'User created'

    #Register same user again
    response = test_client.post('/register', data=json.dumps({
        "username": "new_test",
        "password": "password"
    }), content_type='application/json')

    assert response.status_code == 400
    assert response.json['status'] == "Username already exists"

def test_register_missing_credentials(test_client):
    """
    Test user registration with missing fields
    """

    response = test_client.post('/register', data=json.dumps({
        "username": "test"}), content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == "Missing name or password"

def test_login(test_client):
    """
    Test user login. 
    """

    # Register a user
    test_client.post('/register', data=json.dumps({
        "username": "unique_test1",
        "password": "password"
    }), content_type='application/json')

    # Test login with the registered user
    response = test_client.post('/login', data=json.dumps({
        "username": "unique_test1",
        "password": "password"
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == "Login successful"

def test_login_missing_credentials(test_client):
    """
    Test the login of users with missing credentials
    """
    response = test_client.post('/login', json={
        "username": "test"
    })

    assert response.status_code == 200
    assert response.json['status'] == "Missing username or password"

def test_login_wrong_credentials(test_client):
    """
    Test the login of users with wrong credentials
    """
    # Register a user
    test_client.post('/register', data=json.dumps({
        "username": "test",
        "password": "password"
    }), content_type='application/json')

    #Try login with wrong credentials
    response = test_client.post('/login', data=json.dumps({
        "username": "test",
        "password": "None"
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == "Invalid credentials"

def test_change_password(test_client):
    """Test the successful password change
    """

    #Register a new user
    test_client.post('/register', data=json.dumps({
        "username":"unique_test2",
        "password": "password"
        }), content_type='application/json')
    #Change their password and note response
    response = test_client.post('/change-password', data=json.dumps({
        "username": "unique_test2", 
        "old_password": "password", 
        "new_password": "new_password"
        }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == "Password changed"

def test_change_password_missing_fields(test_client):
    """Test change_password with missing required fields
    """

    #Register a new user
    test_client.post('/regiser', data=json.dumps({
        "username": "test", 
        "password": "password"
        }), content_type='application/json')

    #Try to change password with missing field

    response = test_client.post('/change-password', data=json.dumps({
        "username": "test",
        "old_password": "password"
        }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == "Missing required fields"

def test_change_password_wrong_credentials(test_client):
    """Test change_password with non existent user
    """
    #Change password without registering user first
    response = test_client.post('/change-password', data=json.dumps({
        "username": "test",
        "old_password": "password",
        "new_password": "new_password"
        }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == "Invalid credentials"

#########################
#Buy Unit Tests
#########################

def test_buy_stock(test_client):
    """
    Test successfully buying stock. 
    """

    # Register a user
    test_client.post('/register', data=json.dumps({
        "username": "test",
        "password": "password"
    }), content_type='application/json')

    # Buy stock
    response = test_client.post('/buy_stock', data=json.dumps({
        "username": "test",
        "ticker": "AAPL",
        "quantity": 10
    }))

    assert response.status_code == 200
    assert response.json['status'] == "success"
    assert response.json['message'] == "Stock added"

def test_buy_stock_missing_fields(test_client):
    """
    Test buy stock with no specified quantity
    """

    # Register a user
    test_client.post('/register', data=json.dumps({
        "username": "test",
        "password": "password"
    }), content_type='application/json')

    # Try to buy stock
    response = test_client.post('/buy-stock', data=json.dumps({
        "username": "test",
        "ticker": "AAPL"
    }), content_type='application/json')

    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'Missing fields'

def test_buy_stock_no_user(test_client):
    """Test buy_stock with non-existent user
    """
    
    #Try to buy stock 
    response = test_client.post('/buy-stock', data=json.dumps({
        "username": "None",
        "ticker": "AAPL", 
        "quantity": 10
    }), content_type='application/json')

    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert response.json['message'] == "User not found"

#########################
#Sell Unit Tests
#########################

def test_sell_stock(test_client):
    """
    Test successful selling stock. 
    """

    # Register a user
    test_client.post('/register', data=json.dumps({
        "username": "test",
        "password": "password"
    }), content_type='application/json')

    # Buy stock
    test_client.post('/buy-stock', data=json.dumps({
        "username": "test",
        "ticker": "AAPL",
        "quantity": 10
    }), content_type='application/json')

    #Sell stock
    response = test_client.post('/sell-stock', data=json.dumps({
        "username": "test",
        "ticker": "AAPL",
        "quantity": 5
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == "success"
    assert response.json['message'] == "Stock added to portfolio"

def test_sell_stock_missing_fields(test_client):
    """
    Test selling stock with no specified quantity
    """

    # Register a user
    test_client.post('/register', data=json.dumps({
        "username": "unique_test3",
        "password": "password"
    }), content_type='application/json')

    # Buy stock
    test_client.post('/buy-stock', data=json.dumps({
        "username": "unique_test3",
        "ticker": "AAPL",
        "quantity": 10
    }), content_type='application/json')

    #Try to sell
    response = test_client.post('/sell-stock', data=json.dumps({
        "username":"unique_test3", 
        "ticker": "AAPL"
        }), content_type='application/json')
    
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert response.json['message'] == "Missing fields"

def test_sell_stock_insufficient(test_client):
    """
    Test trying to sell more than what you bought in shares
    """
    # Register a user
    test_client.post('/register', data=json.dumps({
        "username": "unique_test4",
        "password": "password"
    }), content_type='application/json')

    # Buy stock
    test_client.post('/buy-stock', data=json.dumps({
        "username": "unique_test4",
        "ticker": "AAPL",
        "quantity": 5
    }), content_type='application/json')

    # Sell more than what you have

    response = test_client.post('/sell-stock', data=json.dumps({
        "username": "unique_test4", 
        "ticker": "AAPL", 
        "quantity": 10
        }), content_type='application/json')
    
    assert response.status_code == 400
    assert response.json['status'] == "error"
    assert response.json['message'] == "Insufficient shares or ticker not found"

def test_sell_stock_no_user(test_client):
    """Test selling stock of a non-existent user
    """
    # Sell without registering first

    response = test_client.post('/sell-stock', data=json.dumps({
        "username":"none", 
        "ticker": "AAPL",
        "quantity": 10
        }), content_type='application/json')

    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == "User not found"

#########################
# Portfolio Unit Tests
#########################
def test_portfolio(test_client):
    """
    Tests the successfull viewing of portfolio
    """
    # Register a user and buy stock
    test_client.post('/register', data=json.dumps({
        "username": "test",
        "password": "password"
    }), content_type='application/json')

    test_client.post('/buy-stock', data=json.dumps({
        "username": "test",
        "ticker": "AAPL",
        "quantity": 10
    }), content_type='application/json')

    # Check portfolio
    response = test_client.post('/portfolio', data=json.dumps({
        "username": "test"
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == "success"
    assert "AAPL" in response.json['portfolio']

def test_portfolio_no_user(test_client):
    """
    Test vieweing of portfolio when user doesn't exist
    """
    
    response = test_client.post('/portfolio', data=json.dumps({
        "username": "not_real"
        }), content_type='application/json')
    
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'User not found'

def test_porfolio_invalid(test_client):
    """
    Test portfolio with invalid username
    """
    response = test_client.post('/portfolio', data=json.dumps({
        
        }), content_type='application/json')

    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert response.json['message'] == "Username is required"

#########################
# Portfolio Value Unit Tests
#########################

def test_portfolio_value(test_client):
    """
    Test porfolio_value successfully
    """

    #Register a new user and buy stock
    test_client.post('/register', data=json.dumps({
        "username": "test",
        "password": "password"
    }))
    test_client.post('/buy-stock', data=json.dumps({
        "username": "test",
        "ticker": "AAPL",
        "quantity": 10
    }))

    #Mock the yfinance ticker
    with patch('yfinance.Ticker') as MockTicker:
        mock_ticker = MockTicker.return_value
        mock_ticker.history.return_value = {"Close": [100]} #random num

        response = test_client.post('/portfolio-value', json={"username": "test"})

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['portfolio_value'] == 1000 #(100* 10 shares)

def test_portfolio_value_no_user(test_client):
    """
    Tests in case there's no user
    """
    
    response = test_client.post('/portfolio-value', json={"username": "non existent"})

    assert response.status_code == 404
    assert response.json['status'] == "error"
    assert response.json['message'] == "User not found"

def test_portfolio_value_missing_fields(test_client):
    """
    Tests in case username is missing
    """
    response = test_client.post('/portfolio-value', json={})

    assert response.status_code == 400
    assert response.json['status'] == "error"
    assert response.json['message'] == "Username is required"

#########################
# Stock Info Unit Tests
#########################

def test_stock_info(test_client):
    """
    Test successful retrieval of stock info
    """

    #use mock to return fake stock info
    with patch('yfinance.Ticker') as MockTicker:
        mock_ticker = MockTicker.return_value
        mock_ticker.history.return_value = {
            "Close": [100, 101, 102, 103, 104],  # Last 5 closing prices
            "Volume": [100000, 110000, 120000, 130000, 140000]  # Last 5 volumes
        }

        response = test_client.post('/stock_info', json={"ticker": "AAPL"})

    assert response.status_code == 200
    assert response.json['status'] == "success"
    assert response.json['ticker'] == "AAPL"
    assert response.json['last_prices'] == [100, 101, 102, 103, 104]
    assert response.json['volumes'] == [100000, 110000, 120000, 130000, 140000]

def test_stock_info_missing_fields(test_client):
    """
    Test stock info without specifying the ticker
    """
    response = test_client.post('/stock-info', json={})

    assert response.status_code == 400
    assert response.json['status'] == "error"
    assert response.json['message'] == "Ticker is required"

def test_stock_info_invalid_ticker(test_client):
    """
    Test when we plug in an invalid ticker
    """

    with patch('yfinance.Ticker') as MockTicker:
        mock_ticker = MockTicker.return_value
        mock_ticker.history.side_effect = Exception("Invalid ticker")

        response = test_client.post('/stock-info', json={"ticker": "INVALID_TICKER"})

    assert response.status_code == 404
    assert response.json['status'] == "error"
    assert response.json['message'] == "Invalid ticker"
