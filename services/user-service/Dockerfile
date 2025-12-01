FROM python:3.11-slim

WORKDIR /app

COPY services/user-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy proto files (from project root)
COPY proto /app/proto

# Compile proto files
RUN python -m grpc_tools.protoc -I /app/proto --python_out=/app/proto --grpc_python_out=/app/proto /app/proto/user.proto

COPY services/user-service/init_db.py .
COPY services/user-service/app.py .
COPY services/user-service/grpc_server.py .
COPY services/user-service/start.sh .

RUN chmod +x start.sh

EXPOSE 5001 50051

CMD ["./start.sh"]

