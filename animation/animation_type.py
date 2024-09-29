#for passing animation types to run.
from enum import Enum, auto

class AnimationType(Enum):
    WIN = auto()
    MISS = auto()
    HIT = auto()
