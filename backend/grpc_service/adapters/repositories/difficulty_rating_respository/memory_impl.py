from collections.abc import Sequence
from typing import ClassVar
from typing import override

from backend.grpc_service.core.models import DogTrick
from backend.grpc_service.core.ports.repositories.difficulty_rating_repository import IDifficultyRatingRepository
from backend.grpc_service.log import log


class MemoryDifficultyRatingRepository(IDifficultyRatingRepository):
    _difficulty_lookup: ClassVar[dict[DogTrick , float]] = {
        DogTrick.LAY_DOWN: 1,
        DogTrick.ROLL_OVER: 2,
        DogTrick.SIT: 1,
        DogTrick.SHAKE: 1,
        DogTrick.HIGH_FIVE: 2,
        DogTrick.GO_TO_BED: 2,
        DogTrick.STAY: 7,
        DogTrick.COME: 5,
        DogTrick.FETCH: 3,
        DogTrick.GO_TO_SPOT: 1,
        DogTrick.BUTTON: 6,
        DogTrick.LETS_GO: 2,
        DogTrick.THIS_WAY: 2,
        DogTrick.LEAVE_IT: 10,
        DogTrick.DROP_IT: 15,
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
