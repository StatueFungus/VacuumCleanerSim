import pygame

from sprite.Box import Box
from utils.colorUtils import BLACK


class Obstacle(Box):
    def __init__(self, x, y, width, height, color=BLACK):
        super().__init__(x, y, width, height, color)
