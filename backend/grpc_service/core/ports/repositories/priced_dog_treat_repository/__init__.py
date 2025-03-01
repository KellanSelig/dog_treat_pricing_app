from abc import ABC
from abc import abstractmethod

from backend.grpc_service.core.models import Price
from backend.grpc_service.core.models import PricingResult
from backend.grpc_service.core.models.perform_dog_trick_models import Status


class IPricedDogTreatRepository(ABC):
    @abstractmethod
    def save_new_pricing_result(self, price: Price) -> PricingResult:
        """Get the price of a dog treat by its ID."""

    @abstractmethod
    def fetch_pricing_result(self, pricing_id: str, status_filter: set[Status] | None = None) -> PricingResult | None:
        """Set the price of a dog treat by its ID."""

    @abstractmethod
    def set_pricing_result_status(self, pricing_id: str, new_status: Status) -> None:
        """Set the price of a dog treat by its ID."""
