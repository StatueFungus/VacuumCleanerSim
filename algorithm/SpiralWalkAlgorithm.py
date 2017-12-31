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

    def update(self, obstacles, robot):

        self.count = self.count + 1

        if not self.started:
            self.start()
            robot.state = RobotState.WALK_ROTATE
            robot.custom_rss = 5

        if self.robot_colided(obstacles, robot):
            new_state = RobotState.STOP

            return [ConfigurationChanged(new_state=new_state)]

        if 180 <= robot.angle <= 180 + self.rotation_speed or 0 <= robot.angle <= self.rotation_speed:
            self.rotation_speed = self.rotation_speed / 1.1
            return [ConfigurationChanged(rss=self.rotation_speed)]

        return []
