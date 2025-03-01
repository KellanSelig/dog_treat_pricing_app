from collections.abc import Iterator
from typing import override

import grpc
from google.protobuf import empty_pb2

from backend.code_gen.grpc_service.v1.service_pb2 import GetDogTreatPriceRequest
from backend.code_gen.grpc_service.v1.service_pb2 import GetDogTreatPriceResponse
from backend.code_gen.grpc_service.v1.service_pb2 import HealthCheckResponse
from backend.code_gen.grpc_service.v1.service_pb2 import PerformDogTrickRequest
from backend.code_gen.grpc_service.v1.service_pb2 import PerformDogTrickResponse
from backend.code_gen.grpc_service.v1.service_pb2 import Status
from backend.code_gen.grpc_service.v1.service_pb2_grpc import DogTrickServiceServicer
from backend.grpc_service.config import config
from backend.grpc_service.core.services import IDogTreatServerCore
from backend.grpc_service.errors import PerformDogTrickRequestExceptionGroup
from backend.grpc_service.log import log
from backend.grpc_service.server.api.converters import convert_core_get_dog_treat_price_response_to_pb2
from backend.grpc_service.server.api.converters import convert_pb2_get_dog_treat_price_request_to_core
from backend.grpc_service.server.api.validators import validate_dog_trick_price_request
from backend.grpc_service.server.api.validators import validate_perform_dog_trick_request


class DogTrickServicer(DogTrickServiceServicer):
    def __init__(self, core_service: IDogTreatServerCore) -> None:
        self.core_service = core_service

    @override
    def GetDogTreatPrice(
        self, request: GetDogTreatPriceRequest, context: grpc.ServicerContext
    ) -> GetDogTreatPriceResponse:
        validate_dog_trick_price_request(request)  # always success because well, time
        pricing_result = self.core_service.price_dog_tricks(convert_pb2_get_dog_treat_price_request_to_core(request))
        return convert_core_get_dog_treat_price_response_to_pb2(pricing_result)

    @override
    def PerformDogTrick(
        self, request: PerformDogTrickRequest, context: grpc.ServicerContext
    ) -> Iterator[PerformDogTrickResponse]:
        try:
            validate_perform_dog_trick_request(request)
        except PerformDogTrickRequestExceptionGroup as error:
            log.info("Validation errors: %s", error)
            yield PerformDogTrickResponse(status=Status.STATUS_ERROR, error_message=str(error))
            return
        raise NotImplementedError("Method not implemented!")

    @override
    def HeathCheck(self, request: empty_pb2.Empty, context: grpc.ServicerContext) -> HealthCheckResponse:
        log.info("Health check request received")
        log.info("Context: %s", context)
        return HealthCheckResponse(service_name=config.service_name, version=config.service_version)
