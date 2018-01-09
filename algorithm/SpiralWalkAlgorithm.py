from enum import Enum
from random import randint

from algorithm.AbstractCleaningAlgorithm import AbstractCleaningAlgorithm
from events.ConfigurationChanged import ConfigurationChanged
from sprite.Robot import RobotState


class SpiralWalkAlgorithm(AbstractCleaningAlgorithm):
    def __init__(self):
        super().__init__()
        self.rotation_speed = 5
        self.count = 0
        self.last_config_change = -1
        self.mode = Mode.SPIRAL

    def update(self, obstacles, robot):

        self.count = self.count + 1

        if not self.started:
            self.start()
            robot.state = RobotState.WALK_ROTATE
            robot.custom_rss = 5

        if self.mode == Mode.SPIRAL and self.robot_colided(obstacles, robot):
            self.mode = Mode.RANDOM_WALK
            self.rotation_speed = 5
            return [ConfigurationChanged(rss=self.rotation_speed)]

        if self.mode == Mode.SPIRAL and 180 <= robot.angle <= 180 + self.rotation_speed or 0 <= robot.angle <= self.rotation_speed:
            self.rotation_speed = self.rotation_speed / 1.1
            return [ConfigurationChanged(rss=self.rotation_speed)]

        if self.mode == Mode.RANDOM_WALK and not robot.busy and self.robot_colided(obstacles, robot):
            new_state = RobotState.WALK_BACKWARDS_THEN_ROTATE
            delta_angle = randint(70, 150)
            if randint(0, 1):
                delta_angle = delta_angle * -1
            return [ConfigurationChanged(new_state=new_state, delta_angle=delta_angle)]

        return []


class Mode(Enum):
    RANDOM_WALK = 1,
    SPIRAL = 2
