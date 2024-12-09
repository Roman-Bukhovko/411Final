# Stock Trading Application

## Overview
### The Stock Trading Application is a straightforward and effective tool designed for individual investors who want to manage their portfolios, execute trades, and monitor market conditions.

### API: yfinance 

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Features
1. View My Portfolio

### Displays the user’s current stock holdings, including quantity, the current price of each stock, and the total value of each holding, culminating in an overall portfolio value.

2. "Buy" Stock

### Enables users to purchase shares of a specified stock. The user provides the stock symbol and the number of shares they wish to buy, and the transaction is executed based on the current market price.

3. "Sell" Stock

### Allows users to sell shares of a stock they currently hold. Users specify the stock symbol and the number of shares to sell, and the system processes the sale at the latest market price.

4. Look Up a Stock

### Provides detailed information about a specific stock, including its current market price, historical price data, and a brief description of the company. This feature is useful for conducting research before making buying or selling decisions.

5. Calculate My Portfolio Value

### Calculates the total value of the user's investment portfolio in real-time, reflecting the latest stock prices. This helps users understand the current worth of their investments.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Routes

1. Route: /buy-stock
  - Request Type: POST
  - Purpose: Allows users to purchase shares of a specified stock.
  - Request Body:
    - symbol (String): The stock symbol (e.g., AAPL for Apple).
    - quantity (Integer): The number of shares to buy.
  - Response Format: JSON
    - Success Response Example:
      ### Code: 200
    `{
      "message": "Purchase successful",
      "status": "200",
      "total_cost": 1000
    }`

  - Example Request:

    `{
      "symbol": "AAPL",
      "quantity": 10
    }`

  - Example Response:

    `{
      "message": "Purchase successful",
      "status": "200",
      "total_cost": 1000
    }`


2. Route: /sell-stock
  - Request Type: POST
  - Purpose: Allows users to sell shares of a stock they currently hold.
  - Request Body:
    - symbol (String): The stock symbol (e.g., AAPL for Apple).
    - quantity (Integer): The number of shares to sell.
  - Response Format: JSON
    - Success Response Example:
      ### Code: 200
    `{
      "message": "Sale successful",
      "status": "200",
      "total_revenue": 900
    }`

  - Example Request:

    `{
      "symbol": "AAPL",
      "quantity": 5
    }`

  - Example Response:

    `{
      "message": "Sale successful",
      "status": "200",
      "total_revenue": 900
    }`


3. Route: /portfolio
  - Request Type: GET
  - Purpose: Retrieves the user's current stock holdings and the total portfolio value.
  - Request Body: None
  - Response Format: JSON
    - Success Response Example:
      ### Code: 200
    `{
      "stocks": [
        {
          "symbol": "AAPL",
          "quantity": 10,
          "current_price": 150,
          "total_value": 1500
        },
        {
          "symbol": "GOOGL",
          "quantity": 5,
          "current_price": 2000,
          "total_value": 10000
        }
      ],
      "portfolio_value": 11500
    }`

  -  Example Request:
    `{
      // No request body is needed, simply request the portfolio.
    }`

  - Example Response:
      `{
        "stocks": [
          {
            "symbol": "AAPL",
            "quantity": 10,
            "current_price": 150,
            "total_value": 1500
          },
          {
            "symbol": "GOOGL",
            "quantity": 5,
            "current_price": 2000,
            "total_value": 10000
          }
        ],
        "portfolio_value": 11500
      }`


4. Route: /stock-info
  - Request Type: GET
  - Purpose: Provides detailed information about a specific stock.
  - Request Body: None
  - Response Format: JSON
    - Success Response Example:
      ### Code: 200
    `{
      "symbol": "AAPL",
      "current_price": 150,
      "historical_prices": [
        {"date": "2024-11-20", "price": 145},
        {"date": "2024-11-19", "price": 148}
      ],
      "description": "Apple Inc."
    }`

  - Example Request:

    `{
      "symbol": "AAPL"
    }`

  - Example Response:
    `{
      "symbol": "AAPL",
      "current_price": 150,
      "historical_prices": [
        {"date": "2024-11-20", "price": 145},
        {"date": "2024-11-19", "price": 148}
      ],
      "description": "Apple Inc."
    }`


5. Route: /portfolio-value
  - Request Type: GET
  - Purpose: Calculates the total value of the user's portfolio in real-time, reflecting the latest stock prices.
  - Request Body: None
  - Response Format: JSON
    - Success Response Example:
      ### Code: 200
      `{
        "total_value": 11500,
        "stocks": [
          {"symbol": "AAPL", "quantity": 10, "current_price": 150, "total_value": 1500},
          {"symbol": "GOOGL", "quantity": 5, "current_price": 2000, "total_value": 10000}
        ]
      }`

  - Example Request:
    `{
      // No request body is needed for this route.
    }`

  - Example Response:
    `{
      "total_value": 11500,
      "stocks": [
        {"symbol": "AAPL", "quantity": 10, "current_price": 150, "total_value": 1500},
        {"symbol": "GOOGL", "quantity": 5, "current_price": 2000, "total_value": 10000}
      ]
    }`
