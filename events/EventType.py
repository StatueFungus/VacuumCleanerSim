from enum import Enum


class EventType(Enum):
    CONFIGURATION_CHANGED = 1
    OBSTACLE_ADDED = 2
    OBSTACLE_DRAWN = 3
    TILE_COVERED = 4
