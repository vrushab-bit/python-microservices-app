#!/bin/bash

# Start Flask app in background
python app.py &
FLASK_PID=$!

# Start gRPC server in background
python grpc_server.py &
GRPC_PID=$!

# Function to handle shutdown
cleanup() {
    echo "Shutting down services..."
    kill $FLASK_PID $GRPC_PID 2>/dev/null
    exit 0
}

# Trap SIGTERM and SIGINT
trap cleanup SIGTERM SIGINT

# Wait for both processes
wait $FLASK_PID $GRPC_PID

