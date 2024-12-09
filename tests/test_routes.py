import pytest
import json
from app import create_app
from data.models import db, User

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

def test_register(test_client):
    """
    Test user registration. 
    """
    response = test_client.post('/register', data=json.dumps({
        "name": "test",
        "password": "password"
    }))

    assert response.status_code == 200
    assert response.json['status'] == "success"
    assert response.json['message'] == "User created"

def test_login(test_client):
    """
    Test user login. 
    """

    # Register a user
    test_client.post('/register', data=json.dumps({
        "name": "test",
        "password": "password"
    }), content_type='application/json')

    # Test login with the registered user
    response = test_client.post('/login', data=json.dumps({
        "name": "test",
        "password": "password"
    }))

    assert response.status_code == 200
    assert response.json['status'] == "success"
    assert response.json['message'] == "Login successful"

def test_buy_stock():
    """
    Test buying stock. 
    """

    # Register a user
    test_client.post('/register', data=json.dumps({
        "name": "test",
        "password": "password"
    }), content_type='application/json')

    # Buy stock
    response = test_client.post('/buy-stock', data=json.dumps({
        "name": "test",
        "ticker": "AAPL",
        "quantity": 10
    }))

    assert response.status_code == 200
    assert response.json['status'] == "success"
    assert response.json['message'] == "Stock added"

def test_buy_stock():
    """
    Test selling stock. 
    """

    # Register a user
    test_client.post('/register', data=json.dumps({
        "name": "test",
        "password": "password"
    }))

    # Buy stock
    response = test_client.post('/buy-stock', data=json.dumps({
        "name": "test",
        "ticker": "AAPL",
        "quantity": 10
    }))

    #Sell stock
    response = test_client.post('sell-stock', data=json.dumps({
        "name": "test",
        "ticker": "AAPL",
        "quantity": 5
    }))

    assert response.status_code == 200
    assert response.json['status'] == "success"
    assert response.json['message'] == "Stock sold"

def test_portfolio():

    # Register a user and buy stock
    test_client.post('/register', data=json.dumps({
        "name": "test",
        "password": "password"
    }))
    test_client.post('/buy-stock', data=json.dumps({
        "name": "test",
        "ticker": "AAPL",
        "quantity": 10
    }))

    # Check portfolio
    response = test_client.get('/portfolio?name=test')
    assert response.status_code == 200
    assert response.json['status'] == "success"
    assert "AAPL" in response.json['portfolio']