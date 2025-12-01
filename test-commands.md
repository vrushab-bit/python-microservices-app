# API Test Commands

## Prerequisites
Make sure all services are running:
```bash
docker-compose up -d
```

## Gateway Health Check

```bash
curl http://localhost:8000/health
```

## User Service Tests

### Get All Users
```bash
curl http://localhost:8000/api/users
```

### Get User by ID
```bash
curl http://localhost:8000/api/users/1
```

### Create User
```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com"
  }'
```

### Update User
```bash
curl -X PUT http://localhost:8000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Updated",
    "email": "john.updated@example.com"
  }'
```

### Delete User
```bash
curl -X DELETE http://localhost:8000/api/users/1
```

## Product Service Tests

### Get All Products
```bash
curl http://localhost:8000/api/products
```

### Get Product by ID
```bash
curl http://localhost:8000/api/products/1
```

### Create Product
```bash
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "price": 999.99,
    "description": "High-performance laptop"
  }'
```

### Update Product
```bash
curl -X PUT http://localhost:8000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop Pro",
    "price": 1299.99,
    "description": "Updated description"
  }'
```

### Delete Product
```bash
curl -X DELETE http://localhost:8000/api/products/1
```

## Order Service Tests

### Get All Orders
```bash
curl http://localhost:8000/api/orders
```

### Get Order by ID
```bash
curl http://localhost:8000/api/orders/1
```

### Create Order
```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "product_id": 1,
    "quantity": 2
  }'
```

## Error Testing

### Invalid Order - Non-existent User
```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 99999,
    "product_id": 1,
    "quantity": 1
  }'
```

### Invalid Order - Non-existent Product
```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "product_id": 99999,
    "quantity": 1
  }'
```

### Invalid Order - Zero Quantity
```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "product_id": 1,
    "quantity": 0
  }'
```

### Duplicate Email
```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Duplicate",
    "email": "john.doe@example.com"
  }'
```

## Complete Test Flow

```bash
# 1. Create a user
USER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}')
USER_ID=$(echo $USER_RESPONSE | jq -r '.id')
echo "Created User ID: $USER_ID"

# 2. Create a product
PRODUCT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "description": "High-performance laptop"}')
PRODUCT_ID=$(echo $PRODUCT_RESPONSE | jq -r '.id')
echo "Created Product ID: $PRODUCT_ID"

# 3. Create an order
ORDER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": $USER_ID, \"product_id\": $PRODUCT_ID, \"quantity\": 2}")
echo "Created Order:"
echo $ORDER_RESPONSE | jq .

# 4. Verify all data
echo "All Users:"
curl -s http://localhost:8000/api/users | jq .

echo "All Products:"
curl -s http://localhost:8000/api/products | jq .

echo "All Orders:"
curl -s http://localhost:8000/api/orders | jq .
```

## Using jq for Pretty Output

If you have `jq` installed, add `| jq .` to any curl command for formatted JSON output:

```bash
curl http://localhost:8000/api/users | jq .
```

## Testing with HTTPie (Alternative)

If you prefer HTTPie over curl:

```bash
# Install HTTPie: pip install httpie

# Get all users
http GET http://localhost:8000/api/users

# Create user
http POST http://localhost:8000/api/users name="John Doe" email="john@example.com"

# Create product
http POST http://localhost:8000/api/products name="Laptop" price:=999.99 description="High-performance laptop"

# Create order
http POST http://localhost:8000/api/orders user_id:=1 product_id:=1 quantity:=2
```

