from enum import Enum

from sprite.Box import Box
from utils.colorUtils import LIGHT_GREY, DARK_GREY, BLACK, WHITE
from utils.confUtils import CONF as conf


class Tile(Box):
    def __init__(self, x: int, y: int):
        ts = conf["environment"]["tile_size"]
        super().__init__(x, y, ts, ts, LIGHT_GREY)

        self.cover_count = 0
        self.temp_count = 0
        self.need_update = False
        self.state = TileState.UNCOVERED

        self.dirt_per_cover = conf["robot"].get("dirt_per_cover", 7)
        self.dirt = conf["simulation"].get("dirt", 35)
        self.ticks_for_cover = conf["simulation"].get("ticks_for_cover", 10)
        self.dirt = self.dirt if self.dirt % self.dirt_per_cover == 0 else self.dirt - self.dirt % self.dirt_per_cover
        self.steps = self.dirt / self.dirt_per_cover
        self.base_color = [255 - self.dirt, 255 - self.dirt, 255 - self.dirt]

    def update(self):
        if self.need_update:
            if self.state == TileState.COVERED_BY_OBSTACLE:
                self.image.fill(DARK_GREY)

            if self.state == TileState.COVERED:
                color = list(map(lambda x: x + self.cover_count * self.dirt_per_cover, self.base_color)) # calculates the new color
                self.image.fill(color)

        self.need_update = False

    def set_state(self, new_state):
        self.state = new_state
        self.need_update = True

    def increase_cover_count(self):
        if self.temp_count == 0:
            self.cover_count = self.cover_count + 1

        self.temp_count = self.temp_count + 1

        if self.temp_count >= self.ticks_for_cover and self.cover_count < self.steps:
            self.temp_count = 0


class TileState(Enum):
    UNCOVERED = 0
    COVERED = 1
    COVERED_BY_OBSTACLE = 2
