from events.EventType import EventType
from sprite.Tile import Tile, TileState


class TileCovered:
    type = EventType.TILE_COVERED

    def __init__(self, tile: Tile):
        self.tile = tile
        self.tile.state = TileState.COVERED
