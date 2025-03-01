from abc import ABC
from abc import abstractmethod
from typing import override

from backend.grpc_service.core.models import PricingRequest
from backend.grpc_service.core.models import PricingResult
from backend.grpc_service.core.ports.repositories.cuteness_rating_repository import ICutenessRatingRepository
from backend.grpc_service.core.ports.repositories.difficulty_rating_repository import IDifficultyRatingRepository
from backend.grpc_service.core.ports.repositories.priced_dog_treat_repository import IPricedDogTreatRepository
from backend.grpc_service.core.pricing_engine.pricing_engine import calculate_price
from backend.grpc_service.log import log


class IDogTreatServerCore(ABC):
    def __init__(
        self,
        difficulty_rating_repository: IDifficultyRatingRepository,
        cuteness_rating_repository: ICutenessRatingRepository,
        priced_dog_treat_repository: IPricedDogTreatRepository,
    ):
        self.difficulty_rating_repository = difficulty_rating_repository
        self.cuteness_rating_repository = cuteness_rating_repository
        self.priced_dog_treat_repository = priced_dog_treat_repository

    @abstractmethod
    def perform_dog_trick(self) -> None: ...

    @abstractmethod
    def price_dog_tricks(self, request: PricingRequest) -> PricingResult: ...


class DogTreatServerCoreV1(IDogTreatServerCore):
    @override
    def perform_dog_trick(self) -> None:
        # TODO: Use a local LLM to generate the text.
        pass

    @override
    def price_dog_tricks(self, request: PricingRequest) -> PricingResult:
        price = calculate_price(request, self.difficulty_rating_repository, self.cuteness_rating_repository)
        pricing_result = self.priced_dog_treat_repository.save_new_pricing_result(price)
        log.info("Pricing result saved: %s", pricing_result)
        return pricing_result
