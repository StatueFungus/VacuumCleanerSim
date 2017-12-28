import pygame

from utils.colorUtils import GREEN


class Robot(pygame.sprite.Sprite):
    def __init__(self, x, y, diameter, color):
        super().__init__()
        self.image = pygame.Surface([diameter * 2, diameter * 2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (diameter, diameter), diameter)
        pygame.draw.polygon(self.image, GREEN, [(0, diameter), (2 * diameter, diameter), (diameter, 0)])

        self.org_image = self.image
        self.angle = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
