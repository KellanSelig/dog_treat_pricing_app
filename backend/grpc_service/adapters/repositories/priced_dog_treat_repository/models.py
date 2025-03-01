from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from backend.grpc_service.core.models.perform_dog_trick_models import Status


@dataclass
class PricedTrick:
    id: UUID
    amount_dog_treat: float
    amount_belly_rub: float
    created_at: datetime
    updated_at: datetime
    current_status: Status
