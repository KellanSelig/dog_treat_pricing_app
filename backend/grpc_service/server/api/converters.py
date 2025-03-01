from backend.code_gen.grpc_service.v1 import service_pb2 as pb2
from backend.grpc_service.core.models import DogBehavior
from backend.grpc_service.core.models import DogTrick
from backend.grpc_service.core.models import Location
from backend.grpc_service.core.models import PricingRequest
from backend.grpc_service.core.models import PricingResult


def convert_pb2_get_dog_treat_price_request_to_core(request: pb2.GetDogTreatPriceRequest) -> PricingRequest:
    """Convert the protobuf request to a domain model."""
    return PricingRequest(
        dog_name=request.dog_name,
        dog_treat_to_belly_rub_ratio=request.dog_treat_to_belly_rub_ratio,
        tricks_to_perform=[DogTrick(pb2.DogTrick.Name(t).replace("DOG_TRICK_", "")) for t in request.tricks_to_perform],
        behaviors_to_perform=[
            DogBehavior(pb2.DogBehavior.Name(b).replace("DOG_BEHAVIOR_", "")) for b in request.cutes_to_include
        ],
        location=Location(request.location),
    )


def convert_core_get_dog_treat_price_response_to_pb2(
    result: PricingResult, request: pb2.GetDogTreatPriceRequest
) -> pb2.GetDogTreatPriceResponse:
    """Convert the domain model to a protobuf request."""
    return pb2.GetDogTreatPriceResponse(
        pricing_result=pb2.PricingResult(
            pricing_id=result.pricing_id,
            dog_treat_price=result.amount_dog_treat,
            belly_rub_price=result.amount_belly_rub,
            request=request,
        ),
        status=pb2.Status.STATUS_SUCCESS,
    )
