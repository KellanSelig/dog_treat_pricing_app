from backend.grpc_service.adapters.repositories.priced_dog_treat_repository.models import PricedTrick
from backend.grpc_service.core.models import PricingResult


def convert_priced_trick_to_pricing_result(
    priced_trick: PricedTrick,
) -> PricingResult:
    """Convert a PricedTrick object to a PricingResult object."""
    return PricingResult(
        pricing_id=str(priced_trick.id),
        amount_dog_treat=priced_trick.amount_dog_treat,
        amount_belly_rub=priced_trick.amount_belly_rub,
    )
