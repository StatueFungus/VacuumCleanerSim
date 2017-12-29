from algorithm.AbstractCleaningAlgorithm import AbstractCleaningAlgorithm
from events.ConfigurationChanged import ConfigurationChanged
from sprite.Robot import RobotState
from random import randint


class RandomBounceWalkAlgorithm(AbstractCleaningAlgorithm):
    def __init__(self):
        super().__init__()

    def update(self, obstacles, robot):
        super().update(obstacles, robot)

        configuration_events = []

        if not robot.busy and self.robot_colided(obstacles, robot):
            new_state = RobotState.WALK_BACKWARDS_THEN_ROTATE
            delta_angle = randint(70, 150)
            configuration_events.append(ConfigurationChanged(new_state=new_state, delta_angle=delta_angle))

        return configuration_events
