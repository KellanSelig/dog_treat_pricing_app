uv run python -m grpc_tools.protoc -Ibackend/protos --python_out=. --grpc_python_out=. --mypy_out=. backend/protos/grpc_service/v1/service.proto
