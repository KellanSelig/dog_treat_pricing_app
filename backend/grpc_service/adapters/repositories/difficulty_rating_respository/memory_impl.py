from collections.abc import Sequence
from typing import ClassVar
from typing import override

from backend.grpc_service.core.models import DogTrick
from backend.grpc_service.core.ports.repositories.difficulty_rating_repository import IDifficultyRatingRepository
from backend.grpc_service.log import log


class MemoryDifficultyRatingRepository(IDifficultyRatingRepository):
    _difficulty_lookup: ClassVar[dict[DogTrick , float]] = {
        DogTrick.LAY_DOWN: 1,
        DogTrick.ROLL_OVER: 1,
        DogTrick.SIT: 1,
        DogTrick.SHAKE: 1,
        DogTrick.HIGH_FIVE: 1,
        DogTrick.GO_TO_BED: 1,
        DogTrick.STAY: 1,
        DogTrick.COME: 1,
        DogTrick.FETCH: 1,
        DogTrick.GO_TO_SPOT: 1,
        DogTrick.BUTTON: 1,
        DogTrick.LETS_GO: 1,
        DogTrick.THIS_WAY: 1,
        DogTrick.LEAVE_IT: 1,
        DogTrick.DROP_IT: 1,
    }

    @override
    def get_difficulty_ratings(self, tricks: Sequence[DogTrick]) -> list[float]:
        behavior_lookups: list[float] = []
        for trick in tricks:
            try:
                behavior_lookups.append(MemoryDifficultyRatingRepository._difficulty_lookup[trick])
            except KeyError:
                log.error("Unknown dog behavior: %s", trick)
        return behavior_lookups

    @override
    def set_difficulty_rating(self, trick: DogTrick, rating: float) -> None:
        MemoryDifficultyRatingRepository._difficulty_lookup[trick] = rating
