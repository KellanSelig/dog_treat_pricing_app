from collections.abc import Sequence
from typing import ClassVar
from typing import override

from backend.grpc_service.core.models import DogBehavior
from backend.grpc_service.core.models import DogTrick
from backend.grpc_service.core.ports.repositories.cuteness_rating_repository import ICutenessRatingRepository
from backend.grpc_service.log import log


class MemoryCutenessRatingRepository(ICutenessRatingRepository):
    _cuteness_lookup: ClassVar[dict[DogBehavior | DogTrick, float]] = {
        DogTrick.LAY_DOWN: 1,
        DogTrick.ROLL_OVER: 2,
        DogTrick.SIT: 1,
        DogTrick.SHAKE: 2,
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
        DogBehavior.WAGGING_TAIL: 1,
        DogBehavior.PUPPY_EYES: 3,
        DogBehavior.HEAD_TILT: 2,
        DogBehavior.SNEEZE: 1,
        DogBehavior.YAWN: 1,
        DogBehavior.BARK: 1,
        DogBehavior.PANT: 1,
        DogBehavior.LICK: 1,
        DogBehavior.JUMP: 1,
        DogBehavior.SPIN: 2,
        DogBehavior.SAD_PUPPY_EYES: 1,
        DogBehavior.SLEEPY: 1,
        DogBehavior.MAKE_BED: 2,
        DogBehavior.CARRY_TOY: 3,
        DogBehavior.CHOMP: 2,
        DogBehavior.TUG_OF_WAR: 2,
    }

    @override
    def get_cuteness_ratings(self, behaviors: Sequence[DogBehavior | DogTrick]) -> list[float]:
        behavior_lookups: list[float] = []
        for behavior in behaviors:
            try:
                behavior_lookups.append(MemoryCutenessRatingRepository._cuteness_lookup[behavior])
            except KeyError:
                log.error("Unknown dog behavior: %s", behavior)
        return behavior_lookups

    @override
    def set_cuteness_rating(self, behavior: DogBehavior | DogTrick, rating: float) -> None:
        MemoryCutenessRatingRepository._cuteness_lookup[behavior] = rating
