from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import sys

# Add proto path
sys.path.append('/app/proto')
sys.path.append('/app')

from grpc_client import UserServiceClient, ProductServiceClient

app = Flask(__name__)
CORS(app)

# Service URLs (using Docker service names)
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user-service:5001')
PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://product-service:5002')
ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://order-service:5003')

# gRPC clients
USER_GRPC_HOST = os.getenv('USER_GRPC_HOST', 'user-service')
USER_GRPC_PORT = os.getenv('USER_GRPC_PORT', '50051')
PRODUCT_GRPC_HOST = os.getenv('PRODUCT_GRPC_HOST', 'product-service')
PRODUCT_GRPC_PORT = os.getenv('PRODUCT_GRPC_PORT', '50052')

# Initialize gRPC clients
user_grpc_client = UserServiceClient(USER_GRPC_HOST, USER_GRPC_PORT)
product_grpc_client = ProductServiceClient(PRODUCT_GRPC_HOST, PRODUCT_GRPC_PORT)


def proxy_request(service_url, path, method='GET', data=None, json_data=None):
    """Proxy request to a microservice"""
    try:
        url = f"{service_url}{path}"
        if method == 'GET':
            response = requests.get(url, timeout=5)
        elif method == 'POST':
            response = requests.post(url, json=json_data, timeout=5)
        elif method == 'PUT':
            response = requests.put(url, json=json_data, timeout=5)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=5)
        else:
            return jsonify({'error': 'Method not allowed'}), 405
        
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Service unavailable: {str(e)}'}), 503


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'gateway'}), 200


@app.route('/api/users', methods=['GET', 'POST'])
@app.route('/api/users/<path:user_path>', methods=['GET', 'PUT', 'DELETE'])
def users_proxy(user_path=None):
    """Proxy requests to User Service"""
    path = '/users' if user_path is None else f'/users/{user_path}'
    method = request.method
    
    json_data = None
    if method in ['POST', 'PUT']:
        json_data = request.get_json()
    
    return proxy_request(USER_SERVICE_URL, path, method, json_data=json_data)


@app.route('/api/products', methods=['GET', 'POST'])
@app.route('/api/products/<path:product_path>', methods=['GET', 'PUT', 'DELETE'])
def products_proxy(product_path=None):
    """Proxy requests to Product Service"""
    path = '/products' if product_path is None else f'/products/{product_path}'
    method = request.method
    
    json_data = None
    if method in ['POST', 'PUT']:
        json_data = request.get_json()
    
    return proxy_request(PRODUCT_SERVICE_URL, path, method, json_data=json_data)


@app.route('/api/orders', methods=['GET', 'POST'])
@app.route('/api/orders/<path:order_path>', methods=['GET'])
def orders_proxy(order_path=None):
    """Proxy requests to Order Service"""
    path = '/orders' if order_path is None else f'/orders/{order_path}'
    method = request.method
    
    json_data = None
    if method == 'POST':
        json_data = request.get_json()
    
    return proxy_request(ORDER_SERVICE_URL, path, method, json_data=json_data)


# gRPC Endpoints
@app.route('/api/grpc/users', methods=['GET'])
def grpc_get_users():
    """Get all users via gRPC"""
    try:
        users = user_grpc_client.get_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/grpc/users/<int:user_id>', methods=['GET'])
def grpc_get_user(user_id):
    """Get user by ID via gRPC"""
    try:
        user = user_grpc_client.get_user(user_id)
        if user:
            return jsonify(user), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/grpc/users', methods=['POST'])
def grpc_create_user():
    """Create user via gRPC"""
    try:
        data = request.get_json()
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({'error': 'Name and email are required'}), 400
        
        user = user_grpc_client.create_user(data['name'], data['email'])
        return jsonify(user), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/grpc/products', methods=['GET'])
def grpc_get_products():
    """Get all products via gRPC"""
    try:
        products = product_grpc_client.get_products()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/grpc/products/<int:product_id>', methods=['GET'])
def grpc_get_product(product_id):
    """Get product by ID via gRPC"""
    try:
        product = product_grpc_client.get_product(product_id)
        if product:
            return jsonify(product), 200
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/grpc/products', methods=['POST'])
def grpc_create_product():
    """Create product via gRPC"""
    try:
        data = request.get_json()
        if not data or not data.get('name') or data.get('price') is None:
            return jsonify({'error': 'Name and price are required'}), 400
        
        product = product_grpc_client.create_product(
            data['name'],
            float(data['price']),
            data.get('description', '')
        )
        return jsonify(product), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

