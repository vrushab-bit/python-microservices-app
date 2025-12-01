from concurrent import futures
import grpc
import os
import sys
from datetime import datetime

# Add proto path
sys.path.append('/app/proto')
sys.path.append('/app')

from proto import user_pb2, user_pb2_grpc
from app import app, db, User


class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    """gRPC server implementation for User Service"""
    
    def GetUser(self, request, context):
        """Get a single user by ID"""
        try:
            with app.app_context():
                user = User.query.get(request.user_id)
                if not user:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f'User with id {request.user_id} not found')
                    return user_pb2.UserResponse()
                
                return user_pb2.UserResponse(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    created_at=user.created_at.isoformat() if user.created_at else ''
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.UserResponse()
    
    def GetUsers(self, request, context):
        """Get all users"""
        try:
            with app.app_context():
                users = User.query.all()
                user_responses = [
                    user_pb2.UserResponse(
                        id=user.id,
                        name=user.name,
                        email=user.email,
                        created_at=user.created_at.isoformat() if user.created_at else ''
                    )
                    for user in users
                ]
                return user_pb2.UsersResponse(users=user_responses)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.UsersResponse()
    
    def CreateUser(self, request, context):
        """Create a new user"""
        try:
            with app.app_context():
                # Check if email already exists
                existing_user = User.query.filter_by(email=request.email).first()
                if existing_user:
                    context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                    context.set_details('Email already exists')
                    return user_pb2.UserResponse()
                
                user = User(
                    name=request.name,
                    email=request.email
                )
                db.session.add(user)
                db.session.commit()
                
                return user_pb2.UserResponse(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    created_at=user.created_at.isoformat() if user.created_at else ''
                )
        except Exception as e:
            db.session.rollback()
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.UserResponse()
    
    def UpdateUser(self, request, context):
        """Update a user"""
        try:
            with app.app_context():
                user = User.query.get(request.user_id)
                if not user:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f'User with id {request.user_id} not found')
                    return user_pb2.UserResponse()
                
                if request.name:
                    user.name = request.name
                if request.email:
                    # Check if email exists for another user
                    existing_user = User.query.filter_by(email=request.email).first()
                    if existing_user and existing_user.id != request.user_id:
                        context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                        context.set_details('Email already exists')
                        return user_pb2.UserResponse()
                    user.email = request.email
                
                db.session.commit()
                
                return user_pb2.UserResponse(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    created_at=user.created_at.isoformat() if user.created_at else ''
                )
        except Exception as e:
            db.session.rollback()
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.UserResponse()
    
    def DeleteUser(self, request, context):
        """Delete a user"""
        try:
            with app.app_context():
                user = User.query.get(request.user_id)
                if not user:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f'User with id {request.user_id} not found')
                    return user_pb2.DeleteUserResponse(success=False, message='User not found')
                
                db.session.delete(user)
                db.session.commit()
                
                return user_pb2.DeleteUserResponse(success=True, message='User deleted successfully')
        except Exception as e:
            db.session.rollback()
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.DeleteUserResponse(success=False, message=str(e))


def serve():
    """Start the gRPC server"""
    port = os.getenv('GRPC_PORT', '50051')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f'gRPC User Service server started on port {port}')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

