#!/bin/bash

# Simple test script without colors (for environments without color support)


API_BASE="https://tosapp.non-prod.oneassure.in/api"
GATEWAY_BASE="https://tosapp.non-prod.oneassure.in"

echo "========================================"
echo "Microservices API Test Script"
echo "========================================"
echo ""

# Test Gateway Health
echo "1. Testing Gateway Health..."
curl -s "${GATEWAY_BASE}/health" | jq .
echo ""

# Create User
echo "2. Creating User..."
USER_RESPONSE=$(curl -s -X POST "${API_BASE}/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com"}')
echo $USER_RESPONSE | jq .
USER_ID=$(echo $USER_RESPONSE | jq -r '.id')
echo ""

# Create Product
echo "3. Creating Product..."
PRODUCT_RESPONSE=$(curl -s -X POST "${API_BASE}/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 49.99, "description": "Test description"}')
echo $PRODUCT_RESPONSE | jq .
PRODUCT_ID=$(echo $PRODUCT_RESPONSE | jq -r '.id')
echo ""

# Create Order
echo "4. Creating Order..."
ORDER_RESPONSE=$(curl -s -X POST "${API_BASE}/orders" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": ${USER_ID}, \"product_id\": ${PRODUCT_ID}, \"quantity\": 3}")
echo $ORDER_RESPONSE | jq .
echo ""

# Get All
echo "5. Getting All Users..."
curl -s "${API_BASE}/users" | jq .
echo ""

echo "6. Getting All Products..."
curl -s "${API_BASE}/products" | jq .
echo ""

echo "7. Getting All Orders..."
curl -s "${API_BASE}/orders" | jq .
echo ""

echo "Test completed!"

