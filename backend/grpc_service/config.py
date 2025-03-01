from pydantic_settings import BaseSettings


class Config(BaseSettings):
    grpc_port: int = 50051
    service_name: str = "dog_trick_service"
    service_version: str = "v0.1.0"

config = Config()
