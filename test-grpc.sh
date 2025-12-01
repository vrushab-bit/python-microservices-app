#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_BASE="http://localhost:8000/api"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}gRPC Endpoints Test Script${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Test gRPC User Endpoints
echo -e "${YELLOW}1. Testing gRPC User Endpoints...${NC}"

echo -e "${GREEN}Creating User via gRPC...${NC}"
USER_RESPONSE=$(curl -s -X POST "${API_BASE}/grpc/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "gRPC User", "email": "grpc.user@example.com"}')
echo $USER_RESPONSE | jq .
USER_ID=$(echo $USER_RESPONSE | jq -r '.id')

echo -e "\n${GREEN}Getting All Users via gRPC...${NC}"
curl -s "${API_BASE}/grpc/users" | jq .

echo -e "\n${GREEN}Getting User by ID (${USER_ID}) via gRPC...${NC}"
curl -s "${API_BASE}/grpc/users/${USER_ID}" | jq .

# Test gRPC Product Endpoints
echo -e "\n${YELLOW}2. Testing gRPC Product Endpoints...${NC}"

echo -e "${GREEN}Creating Product via gRPC...${NC}"
PRODUCT_RESPONSE=$(curl -s -X POST "${API_BASE}/grpc/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "gRPC Product", "price": 199.99, "description": "Product created via gRPC"}')
echo $PRODUCT_RESPONSE | jq .
PRODUCT_ID=$(echo $PRODUCT_RESPONSE | jq -r '.id')

echo -e "\n${GREEN}Getting All Products via gRPC...${NC}"
curl -s "${API_BASE}/grpc/products" | jq .

echo -e "\n${GREEN}Getting Product by ID (${PRODUCT_ID}) via gRPC...${NC}"
curl -s "${API_BASE}/grpc/products/${PRODUCT_ID}" | jq .

# Test Order Service using gRPC (internally)
echo -e "\n${YELLOW}3. Testing Order Service (uses gRPC internally)...${NC}"

echo -e "${GREEN}Creating Order (Order Service uses gRPC to validate user and product)...${NC}"
ORDER_RESPONSE=$(curl -s -X POST "${API_BASE}/orders" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": ${USER_ID}, \"product_id\": ${PRODUCT_ID}, \"quantity\": 2}")
echo $ORDER_RESPONSE | jq .

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}gRPC Test Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Created User via gRPC: ${USER_ID}${NC}"
echo -e "${GREEN}Created Product via gRPC: ${PRODUCT_ID}${NC}"
echo -e "${GREEN}Order Service uses gRPC internally for validation${NC}"
echo -e "${BLUE}========================================${NC}\n"

