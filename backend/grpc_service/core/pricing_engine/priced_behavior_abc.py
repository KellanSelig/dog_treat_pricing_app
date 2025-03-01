from abc import ABC
from abc import abstractmethod

from backend.grpc_service.core.models import Price


class PricedBehavior(ABC):
    @abstractmethod
    def get_price(self) -> Price: ...

class PricedBehaviorModifier(PricedBehavior):
    def __init__(self, base_behavior: PricedBehavior) -> None:
        self.base_behavior = base_behavior
