from events.EventType import *


class ConfigurationChanged:
    type = EventType.CONFIGURATION_CHANGED
    old_c = None
    new_c = None

    def __init__(self, old_c, new_c):
        self.old_c = old_c
        self.new_c = new_c
