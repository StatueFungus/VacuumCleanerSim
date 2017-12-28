from abc import ABC, abstractmethod


class AbstractCleaningAlgorithm(ABC):

    @abstractmethod
    def update(self, obstacles, robot):
        pass

    def robot_colided(self, obstacles, robot):
        for obstacle in obstacles:
            if robot.collides_rectangle(obstacle):
                return True

        return False
