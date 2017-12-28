import pygame

from utils.colorUtils import GREEN, BLACK
from utils.mathUtils import distance


class Robot(pygame.sprite.Sprite):
    def __init__(self, x, y, diameter, color=BLACK):
        super().__init__()
        self.image = pygame.Surface([diameter * 2, diameter * 2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (diameter, diameter), diameter)
        pygame.draw.polygon(self.image, GREEN, [(0, diameter), (2 * diameter, diameter), (diameter, 0)])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = 0
        self.diameter = diameter

    def get_configuration(self):
        return self.rect.x, self.rect.y, self.angle

    def set_configuration(self, c):
        self.rect.x = c[0]
        self.rect.y = c[1]
        self.angle = c[2]

    def collides_rectangle(self, rect):
        d = self.diameter
        c = self.rect.x + d, self.rect.y + d  # configuration of the middle of the circle
        # get vertices from rectangle
        v0, v1, v2, v3 = [rect.get_vertex(i) for i in range(4)]

        # check if c is in the rectangle
        if v0[0] < c[0] < v1[0] and v3[1] < c[1] < v0[1]:
            return True

        # check if the circle overlaps the rectangle
        if v0[0] < c[0] < v1[0] and (v3[1] - d < c[1] < v3[1] or v0[1] < c[1] < v0[1] + d):
            return True
        if v3[1] < c[1] < v0[1] and (v0[1] - d < c[1] < v0[1] or v1[1] < c[1] < v1[1] + d):
            return True

        # check distances to the corners
        if distance(c, v0) < d or distance(c, v1) < d or distance(c, v2) < d or distance(c, v3) < d:
            return True

        return False
