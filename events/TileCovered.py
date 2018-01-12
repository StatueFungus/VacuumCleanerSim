from events.EventType import EventType
from sprite.Tile import Tile, TileState


class TileCovered:
    type = EventType.TILE_COVERED

    def __init__(self, tile: Tile):
        self.tile = tile
        self.tile.set_state(TileState.COVERED)
        self.tile.increase_cover_count()

    def is_first_cover(self):
        return self.tile.temp_count == 1 and self.tile.cover_count == 1
