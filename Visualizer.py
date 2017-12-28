import pygame
from pygame.locals import *

from events.EventType import EventType
from events.ObstacleDrawn import ObstacleDrawn
from utils.Runmode import Runmode
from utils.colorUtils import *
from utils.confUtils import LOG as log


class Visualizer:
    run_mode = Runmode.BUILD

    def __init__(self, env):
        pygame.init()
        w, h, tile_size = env.get_params()

        self.screen = pygame.display.set_mode((w, h), DOUBLEBUF)
        self.screen.set_alpha(None)

        self.tile_group = pygame.sprite.Group()
        # self.tile_group.add(env.tiles)

        self.wall_group = pygame.sprite.Group()
        self.wall_group.add(env.walls)

        self.obstacle_group = pygame.sprite.Group()
        self.obstacle_group.add(env.obstacles)

        # --- Temp rectangle for placing new rectangles ---
        self.mouse_down = False
        self.start_point = None
        self.temp_rectangle = None
        self.new_rectangle = None

    def update(self, sim_events=None, pygame_events=None):
        if sim_events is not None and len(sim_events) != 0:
            self.handle_sim_events(sim_events)
        if pygame_events is not None:
            self.handle_pygame_events(pygame_events)

        self.draw()

    def handle_sim_events(self, events):
        for event in events:
            if event.type == EventType.OBSTACLE_ADDED:
                log.error("Add Obstacle")
                self.obstacle_group.add(event.new_obstacle)
            if event.type == EventType.TILE_COVERED:
                self.tile_group.add(event.tile)

    def handle_pygame_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                log.error("mouse down")
                self.mouse_down = True
                self.start_point = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                log.error("mouse up")
                self.mouse_down = False
                self.new_rectangle = self.temp_rectangle
                self.start_point = None
                self.temp_rectangle = None

    def get_obstacle_added_event(self):
        if self.new_rectangle is not None:
            ret = self.new_rectangle
            self.new_rectangle = None
            return ObstacleDrawn(ret)

        return None

    def draw_temp_rectangle(self):
        if self.mouse_down:
            x, y = pygame.mouse.get_pos()
            self.temp_rectangle = [self.start_point[0], self.start_point[1], x - self.start_point[0],
                                   y - self.start_point[1]]

            pygame.draw.rect(self.screen, RED, self.temp_rectangle)

    def clean_obstacles(self):
        self.obstacle_group.empty()

    def set_run_mode(self, new_run_mode):
        self.run_mode = new_run_mode

    def draw(self):

        self.screen.fill(WHITE)

        self.tile_group.update()
        self.wall_group.update()
        self.obstacle_group.update()

        self.tile_group.draw(self.screen)
        self.wall_group.draw(self.screen)
        self.obstacle_group.draw(self.screen)

        self.draw_temp_rectangle()

        pygame.display.flip()
