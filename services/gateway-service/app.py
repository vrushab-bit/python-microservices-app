from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Service URLs (using Docker service names)
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user-service:5001')
PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://product-service:5002')
ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://order-service:5003')


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

