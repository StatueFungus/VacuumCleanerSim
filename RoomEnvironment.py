class RoomEnvironment():
    def __init__(self, width=800, height=600, tile_size=10):
        self.obstacles = []
        self.robot = None

        self.width = width
        self.height = height
        self.tile_size = tile_size

    def update(self, events):
        pass

    def add_obstacle(self, rect):
        # TODO test if rect colides with robot
        return True

    def get_params(self):
        return self.width, self.height, self.tile_size
