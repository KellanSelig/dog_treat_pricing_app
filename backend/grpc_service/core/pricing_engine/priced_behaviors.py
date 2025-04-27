from backend.grpc_service.core.models import Price
from backend.grpc_service.core.pricing_engine.priced_behavior_abc import PricedBehavior


class FreeBehavior(PricedBehavior):
    def get_price(self) -> Price:
        return Price(0, 0)


class EasyBehavior(PricedBehavior):
    def get_price(self) -> Price:
        return Price(5, 5)


class MediumBehavior(PricedBehavior):
    def get_price(self) -> Price:
        return Price(10, 10)


class HardBehavior(PricedBehavior):
    def get_price(self) -> Price:
        return Price(20, 20)
