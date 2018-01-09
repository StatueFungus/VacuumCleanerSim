import pygame

from utils.colorUtils import BLACK


class Box(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_vertex(self, idx: int):
        idx = idx % 4

        if idx == 0:
            return self.rect.x, self.rect.y + self.height
        if idx == 1:
            return self.rect.x + self.width, self.rect.y + self.height
        if idx == 2:
            return self.rect.x + self.width, self.rect.y
        if idx == 3:
            return self.rect.x, self.rect.y

    def __repr__(self):
        return "[" + str(self.rect.x) + ", " + str(self.rect.y) + ", " + str(self.width) + ", " + str(self.height) + "]"
