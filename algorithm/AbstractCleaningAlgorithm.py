from abc import ABC

from sprite.Robot import RobotState


class AbstractCleaningAlgorithm(ABC):
    def __init__(self):
        self.started = False

    def update(self, obstacles, robot):
        if not self.started:
            self.start()
            robot.state = RobotState.WALK

    def robot_colided(self, obstacles, robot):
        for obstacle in obstacles:
            if robot.collides_rectangle(obstacle):
                return True

        return False

    def start(self):
        self.started = True
