from events.EventType import EventType


class ObstacleDrawn:
    type = EventType.OBSTACLE_DRAWN

    def __init__(self, drawn_obstacle):
        self.drawn_obstacle = drawn_obstacle
