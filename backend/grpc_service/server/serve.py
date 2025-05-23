from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from backend.grpc_service.config import config
from backend.grpc_service.core.services import IDogTreatServerCore
from backend.grpc_service.log import log
from backend.grpc_service.server.api.dog_trick_server import DogTrickServicer
from grpc_service.v1 import service_pb2
from grpc_service.v1.service_pb2_grpc import add_DogTrickServiceServicer_to_server


def serve(core_service: IDogTreatServerCore) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = DogTrickServicer(core_service)
    log.info("Starting server: %s", config)
    add_DogTrickServiceServicer_to_server(servicer, server)
    service_names = (
        service_pb2.DESCRIPTOR.services_by_name["DogTrickService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)
    server.add_insecure_port(f"[::]:{config.grpc_port}")
    log.info("Server started on port: %s", config.grpc_port)
    server.start()
    server.wait_for_termination()
