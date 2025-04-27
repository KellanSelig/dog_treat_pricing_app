import logging
from datetime import UTC
from datetime import datetime
from typing import override
from uuid import UUID
from uuid import uuid4

from backend.grpc_service.adapters.repositories.priced_dog_treat_repository.converters import (
    convert_priced_trick_to_pricing_result,
)
from backend.grpc_service.adapters.repositories.priced_dog_treat_repository.models import PricedTrick
from backend.grpc_service.adapters.repositories.priced_dog_treat_repository.models import Status
from backend.grpc_service.core.models import Price
from backend.grpc_service.core.models import PricingResult
from backend.grpc_service.core.ports.repositories.priced_dog_treat_repository import IPricedDogTreatRepository
from backend.grpc_service.log import log

ONE_HOUR_SECONDS = 60 * 60 * 60

logger = logging.getLogger(__name__)
class MemoryPricedDogTreatRepository(IPricedDogTreatRepository):
    def __init__(self):
        self._pricing_results: dict[UUID, PricedTrick] = {}

    @override
    def save_new_pricing_result(self, price: Price) -> PricingResult:
        current_dt = datetime.now(UTC)
        pricing_id = uuid4()
        record = PricedTrick(
            id=pricing_id,
            amount_dog_treat=price.amount_dog_treat,
            amount_belly_rub=price.amount_belly_rub,
            created_at=current_dt,
            updated_at=current_dt,
            current_status=Status.NEW,
        )
        logger.info("pricing_results: %s", self._pricing_results)
        return convert_priced_trick_to_pricing_result(self._pricing_results.setdefault(pricing_id, record))

    @override
    def fetch_pricing_result(self, pricing_id: str, status_filter: set[Status] | None = None) -> PricingResult | None:
        try:
            priced_trick = self._pricing_results[UUID(pricing_id)]
            if status_filter and priced_trick.current_status not in status_filter:
                log.info(
                    "Pricing result with ID %s has status %s, which is not in the filter.",
                    pricing_id,
                    priced_trick.current_status,
                )
                return None
            return convert_priced_trick_to_pricing_result(self._pricing_results[UUID(pricing_id)])
        except KeyError:
            log.info("Pricing result with ID %s not found.", pricing_id)

    @override
    def set_pricing_result_status(self, pricing_id: str, new_status: Status) -> None:
        try:
            priced_trick = self._pricing_results[UUID(pricing_id)]
            priced_trick.current_status = new_status
        except KeyError:
            msg = f"Pricing result with ID {pricing_id} not found."
            raise KeyError(msg) from None
