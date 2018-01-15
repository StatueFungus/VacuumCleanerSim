from enum import Enum

from algorithm.AbstractCleaningAlgorithm import AbstractCleaningAlgorithm
from events.ConfigurationChanged import ConfigurationChanged
from sprite.Robot import RobotState


class SWalkAlgorithm(AbstractCleaningAlgorithm):
    def __init__(self):
        super().__init__()
        self.state = State.WALK_LINE
        self.steps_between_lines = 0
        self.rotate_clockwise = False

    def update(self, obstacles, robot):
        super().update(obstacles, robot)

        configuration_events = []

        if self.state == State.WALK_LINE:
            if not robot.busy and self.robot_colided(obstacles, robot):
                new_state = RobotState.WALK_BACKWARDS_THEN_ROTATE
                delta_angle = self._get_current_angle()
                configuration_events.append(ConfigurationChanged(new_state=new_state, delta_angle=delta_angle))
                self.state = State.MOVE_TO_NEXT_LINE
            return configuration_events

        if self.state == State.MOVE_TO_NEXT_LINE:
            if not robot.busy:
                self.steps_between_lines = self.steps_between_lines + 1

            if self.robot_colided(obstacles, robot):
                new_state = RobotState.WALK_BACKWARDS_THEN_ROTATE
                delta_angle = self._get_current_angle()
                configuration_events.append(ConfigurationChanged(new_state=new_state, delta_angle=delta_angle))

            if self.steps_between_lines >= 7:
                new_state = RobotState.ROTATE
                delta_angle = self._get_current_angle()
                configuration_events.append(ConfigurationChanged(new_state=new_state, delta_angle=delta_angle))
                self.state = State.WALK_LINE
                self.steps_between_lines = 0
                self.rotate_clockwise = not self.rotate_clockwise

            return configuration_events

        return configuration_events

    def _get_current_angle(self):
        return 90 if self.rotate_clockwise else -90


class State(Enum):
    WALK_LINE = 1,
    MOVE_TO_NEXT_LINE = 2
