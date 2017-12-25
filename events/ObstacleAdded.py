from events.EventType import EventType


class ObstacleAdded:
    type = EventType.OBSTACLE_ADDED

    def __init__(self, new_obstacle):
        self.new_obstacle = new_obstacle