from collections.abc import Sequence
from datetime import UTC
from datetime import datetime

from backend.grpc_service.core.models import DogBehavior
from backend.grpc_service.core.models import DogTrick
from backend.grpc_service.core.models import Location
from backend.grpc_service.core.models import Price
from backend.grpc_service.core.models import PricingRequest
from backend.grpc_service.core.ports.repositories.cuteness_rating_repository import ICutenessRatingRepository
from backend.grpc_service.core.ports.repositories.difficulty_rating_repository import IDifficultyRatingRepository
from backend.grpc_service.core.pricing_engine.priced_behavior_abc import PricedBehavior
from backend.grpc_service.core.pricing_engine.priced_behavior_abc import PricedBehaviorModifier
from backend.grpc_service.core.pricing_engine.priced_behavior_modifiers import BasicCutenessModifier
from backend.grpc_service.core.pricing_engine.priced_behavior_modifiers import DogParkLocationModifier
from backend.grpc_service.core.pricing_engine.priced_behavior_modifiers import ExtremeCutenessModifier
from backend.grpc_service.core.pricing_engine.priced_behavior_modifiers import HomeLocationModifier
from backend.grpc_service.core.pricing_engine.priced_behavior_modifiers import InsideLocationModifier
from backend.grpc_service.core.pricing_engine.priced_behavior_modifiers import LotsOfDogsLocationModifier
from backend.grpc_service.core.pricing_engine.priced_behavior_modifiers import MediumCutenessModifier
from backend.grpc_service.core.pricing_engine.priced_behavior_modifiers import OutsideLocationModifier
from backend.grpc_service.core.pricing_engine.priced_behavior_modifiers import PetStoreLocationModifier
from backend.grpc_service.core.pricing_engine.priced_behavior_modifiers import SquirrelsPresentLocationModifier
from backend.grpc_service.core.pricing_engine.priced_behavior_modifiers import TastyTreatsLocationModifier
from backend.grpc_service.core.pricing_engine.priced_behavior_modifiers import TirednessLevelModifier
from backend.grpc_service.core.pricing_engine.priced_behavior_modifiers import UnknownLocationModifier
from backend.grpc_service.core.pricing_engine.priced_behaviors import EasyBehavior
from backend.grpc_service.core.pricing_engine.priced_behaviors import FreeBehavior
from backend.grpc_service.core.pricing_engine.priced_behaviors import HardBehavior
from backend.grpc_service.core.pricing_engine.priced_behaviors import MediumBehavior

cuteness_lookup: dict[DogBehavior, int] = {}


def get_trick_difficulty(tricks: Sequence[DogTrick], repository: IDifficultyRatingRepository) -> PricedBehavior:
    total_difficulty = sum(repository.get_difficulty_ratings(tricks))
    if total_difficulty == 0:
        return FreeBehavior()
    if total_difficulty < 5:
        return EasyBehavior()
    if total_difficulty < 10:
        return MediumBehavior()
    return HardBehavior()


def apply_total_cuteness_modifier(
    base_behavior: PricedBehavior, behaviors: Sequence[DogBehavior], repository: ICutenessRatingRepository
) -> PricedBehavior:
    """
    sum all cutenesses and then depending on total return correct modifier
    """
    total_cuteness_score = sum(repository.get_cuteness_ratings(behaviors))
    if total_cuteness_score == 0:
        return base_behavior
    if total_cuteness_score < 5:
        return BasicCutenessModifier(base_behavior)
    if total_cuteness_score < 10:
        return MediumCutenessModifier(base_behavior)
    return ExtremeCutenessModifier(base_behavior)


def apply_location_modifier(base_behavior: PricedBehavior, location: Location) -> PricedBehaviorModifier:
    location_lookup: dict[Location, type[PricedBehaviorModifier]] = {
        Location.INSIDE_LOCATION: InsideLocationModifier,
        Location.OUTSIDE_LOCATION: OutsideLocationModifier,
        Location.LOTS_OF_DOGS_LOCATION: LotsOfDogsLocationModifier,
        Location.DOG_PARK_LOCATION: DogParkLocationModifier,
        Location.SQUIRRELS_PRESENT_LOCATION: SquirrelsPresentLocationModifier,
        Location.HOME_LOCATION: HomeLocationModifier,
        Location.TASTY_TREATS_LOCATION: TastyTreatsLocationModifier,
        Location.PET_STORE_LOCATION: PetStoreLocationModifier,
    }
    return location_lookup.get(location, UnknownLocationModifier)(base_behavior)


def apply_time_of_day_modifier(base_behavior: PricedBehavior) -> PricedBehavior:
    current_time = datetime.now(UTC)

    # TODO - clean up this logic a bit. Just placeholder for now
    if 22 < current_time.hour < 8:
        tiredness_level = 1
    elif 8 <= current_time.hour < 10:
        tiredness_level = 0
    elif 10 <= current_time.hour < 12:
        tiredness_level = 0.3
    elif 12 <= current_time.hour < 14:
        tiredness_level = 0.5
    elif 14 <= current_time.hour < 16:
        tiredness_level = 0.7
    elif 16 <= current_time.hour < 18:
        tiredness_level = 0.8
    elif 18 <= current_time.hour < 20:
        tiredness_level = 0.6
    elif 20 <= current_time.hour < 22:
        tiredness_level = 0.4
    else:
        tiredness_level = 0.5
    return TirednessLevelModifier(base_behavior, tiredness_level)


def calculate_price(
    pricing_request: PricingRequest,
    difficulty_repository: IDifficultyRatingRepository,
    cuteness_repository: ICutenessRatingRepository,
) -> Price:
    priced_behavior = get_trick_difficulty(pricing_request.tricks_to_perform, difficulty_repository)
    priced_behavior = apply_location_modifier(priced_behavior, pricing_request.location)
    priced_behavior = apply_time_of_day_modifier(priced_behavior)
    priced_behavior = apply_total_cuteness_modifier(
        priced_behavior, pricing_request.behaviors_to_perform, cuteness_repository
    )
    subtotal = priced_behavior.get_price()
    # TODO - Check math
    return Price(
        subtotal.amount_dog_treat * pricing_request.dog_treat_to_belly_rub_ratio,
        subtotal.amount_belly_rub * (1 - pricing_request.dog_treat_to_belly_rub_ratio),
    )
