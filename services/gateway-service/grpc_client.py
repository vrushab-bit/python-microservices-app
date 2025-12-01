import grpc
import os
import sys

# Add proto path
sys.path.append('/app/proto')

from proto import user_pb2, user_pb2_grpc
from proto import product_pb2, product_pb2_grpc


class UserServiceClient:
    """gRPC client for User Service"""
    
    def __init__(self, host='user-service', port='50051'):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = user_pb2_grpc.UserServiceStub(self.channel)
    
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            request = user_pb2.GetUserRequest(user_id=user_id)
            response = self.stub.GetUser(request, timeout=5)
            return {
                'id': response.id,
                'name': response.name,
                'email': response.email,
                'created_at': response.created_at
            }
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise Exception(f'gRPC error: {e.details()}')
    
    def get_users(self):
        """Get all users"""
        try:
            request = user_pb2.GetUsersRequest()
            response = self.stub.GetUsers(request, timeout=5)
            return [
                {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'created_at': user.created_at
                }
                for user in response.users
            ]
        except grpc.RpcError as e:
            raise Exception(f'gRPC error: {e.details()}')
    
    def create_user(self, name, email):
        """Create a new user"""
        try:
            request = user_pb2.CreateUserRequest(name=name, email=email)
            response = self.stub.CreateUser(request, timeout=5)
            return {
                'id': response.id,
                'name': response.name,
                'email': response.email,
                'created_at': response.created_at
            }
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                raise Exception('Email already exists')
            raise Exception(f'gRPC error: {e.details()}')
    
    def close(self):
        """Close the channel"""
        self.channel.close()


class ProductServiceClient:
    """gRPC client for Product Service"""
    
    def __init__(self, host='product-service', port='50052'):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = product_pb2_grpc.ProductServiceStub(self.channel)
    
    def get_product(self, product_id):
        """Get product by ID"""
        try:
            request = product_pb2.GetProductRequest(product_id=product_id)
            response = self.stub.GetProduct(request, timeout=5)
            return {
                'id': response.id,
                'name': response.name,
                'price': response.price,
                'description': response.description,
                'created_at': response.created_at
            }
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise Exception(f'gRPC error: {e.details()}')
    
    def get_products(self):
        """Get all products"""
        try:
            request = product_pb2.GetProductsRequest()
            response = self.stub.GetProducts(request, timeout=5)
            return [
                {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'description': product.description,
                    'created_at': product.created_at
                }
                for product in response.products
            ]
        except grpc.RpcError as e:
            raise Exception(f'gRPC error: {e.details()}')
    
    def create_product(self, name, price, description=''):
        """Create a new product"""
        try:
            request = product_pb2.CreateProductRequest(
                name=name,
                price=price,
                description=description
            )
            response = self.stub.CreateProduct(request, timeout=5)
            return {
                'id': response.id,
                'name': response.name,
                'price': response.price,
                'description': response.description,
                'created_at': response.created_at
            }
        except grpc.RpcError as e:
            raise Exception(f'gRPC error: {e.details()}')
    
    def close(self):
        """Close the channel"""
        self.channel.close()

