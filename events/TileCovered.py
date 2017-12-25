from events.EventType import EventType


class TileCovered:
    type = EventType.TILE_COVERED
    tile = None

    def __init__(self, tile):
        self.tile = tile
