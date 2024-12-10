#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000"

#echo "BASE_URL is set to: $BASE_URL"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

clear_db() {
  echo "Clearing database..."
  curl -s -X GET "$BASE_URL/clear-db" | grep -q '"message": "Database cleared"'
  if [ $? -eq 0 ]; then
    echo "Database cleared."
  else
    echo "Failed to clear database."
    exit 1
  fi
}

###############################################
#
# Stock Operations
#
###############################################

buy_stock() {
  username=$1
  ticker=$2
  quantity=$3

  echo "Buying stock ($ticker)..."
  response=$(curl -s -X POST "$BASE_URL/buy-stock" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"ticker\":\"$ticker\", \"quantity\":$quantity}")
  
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Bought stock ($ticker) successfully."
  else
    echo "Failed to buy stock ($ticker). Response: $response"
    exit 1
  fi
}

sell_stock() {
  username=$1
  ticker=$2
  quantity=$3

  echo "Selling stock ($ticker)..."
  response=$(curl -s -X POST "$BASE_URL/sell-stock" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"ticker\":\"$ticker\", \"quantity\":$quantity}")
  
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Sold stock ($ticker) successfully."
  else
    echo "Failed to sell stock ($ticker). Response: $response"
    exit 1
  fi
}

get_portfolio() {
  username=$1

  echo "Fetching portfolio for user ($username)..."
  response=$(curl -s -X POST "$BASE_URL/portfolio" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\"}")
  
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Retrieved portfolio for user ($username)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Portfolio JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve portfolio. Response: $response"
    exit 1
  fi
}

get_stock_info() {
  ticker=$1

  echo "Fetching stock info for ticker ($ticker)..."
  response=$(curl -s -X POST "$BASE_URL/stock-info" -H "Content-Type: application/json" \
    -d "{\"ticker\":\"$ticker\"}")
  
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Retrieved stock info for ($ticker)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Stock Info JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve stock info for ($ticker). Response: $response"
    exit 1
  fi
}

get_portfolio_value() {
  username=$1

  echo "Fetching portfolio value for user ($username)..."
  response=$(curl -s -X POST "$BASE_URL/portfolio-value" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\"}")
  
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Retrieved portfolio value for user ($username)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Portfolio Value JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve portfolio value. Response: $response"
    exit 1
  fi
}

check_health
check_db
clear_db

buy_stock "testuser" "AAPL" 10
get_portfolio "testuser"
get_stock_info "AAPL"
sell_stock "testuser" "AAPL" 5
get_portfolio_value "testuser"

echo "Smoke tests completed."