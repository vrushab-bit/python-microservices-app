# Python Microservices Application

A microservices application built with Flask, PostgreSQL, React, and Docker Compose. This application demonstrates a microservices architecture with an API Gateway, core services with inter-service communication, and a React frontend.

## Architecture

### Services

1. **API Gateway Service** (`gateway-service`)
   - Single entry point for all API requests
   - Routes requests to appropriate microservices
   - Port: 5000

2. **User Service** (`user-service`)
   - Manages user data (CRUD operations)
   - PostgreSQL database: `user_db`
   - Port: 5001 (internal)

3. **Product Service** (`product-service`)
   - Manages product catalog (CRUD operations)
   - PostgreSQL database: `product_db`
   - Port: 5002 (internal)

4. **Order Service** (`order-service`)
   - Manages orders
   - Demonstrates inter-service communication by validating users and products
   - PostgreSQL database: `order_db`
   - Port: 5003 (internal)

### Frontend

- **React Application** (`frontend`)
   - Vite-based React app
   - UI for managing users, products, and orders
   - Port: 3000

## Prerequisites

- Docker and Docker Compose installed
- Git (optional)

## Getting Started

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd python-microservice-app
   ```

2. **Start all services**:
   ```bash
   docker-compose up --build
   ```

   This will:
   - Build all Docker images
   - Start PostgreSQL databases
   - Initialize databases
   - Start all microservices
   - Start the frontend

3. **Access the application**:
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost:5000
   - Health checks:
     - Gateway: http://localhost:5000/health
     - User Service: http://localhost:5000/api/users (via gateway)

## API Endpoints

All API requests go through the Gateway at `http://localhost:5000/api`

### Users
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get user by ID
- `POST /api/users` - Create user
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com"
  }
  ```
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user

### Products
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get product by ID
- `POST /api/products` - Create product
  ```json
  {
    "name": "Product Name",
    "price": 29.99,
    "description": "Product description"
  }
  ```
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Orders
- `GET /api/orders` - Get all orders
- `GET /api/orders/<id>` - Get order by ID
- `POST /api/orders` - Create order (validates user and product exist)
  ```json
  {
    "user_id": 1,
    "product_id": 1,
    "quantity": 2
  }
  ```

## Inter-Service Communication

The Order Service demonstrates inter-service communication:
- When creating an order, it validates that the user exists by calling the User Service
- It validates that the product exists and retrieves the price from the Product Service
- The total price is calculated based on the product price and quantity

## Project Structure

```
python-microservice-app/
├── services/
│   ├── gateway-service/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── user-service/
│   │   ├── app.py
│   │   ├── init_db.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── product-service/
│   │   ├── app.py
│   │   ├── init_db.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── order-service/
│       ├── app.py
│       ├── init_db.py
│       ├── requirements.txt
│       └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Development

### Running Individual Services

You can run services individually for development:

```bash
# User Service
cd services/user-service
pip install -r requirements.txt
python app.py
```

### Database Access

To access PostgreSQL databases directly:

```bash
# User database
docker exec -it python-microservice-app-user-db-1 psql -U postgres -d user_db

# Product database
docker exec -it python-microservice-app-product-db-1 psql -U postgres -d product_db

# Order database
docker exec -it python-microservice-app-order-db-1 psql -U postgres -d order_db
```

## Stopping Services

```bash
docker-compose down
```

To remove volumes (data will be lost):
```bash
docker-compose down -v
```

## Health Checks

All services expose a `/health` endpoint:
- Gateway: `http://localhost:5000/health`
- User Service: `http://localhost:5000/api/users` (via gateway, or directly at `http://user-service:5001/health`)

## Troubleshooting

1. **Services not starting**: Check Docker logs
   ```bash
   docker-compose logs <service-name>
   ```

2. **Database connection errors**: Ensure databases are healthy before services start (handled by `depends_on`)

3. **Frontend can't connect**: Verify the API Gateway is running and accessible

## Technologies Used

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: React, Vite
- **Infrastructure**: Docker, Docker Compose
- **Communication**: HTTP REST APIs, requests library

## License

This is a demonstration project for testing microservices architecture.

