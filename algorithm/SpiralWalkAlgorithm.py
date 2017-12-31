from random import randint

from algorithm.AbstractCleaningAlgorithm import AbstractCleaningAlgorithm
from events.ConfigurationChanged import ConfigurationChanged
from sprite.Robot import RobotState


class SpiralWalkAlgorithm(AbstractCleaningAlgorithm):
    def __init__(self):
        super().__init__()

    def update(self, obstacles, robot):
        if not self.started:
            self.start()
            robot.state = RobotState.WALK_ROTATE
            robot.custom_rss = 5

        configuration_events = []

        if self.robot_colided(obstacles, robot):
            new_state = RobotState.STOP

            configuration_events.append(ConfigurationChanged(new_state=new_state))

        return configuration_events
