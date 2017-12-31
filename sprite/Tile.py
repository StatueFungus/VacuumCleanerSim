from enum import Enum

from sprite.Box import Box
from utils.colorUtils import LIGHT_GREY, BLACK
from utils.confUtils import CONF as conf


class Tile(Box):
    def __init__(self, x: int, y: int):

        ts = conf["environment"]["tile_size"]
        super().__init__(x, y, ts, ts, LIGHT_GREY)

        self.state = TileState.UNCOVERED

    def update(self):
        if self.state == TileState.COVERED_BY_OBSTACLE:
            self.image.fill(BLACK)


class TileState(Enum):
    UNCOVERED = 0
    COVERED = 1
    COVERED_BY_OBSTACLE = 2
