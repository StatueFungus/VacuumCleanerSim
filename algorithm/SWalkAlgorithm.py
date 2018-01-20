from enum import Enum
from random import randint

from algorithm.AbstractCleaningAlgorithm import AbstractCleaningAlgorithm
from events.ConfigurationChanged import ConfigurationChanged
from sprite.Robot import RobotState


class SWalkAlgorithm(AbstractCleaningAlgorithm):
    def __init__(self):
        super().__init__()
        self.state = State.WALK_LINE
        self.steps_between_lines = 0
        self.rotate_clockwise = False
        self.collision_after_direction_change = False
        self.max_steps_between_lines = self._get_max_steps_between_lines()

    def update(self, obstacles, robot):
        super().update(obstacles, robot)

        configuration_events = []

        if self.state == State.WALK_LINE:
            if not robot.busy and self.robot_colided(obstacles, robot):
                new_state = RobotState.WALK_BACKWARDS_THEN_ROTATE
                delta_angle = self._get_current_angle()
                if self.collision_after_direction_change:
                    if randint(0, 1):
                        delta_angle = delta_angle * -1
                    self.rotate_clockwise = delta_angle > 0
                    self.collision_after_direction_change = False
                configuration_events.append(ConfigurationChanged(new_state=new_state, delta_angle=delta_angle))
                self.state = State.MOVE_TO_NEXT_LINE
            return configuration_events

        if self.state == State.MOVE_TO_NEXT_LINE:
            if not robot.busy:
                self.steps_between_lines = self.steps_between_lines + 1

            if self.robot_colided(obstacles, robot):
                new_state = RobotState.WALK_BACKWARDS_THEN_ROTATE
                delta_angle = 180
                configuration_events.append(ConfigurationChanged(new_state=new_state, delta_angle=delta_angle))
                self.steps_between_lines = 0
                self.max_steps_between_lines = self._get_max_steps_between_lines()
                self.state = State.WALK_LINE
                self.collision_after_direction_change = True

            if self.steps_between_lines >= self.max_steps_between_lines :
                new_state = RobotState.ROTATE
                delta_angle = self._get_current_angle()
                configuration_events.append(ConfigurationChanged(new_state=new_state, delta_angle=delta_angle))
                self.state = State.WALK_LINE
                self.steps_between_lines = 0
                self.max_steps_between_lines = self._get_max_steps_between_lines()
                self.rotate_clockwise = not self.rotate_clockwise

            return configuration_events

        return configuration_events

    def _get_current_angle(self):
        return 90 if self.rotate_clockwise else -90

    def _get_max_steps_between_lines(self):
        return randint(2,7)


class State(Enum):
    WALK_LINE = 1,
    MOVE_TO_NEXT_LINE = 2
