from uuid import UUID

from backend.code_gen.grpc_service.v1.service_pb2 import GetDogTreatPriceRequest
from backend.code_gen.grpc_service.v1.service_pb2 import PerformDogTrickRequest
from backend.grpc_service.errors import InvalidDogName
from backend.grpc_service.errors import InvalidPricingID
from backend.grpc_service.errors import PerformDogTrickRequestExceptionGroup


def validate_dog_trick_price_request(request: GetDogTreatPriceRequest) -> None:
    # ... fancy validation logic here
    pass


def validate_perform_dog_trick_request(request: PerformDogTrickRequest) -> None:
    errors: list[tuple[type[Exception], str]] = []
    if not PerformDogTrickRequest.dog_name:
        errors.append(
            (
                InvalidDogName,
                f"A Dog name is required. Recieved: `{request.dog_name}`",
            )
        )
    try:
        UUID(request.pricing_id)
    except ValueError:
        errors.append((InvalidPricingID, f"Invalid pricing ID: {request.pricing_id}. Must be a valid UUID"))

    if errors:
        msg = "Encountered error(s) while parsing `PerformDogTrickRequest`"
        raise PerformDogTrickRequestExceptionGroup(msg, [i[0](i[1]) for i in errors])
