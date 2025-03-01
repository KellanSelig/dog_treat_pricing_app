from enum import StrEnum
from enum import auto


class Status(StrEnum):
    NEW = auto()
    IN_PROGRESS =  auto()
    COMPLETED = auto()
    FAILED =  auto()
