from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import requests
import sys

# Add proto path
sys.path.append('/app/proto')
sys.path.append('/app')

from grpc_client import UserServiceClient, ProductServiceClient

app = Flask(__name__)
CORS(app)

# Database configuration
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'postgres')
db_host = os.getenv('DB_HOST', 'postgres-db')
db_name = os.getenv('DB_NAME', 'order_db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Service URLs for inter-service communication (HTTP fallback)
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user-service:5001')
PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://product-service:5002')

# gRPC clients
USER_GRPC_HOST = os.getenv('USER_GRPC_HOST', 'user-service')
USER_GRPC_PORT = os.getenv('USER_GRPC_PORT', '50051')
PRODUCT_GRPC_HOST = os.getenv('PRODUCT_GRPC_HOST', 'product-service')
PRODUCT_GRPC_PORT = os.getenv('PRODUCT_GRPC_PORT', '50052')

# Initialize gRPC clients
user_grpc_client = UserServiceClient(USER_GRPC_HOST, USER_GRPC_PORT)
product_grpc_client = ProductServiceClient(PRODUCT_GRPC_HOST, PRODUCT_GRPC_PORT)


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'total_price': self.total_price,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


def validate_user(user_id, use_grpc=True):
    """Validate that user exists by calling User Service (via gRPC or HTTP)"""
    if use_grpc:
        try:
            user = user_grpc_client.get_user(user_id)
            return user is not None
        except Exception as e:
            print(f'gRPC error validating user: {e}, falling back to HTTP')
            # Fallback to HTTP
            pass
    
    try:
        response = requests.get(f'{USER_SERVICE_URL}/users/{user_id}', timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f'Error validating user: {e}')
        return False


def validate_product(product_id, use_grpc=True):
    """Validate that product exists by calling Product Service (via gRPC or HTTP)"""
    if use_grpc:
        try:
            product = product_grpc_client.get_product(product_id)
            return product
        except Exception as e:
            print(f'gRPC error validating product: {e}, falling back to HTTP')
            # Fallback to HTTP
            pass
    
    try:
        response = requests.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}', timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f'Error validating product: {e}')
        return None


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        db.session.execute(db.text('SELECT 1'))
        return jsonify({'status': 'healthy', 'service': 'order-service'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503


@app.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order by ID"""
    try:
        order = Order.query.get_or_404(order_id)
        return jsonify(order.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/orders', methods=['POST'])
def create_order():
    """Create a new order with inter-service validation"""
    try:
        data = request.get_json()
        
        if not data or not data.get('user_id') or not data.get('product_id') or not data.get('quantity'):
            return jsonify({'error': 'user_id, product_id, and quantity are required'}), 400
        
        user_id = int(data['user_id'])
        product_id = int(data['product_id'])
        quantity = int(data['quantity'])
        
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be positive'}), 400
        
        # Validate user exists (using gRPC)
        if not validate_user(user_id, use_grpc=True):
            return jsonify({'error': 'User not found'}), 404
        
        # Validate product exists and get price (using gRPC)
        product = validate_product(product_id, use_grpc=True)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Calculate total price
        total_price = float(product['price']) * quantity
        
        order = Order(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify(order.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': 'Invalid data format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5003, debug=True)

