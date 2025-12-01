# gRPC Integration Guide

This microservices application now supports gRPC communication alongside HTTP REST APIs.

## Architecture

### gRPC Communication Flow

1. **Gateway → Services (gRPC)**
   - Gateway can call User and Product services via gRPC
   - New endpoints: `/api/grpc/users` and `/api/grpc/products`

2. **Order Service → Other Services (gRPC)**
   - Order Service uses gRPC to validate users and products
   - Falls back to HTTP if gRPC fails

3. **Services → Services (gRPC)**
   - User Service exposes gRPC server on port 50051
   - Product Service exposes gRPC server on port 50052

## gRPC Endpoints

### Gateway gRPC Endpoints

All gRPC endpoints are accessible through the Gateway:

#### User Service (via gRPC)
- `GET /api/grpc/users` - Get all users via gRPC
- `GET /api/grpc/users/<id>` - Get user by ID via gRPC
- `POST /api/grpc/users` - Create user via gRPC
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com"
  }
  ```

#### Product Service (via gRPC)
- `GET /api/grpc/products` - Get all products via gRPC
- `GET /api/grpc/products/<id>` - Get product by ID via gRPC
- `POST /api/grpc/products` - Create product via gRPC
  ```json
  {
    "name": "Laptop",
    "price": 999.99,
    "description": "High-performance laptop"
  }
  ```

## Testing gRPC Endpoints

### Using the Test Script

```bash
./test-grpc.sh
```

### Manual Testing

```bash
# Create user via gRPC
curl -X POST http://localhost:8000/api/grpc/users \
  -H "Content-Type: application/json" \
  -d '{"name": "gRPC User", "email": "grpc@example.com"}'

# Get all users via gRPC
curl http://localhost:8000/api/grpc/users

# Create product via gRPC
curl -X POST http://localhost:8000/api/grpc/products \
  -H "Content-Type: application/json" \
  -d '{"name": "gRPC Product", "price": 199.99, "description": "Product via gRPC"}'

# Get all products via gRPC
curl http://localhost:8000/api/grpc/products

# Create order (Order Service uses gRPC internally)
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 1, "quantity": 2}'
```

## Proto Files

Proto definitions are located in `/proto`:
- `user.proto` - User Service gRPC definitions
- `product.proto` - Product Service gRPC definitions

## Service Ports

- **User Service**: HTTP (5001), gRPC (50051)
- **Product Service**: HTTP (5002), gRPC (50052)
- **Order Service**: HTTP (5003) - uses gRPC clients internally
- **Gateway**: HTTP (5000/8000) - exposes gRPC endpoints

## Implementation Details

### gRPC Servers
- User Service: `services/user-service/grpc_server.py`
- Product Service: `services/product-service/grpc_server.py`

### gRPC Clients
- Gateway: `services/gateway-service/grpc_client.py`
- Order Service: `services/order-service/grpc_client.py`

### Proto Compilation
Proto files are automatically compiled during Docker build using `grpc_tools.protoc`.

## Benefits of gRPC

1. **Performance**: Binary protocol is faster than JSON
2. **Type Safety**: Strong typing with Protocol Buffers
3. **Streaming**: Supports bidirectional streaming
4. **Efficiency**: Smaller payload sizes compared to JSON

## Fallback Mechanism

Order Service implements a fallback mechanism:
- First attempts gRPC communication
- Falls back to HTTP REST if gRPC fails
- Ensures reliability and backward compatibility

