from enum import Enum

import pygame
import math

from sprite.Tile import Tile
from utils.colorUtils import GREEN, BLACK
from utils.mathUtils import distance, get_direction
from utils.pygameUtils import rot_center
from utils.confUtils import CONF as conf


class RobotState(Enum):
    WALK = 1
    ROTATE = 2
    WALK_ROTATE = 3
    STOP = 4
    WALK_BACKWARDS_THEN_ROTATE = 5


class Robot(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color=BLACK):
        super().__init__()
        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        self._org_image = self.image
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        pygame.draw.polygon(self.image, GREEN, [(0, radius), (2 * radius, radius), (radius, 0)])

        self.state = RobotState.STOP
        self.rect = self.image.get_rect()
        self._org_rect = self.rect
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.angle = 0
        self.angle_delta = 0  # angle to rotate
        self.walk_delta = 0  # distance to walk
        self.radius = radius
        self.busy = False
        self.direction = get_direction(self.angle)

        self.wss = conf["robot"]["wss"]
        self.rss = conf["robot"]["rss"]

        # these two properties are used for slower walk and/or slower rotating while walking
        self.custom_wss = self.wss
        self.custom_rss = self.rss

    def get_configuration(self):
        return self.rect.x, self.rect.y, self.angle

    def set_configuration(self, c):
        if c.new_state is not None:
            self.state = c.new_state
        if c.delta_angle is not None:
            self.angle_delta = c.delta_angle
        if c.rss is not None:
            self.custom_rss = c.rss if c.rss < self.rss else self.rss
        if c.wss is not None:
            self.custom_wss = c.wss if c.wss <= self.wss else self.wss

    def collides_rectangle(self, rect):
        d = self.radius
        c = self.rect.x + d, self.rect.y + d  # configuration of the middle of the circle
        # get vertices from rectangle
        v0, v1, v2, v3 = [rect.get_vertex(i) for i in range(4)]

        # check if c is in the rectangle
        if v0[0] < c[0] < v1[0] and v3[1] < c[1] < v0[1]:
            return True

        # check if the circle overlaps the rectangle
        if v0[0] < c[0] < v1[0] and (v3[1] - d < c[1] < v3[1] or v0[1] < c[1] < v0[1] + d):  # top / bottom
            return True
        if v3[1] < c[1] < v0[1] and (v0[0] - d < c[0] < v0[0] or v1[0] < c[0] < v1[0] + d):  # left / right
            return True

        # check distances to the corners
        if distance(c, v0) < d or distance(c, v1) < d or distance(c, v2) < d or distance(c, v3) < d:
            return True

        return False

    def covers_tile(self, tile: Tile):
        d = self.radius
        c = self.rect.x + d, self.rect.y + d  # configuration of the middle of the circle
        # get vertices from rectangle
        v0, v1, v2, v3 = [tile.get_vertex(i) for i in range(4)]

        return distance(c, v0) < d and distance(c, v1) < d and distance(c, v2) < d and distance(c, v3) < d

    def update(self):

        if self.state == RobotState.ROTATE:
            # rotate logic. robot rotates until it reaches the new angle
            if not self.busy:
                self.busy = True

            if math.fabs(self.angle_delta) < self.custom_rss:
                self.angle = (self.angle - self.angle_delta) % 360
                self.angle_delta = 0

                self.direction = get_direction(self.angle)
                self.state = RobotState.WALK
                self.busy = False

            if self.angle_delta > 0:
                self.angle = (self.angle + self.custom_rss) % 360
                self.angle_delta = self.angle_delta - self.custom_rss

            if self.angle_delta < 0:
                self.angle = (self.angle - self.custom_rss) % 360
                self.angle_delta = self.angle_delta + self.custom_rss

        if self.state == RobotState.WALK_ROTATE:
            # robot rotates every update period
            self.angle = (self.angle - self.custom_rss) % 360
            self.direction = get_direction(self.angle)

        if self.state == RobotState.WALK or self.state == RobotState.WALK_ROTATE:
            # walk logic
            self.x = self.x - self.direction[0] * self.custom_wss
            self.y = self.y - self.direction[1] * self.custom_wss

        if self.state == RobotState.WALK_BACKWARDS_THEN_ROTATE:
            # walk backwards logic
            if not self.busy:
                self.busy = True
                self.walk_delta = 15

            if self.walk_delta != 0:
                self.x = self.x + self.direction[0] * self.custom_wss
                self.y = self.y + self.direction[1] * self.custom_wss
                self.walk_delta = self.walk_delta - 2  # walk speed

            if self.walk_delta <= 0:
                self.y = self.y + self.walk_delta
                self.walk_delta = 0

                self.state = RobotState.ROTATE

        if self.state == RobotState.STOP:
            # stop logic
            self.busy = False
            # reset to normal speed
            self.custom_rss = self.rss
            self.custom_wss = self.wss

        # this is nessecary because the coordinates of self.rect can only be integers.
        # if there is a direction of (0.1,1) the x-coord does not affect the direction
        self.rect.x = self.x
        self.rect.y = self.y

        self.image = rot_center(self._org_image, (self.angle % 360) * -1)
