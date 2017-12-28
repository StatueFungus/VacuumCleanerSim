from events.EventType import *


class ConfigurationChanged:
    type = EventType.CONFIGURATION_CHANGED

    def __init__(self, new_state=None, delta_angle=None):
        self.new_state = new_state
        self.delta_angle = delta_angle