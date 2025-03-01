from abc import ABC
from abc import abstractmethod
from collections.abc import Sequence

from backend.grpc_service.core.models import DogBehavior
from backend.grpc_service.core.models import DogTrick


class ICutenessRatingRepository(ABC):
    @abstractmethod
    def get_cuteness_ratings(self, behaviors: Sequence[DogBehavior | DogTrick]) -> list[float]:
        """Get the cuteness rating for a dog by its ID."""

    @abstractmethod
    def set_cuteness_rating(self, behavior: DogBehavior, rating: float) -> None:
        """Set the cuteness rating for a dog by its ID."""
