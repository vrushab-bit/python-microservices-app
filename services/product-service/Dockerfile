FROM python:3.11-slim

WORKDIR /app

COPY services/product-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy proto files (from project root)
COPY proto /app/proto

# Compile proto files
RUN python -m grpc_tools.protoc -I /app/proto --python_out=/app/proto --grpc_python_out=/app/proto /app/proto/product.proto

COPY services/product-service/init_db.py .
COPY services/product-service/app.py .
COPY services/product-service/grpc_server.py .
COPY services/product-service/start.sh .

RUN chmod +x start.sh

EXPOSE 5002 50052

CMD ["./start.sh"]

