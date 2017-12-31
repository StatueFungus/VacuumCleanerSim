from events.EventType import *


class ConfigurationChanged:
    type = EventType.CONFIGURATION_CHANGED

    def __init__(self, new_state=None, delta_angle=None, rss=None, wss=None):
        self.new_state = new_state
        self.delta_angle = delta_angle
        self.rss = rss
        self.wss = wss
