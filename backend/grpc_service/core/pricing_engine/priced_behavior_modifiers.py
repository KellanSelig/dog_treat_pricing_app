from backend.grpc_service.core.models import Price
from backend.grpc_service.core.pricing_engine.priced_behavior_abc import PricedBehaviorModifier
from backend.grpc_service.core.pricing_engine.priced_behaviors import PricedBehavior


class UnknownLocationModifier(PricedBehaviorModifier):
    def get_price(self) -> Price:
        return self.base_behavior.get_price()

class InsideLocationModifier(PricedBehaviorModifier):
    def get_price(self) -> Price:
        return self.base_behavior.get_price() * 0.5


class OutsideLocationModifier(PricedBehaviorModifier):
    def get_price(self) -> Price:
        return self.base_behavior.get_price() * 2


class LotsOfDogsLocationModifier(PricedBehaviorModifier):
    def get_price(self) -> Price:
        return self.base_behavior.get_price() * 5


class DogParkLocationModifier(PricedBehaviorModifier):
    def get_price(self) -> Price:
        return self.base_behavior.get_price() * 6


class SquirrelsPresentLocationModifier(PricedBehaviorModifier):
    def get_price(self) -> Price:
        return self.base_behavior.get_price() * 10


class HomeLocationModifier(PricedBehaviorModifier):
    def get_price(self) -> Price:
        return self.base_behavior.get_price() * 0.1


class TastyTreatsLocationModifier(PricedBehaviorModifier):
    def get_price(self) -> Price:
        return self.base_behavior.get_price() * 2


class PetStoreLocationModifier(PricedBehaviorModifier):
    def get_price(self) -> Price:
        return self.base_behavior.get_price() * 3


class TirednessLevelModifier(PricedBehaviorModifier):
    def __init__(self, base_behavior: PricedBehavior, tiredness_level: float) -> None:
        super().__init__(base_behavior)
        self.tiredness_level = tiredness_level

    def get_price(self) -> Price:
        if self.tiredness_level < 0.5:
            return self.base_behavior.get_price() - 1
        if self.tiredness_level < 0.7:
            return self.base_behavior.get_price() - 0.5
        if self.tiredness_level < 0.9:
            return self.base_behavior.get_price() - 0.1
        return self.base_behavior.get_price() + 0.5


class HungerLevelModifier(PricedBehaviorModifier):
    def __init__(self, base_behavior: PricedBehavior, hunger_level: float) -> None:
        super().__init__(base_behavior)
        self.hunger_level = hunger_level

    def get_price(self) -> Price:
        if self.hunger_level < 0.5:
            return self.base_behavior.get_price() * Price(0.1, 3)
        if self.hunger_level < 0.7:
            return self.base_behavior.get_price() * Price(0.5, 2)
        if self.hunger_level < 0.9:
            return self.base_behavior.get_price() * Price(1, 0.5)
        return self.base_behavior.get_price() * Price(0.5, 0)


class BasicCutenessModifier(PricedBehaviorModifier):
    def get_price(self) -> Price:
        return self.base_behavior.get_price() * 0.5


class MediumCutenessModifier(PricedBehaviorModifier):
    def get_price(self) -> Price:
        return self.base_behavior.get_price() * 2


class ExtremeCutenessModifier(PricedBehaviorModifier):
    def get_price(self) -> Price:
        return self.base_behavior.get_price() * 2.5
