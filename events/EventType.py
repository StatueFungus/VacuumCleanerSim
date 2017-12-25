from enum import Enum


class EventType(Enum):
    CONFIGURATION_CHANGED = 1
    OBSTACLE_ADDED = 2
    TILE_COVERED = 3
