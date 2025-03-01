from dataclasses import dataclass
from enum import StrEnum
from enum import auto


class DogTrick(StrEnum):
    LAY_DOWN = auto()
    ROLL_OVER = auto()
    SIT = auto()
    SHAKE = auto()
    HIGH_FIVE = auto()
    GO_TO_BED = auto()
    STAY = auto()
    COME = auto()
    FETCH = auto()
    GO_TO_SPOT = auto()
    BUTTON = auto()
    LETS_GO = auto()
    THIS_WAY = auto()
    LEAVE_IT = auto()
    DROP_IT = auto()


class DogBehavior(StrEnum):
    WAGGING_TAIL = auto()
    PUPPY_EYES = auto()
    HEAD_TILT = auto()
    SNEEZE = auto()
    YAWN = auto()
    BARK = auto()
    PANT = auto()
    LICK = auto()
    JUMP = auto()
    SPIN = auto()
    SAD_PUPPY_EYES = auto()
    SLEEPY = auto()
    MAKE_BED = auto()
    CARRY_TOY = auto()
    CHOMP = auto()
    TUG_OF_WAR = auto()


class Location(StrEnum):
    INSIDE_LOCATION = auto()
    OUTSIDE_LOCATION = auto()
    LOTS_OF_DOGS_LOCATION = auto()
    DOG_PARK_LOCATION = auto()
    SQUIRRELS_PRESENT_LOCATION = auto()
    HOME_LOCATION = auto()
    TASTY_TREATS_LOCATION = auto()
    PET_STORE_LOCATION = auto()
    UNKNOWN_LOCATION = auto()


@dataclass(slots=True, frozen=True)
class PricingRequest:
    dog_name: str
    dog_treat_to_belly_rub_ratio: float
    tricks_to_perform: list[DogTrick]
    behaviors_to_perform: list[DogBehavior]
    location: Location


@dataclass(slots=True, frozen=True)
class PricingResult:
    pricing_id: str
    amount_dog_treat: float
    amount_belly_rub: float
