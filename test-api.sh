#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color


API_BASE="https://tosapp.non-prod.oneassure.in/api"
GATEWAY_BASE="https://tosapp.non-prod.oneassure.in"


echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Microservices API Test Script${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Test Gateway Health
echo -e "${YELLOW}1. Testing Gateway Health...${NC}"
curl -s "${GATEWAY_BASE}/health" | jq .
echo -e "\n"

# Test User Service
echo -e "${YELLOW}2. Testing User Service...${NC}"
echo -e "${GREEN}Creating User 1...${NC}"
USER1_RESPONSE=$(curl -s -X POST "${API_BASE}/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john.doe@example.com"}')
echo $USER1_RESPONSE | jq .
USER1_ID=$(echo $USER1_RESPONSE | jq -r '.id')

echo -e "\n${GREEN}Creating User 2...${NC}"
USER2_RESPONSE=$(curl -s -X POST "${API_BASE}/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Smith", "email": "jane.smith@example.com"}')
echo $USER2_RESPONSE | jq .
USER2_ID=$(echo $USER2_RESPONSE | jq -r '.id')

echo -e "\n${GREEN}Getting All Users...${NC}"
curl -s "${API_BASE}/users" | jq .

echo -e "\n${GREEN}Getting User by ID (${USER1_ID})...${NC}"
curl -s "${API_BASE}/users/${USER1_ID}" | jq .

echo -e "\n${GREEN}Updating User ${USER1_ID}...${NC}"
curl -s -X PUT "${API_BASE}/users/${USER1_ID}" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Updated", "email": "john.updated@example.com"}' | jq .

# Test Product Service
echo -e "\n${YELLOW}3. Testing Product Service...${NC}"
echo -e "${GREEN}Creating Product 1...${NC}"
PRODUCT1_RESPONSE=$(curl -s -X POST "${API_BASE}/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "description": "High-performance laptop"}')
echo $PRODUCT1_RESPONSE | jq .
PRODUCT1_ID=$(echo $PRODUCT1_RESPONSE | jq -r '.id')

echo -e "\n${GREEN}Creating Product 2...${NC}"
PRODUCT2_RESPONSE=$(curl -s -X POST "${API_BASE}/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mouse", "price": 29.99, "description": "Wireless mouse"}')
echo $PRODUCT2_RESPONSE | jq .
PRODUCT2_ID=$(echo $PRODUCT2_RESPONSE | jq -r '.id')

echo -e "\n${GREEN}Creating Product 3...${NC}"
PRODUCT3_RESPONSE=$(curl -s -X POST "${API_BASE}/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Keyboard", "price": 79.99, "description": "Mechanical keyboard"}')
echo $PRODUCT3_RESPONSE | jq .
PRODUCT3_ID=$(echo $PRODUCT3_RESPONSE | jq -r '.id')

echo -e "\n${GREEN}Getting All Products...${NC}"
curl -s "${API_BASE}/products" | jq .

echo -e "\n${GREEN}Getting Product by ID (${PRODUCT1_ID})...${NC}"
curl -s "${API_BASE}/products/${PRODUCT1_ID}" | jq .

echo -e "\n${GREEN}Updating Product ${PRODUCT1_ID}...${NC}"
curl -s -X PUT "${API_BASE}/products/${PRODUCT1_ID}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop Pro", "price": 1299.99, "description": "Updated high-performance laptop"}' | jq .

# Test Order Service
echo -e "\n${YELLOW}4. Testing Order Service...${NC}"
echo -e "${GREEN}Creating Order 1 (User ${USER1_ID}, Product ${PRODUCT1_ID}, Quantity 2)...${NC}"
ORDER1_RESPONSE=$(curl -s -X POST "${API_BASE}/orders" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": ${USER1_ID}, \"product_id\": ${PRODUCT1_ID}, \"quantity\": 2}")
echo $ORDER1_RESPONSE | jq .
ORDER1_ID=$(echo $ORDER1_RESPONSE | jq -r '.id')

echo -e "\n${GREEN}Creating Order 2 (User ${USER2_ID}, Product ${PRODUCT2_ID}, Quantity 5)...${NC}"
ORDER2_RESPONSE=$(curl -s -X POST "${API_BASE}/orders" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": ${USER2_ID}, \"product_id\": ${PRODUCT2_ID}, \"quantity\": 5}")
echo $ORDER2_RESPONSE | jq .
ORDER2_ID=$(echo $ORDER2_RESPONSE | jq -r '.id')

echo -e "\n${GREEN}Creating Order 3 (User ${USER1_ID}, Product ${PRODUCT3_ID}, Quantity 1)...${NC}"
ORDER3_RESPONSE=$(curl -s -X POST "${API_BASE}/orders" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": ${USER1_ID}, \"product_id\": ${PRODUCT3_ID}, \"quantity\": 1}")
echo $ORDER3_RESPONSE | jq .
ORDER3_ID=$(echo $ORDER3_RESPONSE | jq -r '.id')

echo -e "\n${GREEN}Getting All Orders...${NC}"
curl -s "${API_BASE}/orders" | jq .

echo -e "\n${GREEN}Getting Order by ID (${ORDER1_ID})...${NC}"
curl -s "${API_BASE}/orders/${ORDER1_ID}" | jq .

# Test Error Cases
echo -e "\n${YELLOW}5. Testing Error Cases...${NC}"
echo -e "${RED}Testing invalid order (non-existent user)...${NC}"
curl -s -X POST "${API_BASE}/orders" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 99999, "product_id": 1, "quantity": 1}' | jq .

echo -e "\n${RED}Testing invalid order (non-existent product)...${NC}"
curl -s -X POST "${API_BASE}/orders" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": ${USER1_ID}, \"product_id\": 99999, \"quantity\": 1}" | jq .

echo -e "\n${RED}Testing invalid order (invalid quantity)...${NC}"
curl -s -X POST "${API_BASE}/orders" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": ${USER1_ID}, \"product_id\": ${PRODUCT1_ID}, \"quantity\": 0}" | jq .

echo -e "\n${RED}Testing duplicate email...${NC}"
curl -s -X POST "${API_BASE}/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "Duplicate", "email": "john.doe@example.com"}' | jq .

# Summary
echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Created Users: ${USER1_ID}, ${USER2_ID}${NC}"
echo -e "${GREEN}Created Products: ${PRODUCT1_ID}, ${PRODUCT2_ID}, ${PRODUCT3_ID}${NC}"
echo -e "${GREEN}Created Orders: ${ORDER1_ID}, ${ORDER2_ID}, ${ORDER3_ID}${NC}"
echo -e "${BLUE}========================================${NC}\n"

