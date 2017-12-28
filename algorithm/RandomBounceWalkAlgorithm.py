import numpy

from algorithm.AbstractCleaningAlgorithm import AbstractCleaningAlgorithm
from events.ConfigurationChanged import ConfigurationChanged


class RandomBounceWalkAlgorithm(AbstractCleaningAlgorithm):
    def update(self, obstacles, robot):
        configuration_events = []

        if not self.robot_colided(obstacles, robot):
            old_c = robot.get_configuration()
            new_c = numpy.add(old_c, (0, -2, 0))
            configuration_events.append(ConfigurationChanged(old_c, new_c))

        return configuration_events
