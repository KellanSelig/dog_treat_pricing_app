uv run python -m grpc_tools.protoc -Ibackend/protos --python_out=backend/code_gen --grpc_python_out=backend/code_gen --mypy_out=backend/code_gen backend/protos/grpc_service/v1/service.proto
