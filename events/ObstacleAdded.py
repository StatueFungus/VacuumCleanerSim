from events.EventType import EventType


class ObstacleAdded:
    type = EventType.OBSTACLE_ADDED

    # new_obstacle is from type "sprite.Obstacle"
    def __init__(self, new_obstacle):
        self.new_obstacle = new_obstacle
