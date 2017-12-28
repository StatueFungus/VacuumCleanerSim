from events.EventType import EventType
from events.ObstacleAdded import ObstacleAdded
from events.RobotPlaced import RobotPlaced
from sprite.Obstacle import Obstacle
from sprite.Robot import Robot
from utils.colorUtils import GREEN
from utils.listUtils import filter_none


class RoomEnvironment:
    def __init__(self, width, height, tile_size):
        self.obstacles = []
        self.walls = []
        self.robot = None

        self.width = width
        self.height = height
        self.tile_size = tile_size

        self.initialize_walls()

    def update(self, events):
        new_events = []

        for event in events:
            if event is not None:
                if event.type == EventType.OBSTACLE_DRAWN:
                    new_events.append(self.handle_drawn_obstacle(event.drawn_obstacle))
                if event.type == EventType.ROBOT_DRAWN:
                    new_events.append(self.handle_drawn_robot(event.drawn_robot))
                if event.type == EventType.CONFIGURATION_CHANGED:
                    new_events.append(self.handle_configuration_changed(event))

        return filter_none(new_events)

    def initialize_walls(self):
        self.walls.append(Obstacle(0, 0, self.width, self.tile_size))
        self.walls.append(Obstacle(0, self.tile_size, self.tile_size, self.height - 2 * self.tile_size))
        self.walls.append(Obstacle(0, self.height - self.tile_size, self.width, self.tile_size))
        self.walls.append(Obstacle(self.width - self.tile_size, self.tile_size, self.tile_size,
                                   self.height - 2 * self.tile_size))

        self.obstacles = list(self.walls)

    def get_params(self):
        return self.width, self.height, self.tile_size

    def clear_obstacles(self):
        self.obstacles = self.walls[:]  # copies the wall list

    def set_robot(self, robot):
        self.robot = robot

    def handle_drawn_obstacle(self, obstacle):
        x, y = obstacle[0], obstacle[1]
        width, height = obstacle[2], obstacle[3]

        if width == 0 or height == 0:
            return None

        # clip drawn obstacle on the walls
        if width < 0:
            width = width * -1
            x = x - width

        if height < 0:
            height = height * -1
            y = y - height

        if x + width > self.width - self.tile_size:
            width = width - ((x + width) - (self.width - self.tile_size))

        if y + height > self.height - self.tile_size:
            height = height - ((y + height) - (self.height - self.tile_size))

        if x < self.tile_size:
            x = self.tile_size

        if y < self.tile_size:
            y = self.tile_size

        # return ObstacleAdded event with clipped obstacle
        new_obstacle = Obstacle(x, y, width, height, GREEN)
        self.obstacles.append(new_obstacle)
        return ObstacleAdded(new_obstacle)

    def handle_drawn_robot(self, robot):
        x, y, diameter = robot[0], robot[1], robot[2]

        # TODO check for collision when placing
        if self.robot is not None:
            self.robot.rect.x = x
            self.robot.rect.y = y
            return RobotPlaced(self.robot)

        new_robot = Robot(x, y, diameter)
        self.robot = new_robot
        return RobotPlaced(new_robot)

    def handle_configuration_changed(self, event):
        self.robot.set_configuration(event.new_c)
