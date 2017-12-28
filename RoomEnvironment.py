from events.EventType import EventType
from events.ObstacleAdded import ObstacleAdded
from sprite.Obstacle import Obstacle
from utils.colorUtils import GREEN


class RoomEnvironment:
    def __init__(self, width, height, tile_size):
        self.obstacles = []
        self.walls = []
        self.robot = None

        self.width = width
        self.height = height
        self.tile_size = tile_size

        self.initialize_walls()

    def update(self, event):
        if event.type == EventType.OBSTACLE_DRAWN:
            return self.handle_drawn_obstacle(event.drawn_obstacle)

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
        return ObstacleAdded(new_obstacle)
