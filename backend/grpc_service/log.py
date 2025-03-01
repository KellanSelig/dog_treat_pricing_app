import logging

from backend.logging_config import setup_logging

setup_logging()
log = logging.getLogger("grpc_service")
