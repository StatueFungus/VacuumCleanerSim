import pygame
from pygame.locals import *

from events.ObstacleAdded import ObstacleAdded
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
        self.draw_environment(env)

        self.mouse_down = False
        self.start_point = None
        self.temp_rectangle = None
        self.new_rectangle = None

    def update(self, sim_events=None, pygame_events=None, env=None):
        if sim_events is not None and len(sim_events) != 0:
            self.handle_sim_events(sim_events)
        if pygame_events is not None:
            self.handle_pygame_events(pygame_events)

        self.draw(env)

    def handle_sim_events(self, events):
        pass

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
            return ObstacleAdded(ret)

        return None

    def draw_environment(self, env=None):
        if env is not None:
            for obstacle in env.obstacles:
                pygame.draw.rect(self.screen, BLACK, [obstacle[0], obstacle[1], obstacle[2], obstacle[3]])

    def draw_temp_rectangle(self):
        if self.mouse_down:
            x, y = pygame.mouse.get_pos()
            self.temp_rectangle = [self.start_point[0], self.start_point[1], x - self.start_point[0],
                                   y - self.start_point[1]]

            pygame.draw.rect(self.screen, RED, self.temp_rectangle)

    def set_run_mode(self, new_run_mode):
        self.run_mode = new_run_mode

    def draw(self, env=None):

        if self.run_mode == Runmode.BUILD:
            self.screen.fill(LIGHT_GREY)
            self.draw_temp_rectangle()
            self.draw_environment(env)
            pygame.display.update()
