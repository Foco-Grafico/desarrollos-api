from enum import Enum

class STATUS_DEV(Enum):
    IN_PROGRESS = 1
    IN_PRESALE = 2
    IN_BUILDING = 3
    IN_DELIVERED = 4
    HIDDEN = 5
    AVAILABLE = 6

class STATUS_BATCH(Enum):
    AVAILABLE = 1
    SOLD = 2
    RESERVED = 3