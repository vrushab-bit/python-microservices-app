FROM python:3.11-slim

WORKDIR /app

COPY services/order-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy proto files (from project root)
COPY proto /app/proto

# Compile proto files
RUN python -m grpc_tools.protoc -I /app/proto --python_out=/app/proto --grpc_python_out=/app/proto /app/proto/user.proto /app/proto/product.proto

COPY services/order-service/init_db.py .
COPY services/order-service/app.py .
COPY services/order-service/grpc_client.py .

EXPOSE 5003

CMD ["python", "app.py"]

