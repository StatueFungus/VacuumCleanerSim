from events.EventType import EventType
from sprite.Tile import Tile


class TileCovered:
    type = EventType.TILE_COVERED

    def __init__(self, tile: Tile):
        self.tile = tile
