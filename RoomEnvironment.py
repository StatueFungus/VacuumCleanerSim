from Geometry import Rectangle, Point


class RoomEnvironment():
    def __init__(self, width=800, height=600, tile_size=10):
        self.obstacles = []
        self.robot = None

        self.width = width
        self.height = height
        self.tile_size = tile_size

        self.initialize_walls()

    def update(self, events):
        pass

    def initialize_walls(self):
        self.obstacles.append((0, 0, self.width, self.tile_size))
        self.obstacles.append((0, self.tile_size, self.tile_size, self.height - 2 * self.tile_size))
        self.obstacles.append((0, self.height - self.tile_size, self.width, self.tile_size))
        self.obstacles.append((self.width - self.tile_size, self.tile_size, self.tile_size,
                               self.height - 2 * self.tile_size))

    def add_obstacle(self, rect):
        self.obstacles.append(rect)

    def get_params(self):
        return self.width, self.height, self.tile_size
