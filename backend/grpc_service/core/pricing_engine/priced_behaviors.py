from backend.grpc_service.core.models import Price
from backend.grpc_service.core.pricing_engine.priced_behavior_abc import PricedBehavior


class FreeBehavior(PricedBehavior):
    def get_price(self) -> Price:
        return Price(0, 0)


class EasyBehavior(PricedBehavior):
    def get_price(self) -> Price:
        return Price(1, 1)


class MediumBehavior(PricedBehavior):
    def get_price(self) -> Price:
        return Price(2, 2)


class HardBehavior(PricedBehavior):
    def get_price(self) -> Price:
        return Price(3, 3)
