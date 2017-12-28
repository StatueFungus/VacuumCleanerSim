from events.EventType import EventType


class RobotDrawn:
    type = EventType.ROBOT_DRAWN

    def __init__(self, drawn_robot):
        self.drawn_robot = drawn_robot
