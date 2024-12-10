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

# Function to perform HTTP requests and check status codes
function test_route() {
  METHOD=$1
  ROUTE=$2
  EXPECTED_STATUS=$3
  DATA=$4

  if [ "$METHOD" == "POST" ]; then
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$DATA" "$BASE_URL$ROUTE")
  else
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$BASE_URL$ROUTE")
  fi

  if [ "$RESPONSE" == "$EXPECTED_STATUS" ]; then
    echo "PASS: $METHOD $ROUTE (Status: $RESPONSE)"
  else
    echo "FAIL: $METHOD $ROUTE (Expected: $EXPECTED_STATUS, Got: $RESPONSE)"
  fi
}

check_health
check_db
clear_db

test_route "POST" "/register" "200" '{"username": "user1", "password": "password"}'
test_route "POST" "/login" "200" '{"username": "user1", "password": "password"}'
test_route "POST" "/buy-stock" "200" '{"username": "user1", "ticker": "AAPL", "quantity": 10}'
test_route "POST" "/sell-stock" "200" '{"username": "user1", "ticker": "AAPL", "quantity": 5}'
test_route "POST" "/portfolio" "200" '{"username": "user1"}'
test_route "GET" "/invalid-route" "404"

echo "Smoke tests completed."