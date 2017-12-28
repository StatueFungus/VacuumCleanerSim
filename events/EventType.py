from enum import Enum


class EventType(Enum):
    CONFIGURATION_CHANGED = 1
    OBSTACLE_ADDED = 2
    OBSTACLE_DRAWN = 3
    ROBOT_DRAWN = 4
    ROBOT_PLACED = 5
    TILE_COVERED = 6
