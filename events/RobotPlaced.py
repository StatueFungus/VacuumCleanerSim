from events.EventType import EventType


class RobotPlaced:
    type = EventType.ROBOT_PLACED

    def __init__(self, placed_robot):
        self.placed_robot = placed_robot
