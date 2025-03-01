from abc import ABC
from abc import abstractmethod
from collections.abc import Sequence

from backend.grpc_service.core.models import DogTrick


class IDifficultyRatingRepository(ABC):
    @abstractmethod
    def get_difficulty_ratings(self, tricks: Sequence[DogTrick]) -> list[float]:
        """Get the difficulty rating for a dog by its ID."""

    @abstractmethod
    def set_difficulty_rating(self, trick: DogTrick, rating: float) -> None:
        """Set the difficulty rating for a dog by its ID."""
