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
    
    def close(self):
        """Close the channel"""
        self.channel.close()

