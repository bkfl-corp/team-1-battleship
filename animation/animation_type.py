'''
Name: Animation types.
Description: Provides strong types for animations for battleship.
Inputs: N/A
Outputs: N/A
Authors: James Hurd, Joshua Lee, Will Whitehead, Trent Gould, Ky Le
Created: 09/29/24
'''
from enum import Enum, auto

#for passing animation types to run.
class AnimationType(Enum):
    WIN = auto()
    MISS = auto()
    HIT = auto()
