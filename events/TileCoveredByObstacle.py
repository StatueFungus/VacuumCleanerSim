from events.EventType import EventType
from sprite.Tile import Tile, TileState


class TileCoveredByObstacle:
    type = EventType.TILE_COVERED_BY_OBSTACLE

    def __init__(self, tile: Tile):
        self.tile = tile
        self.tile.set_state(TileState.COVERED_BY_OBSTACLE)
