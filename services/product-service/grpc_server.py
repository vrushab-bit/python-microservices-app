from concurrent import futures
import grpc
import os
import sys
from datetime import datetime

# Add proto path
sys.path.append('/app/proto')
sys.path.append('/app')

from proto import product_pb2, product_pb2_grpc
from app import app, db, Product


class ProductServiceServicer(product_pb2_grpc.ProductServiceServicer):
    """gRPC server implementation for Product Service"""
    
    def GetProduct(self, request, context):
        """Get a single product by ID"""
        try:
            with app.app_context():
                product = Product.query.get(request.product_id)
                if not product:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f'Product with id {request.product_id} not found')
                    return product_pb2.ProductResponse()
                
                return product_pb2.ProductResponse(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    description=product.description or '',
                    created_at=product.created_at.isoformat() if product.created_at else ''
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return product_pb2.ProductResponse()
    
    def GetProducts(self, request, context):
        """Get all products"""
        try:
            with app.app_context():
                products = Product.query.all()
                product_responses = [
                    product_pb2.ProductResponse(
                        id=product.id,
                        name=product.name,
                        price=product.price,
                        description=product.description or '',
                        created_at=product.created_at.isoformat() if product.created_at else ''
                    )
                    for product in products
                ]
                return product_pb2.ProductsResponse(products=product_responses)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return product_pb2.ProductsResponse()
    
    def CreateProduct(self, request, context):
        """Create a new product"""
        try:
            with app.app_context():
                if request.price < 0:
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    context.set_details('Price must be non-negative')
                    return product_pb2.ProductResponse()
                
                product = Product(
                    name=request.name,
                    price=request.price,
                    description=request.description or ''
                )
                db.session.add(product)
                db.session.commit()
                
                return product_pb2.ProductResponse(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    description=product.description or '',
                    created_at=product.created_at.isoformat() if product.created_at else ''
                )
        except Exception as e:
            db.session.rollback()
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return product_pb2.ProductResponse()
    
    def UpdateProduct(self, request, context):
        """Update a product"""
        try:
            with app.app_context():
                product = Product.query.get(request.product_id)
                if not product:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f'Product with id {request.product_id} not found')
                    return product_pb2.ProductResponse()
                
                if request.name:
                    product.name = request.name
                if request.price >= 0:
                    product.price = request.price
                if request.description:
                    product.description = request.description
                
                db.session.commit()
                
                return product_pb2.ProductResponse(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    description=product.description or '',
                    created_at=product.created_at.isoformat() if product.created_at else ''
                )
        except Exception as e:
            db.session.rollback()
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return product_pb2.ProductResponse()
    
    def DeleteProduct(self, request, context):
        """Delete a product"""
        try:
            with app.app_context():
                product = Product.query.get(request.product_id)
                if not product:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f'Product with id {request.product_id} not found')
                    return product_pb2.DeleteProductResponse(success=False, message='Product not found')
                
                db.session.delete(product)
                db.session.commit()
                
                return product_pb2.DeleteProductResponse(success=True, message='Product deleted successfully')
        except Exception as e:
            db.session.rollback()
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return product_pb2.DeleteProductResponse(success=False, message=str(e))


def serve():
    """Start the gRPC server"""
    port = os.getenv('GRPC_PORT', '50052')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductServiceServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f'gRPC Product Service server started on port {port}')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

