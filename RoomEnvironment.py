from events.EventType import EventType
from events.ObstacleAdded import ObstacleAdded
from events.RobotPlaced import RobotPlaced
from events.TileCovered import TileCovered
from sprite import Box
from sprite.Obstacle import Obstacle
from sprite.Robot import Robot
from sprite.Tile import Tile, TileState
from utils.colorUtils import DARK_GREY
from utils.listUtils import filter_none


class RoomEnvironment:
    def __init__(self, width: int, height: int, tile_size: int, obstacles=None, robot=None):
        self.obstacles = []
        self.walls = []
        self.tiles = []
        self.robot = None

        self.width = width
        self.height = height
        self.tile_size = tile_size

        self.initialize_tiles()
        self.initialize_walls()

        if obstacles is not None:
            self.initialize_default_obstacles(obstacles)

        if robot is not None:
            self.initialize_default_robot(robot)

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

        new_events.extend(self.check_for_new_covered_tiles())

        return filter_none(new_events)

    def initialize_walls(self):
        wall_color = DARK_GREY
        self.walls.append(Obstacle(0, 0, self.width, self.tile_size, wall_color))
        self.walls.append(Obstacle(0, self.tile_size, self.tile_size, self.height - 2 * self.tile_size, wall_color))
        self.walls.append(Obstacle(0, self.height - self.tile_size, self.width, self.tile_size, wall_color))
        self.walls.append(Obstacle(self.width - self.tile_size, self.tile_size, self.tile_size,
                                   self.height - 2 * self.tile_size, wall_color))

        for obstacle in self.walls:
            self._add_obstacle(obstacle)

    def initialize_tiles(self):
        for x in range(0, self.width, self.tile_size):
            col = []
            for y in range(0, self.height, self.tile_size):
                col.append(Tile(x, y))

            self.tiles.append(col)

    def get_params(self):
        return self.width, self.height, self.tile_size

    def clear_obstacles(self):
        self.initialize_tiles()
        self.initialize_walls()

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
        new_obstacle = Obstacle(x, y, width, height, DARK_GREY)
        self._add_obstacle(new_obstacle)
        return ObstacleAdded(new_obstacle)

    def _add_obstacle(self, obstacle: Obstacle):
        self.obstacles.append(obstacle)
        affected_tiles = self.get_affected_tiles(obstacle.rect.x, obstacle.rect.y, obstacle.width, obstacle.height)
        for tile in affected_tiles:
            tile.state = TileState.COVERED_BY_OBSTACLE

    def handle_drawn_robot(self, robot):
        x, y, radius = robot[0], robot[1], robot[2]

        # TODO check for collision when placing
        if self.robot is not None:
            self.robot.rect.x = x
            self.robot.rect.y = y
            return RobotPlaced(self.robot)

        new_robot = Robot(x, y, radius)
        self.robot = new_robot
        return RobotPlaced(new_robot)

    def handle_configuration_changed(self, event):
        self.robot.set_configuration(event)

    def check_for_new_covered_tiles(self):
        covered_tiles_events = []
        if self.robot is not None:
            x, y, r = self.robot.x, self.robot.y, self.robot.radius
            affected_tiles = self.get_affected_tiles(x, y, r * 2, r * 2)
            affected_covered_tiles = list(filter(lambda t: t.state == TileState.UNCOVERED and self.robot.covers_tile(t),
                                                 affected_tiles))

            covered_tiles_events.extend(map(lambda t: TileCovered(t), affected_covered_tiles))
        return covered_tiles_events

    def get_affected_tiles(self, x, y, width, height):
        affected_tiles = []
        start_x = int(x / self.tile_size)
        start_y = int(y / self.tile_size)
        end_x = int((x + width) / self.tile_size)
        end_x = end_x - 1 if x % self.tile_size == 0 else end_x
        end_y = int((y + height) / self.tile_size)
        end_y = end_y - 1 if y % self.tile_size == 0 else end_y

        for idx_x in range(start_x, end_x + 1):
            for idx_y in range(start_y, end_y + 1):
                affected_tiles.append(self.tiles[idx_x][idx_y])

        return affected_tiles

    def get_tile_count(self):
        count = 0
        for col in self.tiles:
            uncovered_tiles = list(filter(lambda t: t.state == TileState.UNCOVERED, col))
            count = count + len(uncovered_tiles)
        return count

    def initialize_default_obstacles(self, obstacles):
        for obstacle in obstacles:
            self._add_obstacle(Obstacle(obstacle[0],obstacle[1],obstacle[2],obstacle[3], DARK_GREY))

    def initialize_default_robot(self, robot):
        self.robot = Robot(robot[0], robot[1], robot[2])
