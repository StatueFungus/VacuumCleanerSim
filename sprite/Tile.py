from sprite.Box import Box
from utils.colorUtils import LIGHT_GREY
from utils.confUtils import CONF as conf


class Tile(Box):
    def __init__(self, x: int, y: int):

        ts = conf["environment"]["tile_size"]
        super().__init__(x, y, ts, ts, LIGHT_GREY)

        self.covered = False
