import pygame
from pygame.locals import *

from utils.colorUtils import *
from utils.confUtils import LOG as log


class Visualizer:
    def __init__(self, env):
        pygame.init()
        w, h, tile_size = env.get_params()
        self.screen = pygame.display.set_mode((w, h), DOUBLEBUF)
        self.screen.set_alpha(None)
        self.draw_initial_environment(env)
        self.mouse_down = False
        self.start_point = None
        self.temp_rectangle = None

    def update(self, sim_events=None, pygame_events=None):
        if sim_events is None:
            sim_events = []
        if pygame_events is not None:
            self.handle_pygame_events(pygame_events)

        if len(sim_events) != 0:
            self.handle_sim_events(sim_events)

        self.draw_temp_rectangle()

    def handle_sim_events(self, events):
        pass

    def handle_pygame_events(self, events):
        # evtl auf runmode prüfen, um das Hinzufügen von Hindernisse zu verbieten wenn man im SIM mode ist
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                log.error("mouse down")
                self.mouse_down = True
                self.start_point = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                print("mouse down")
                self.mouse_down = False

    def get_updates(self):
        return []

    def draw_initial_environment(self, env):
        self.screen.fill(LIGHT_GREY)
        for obstacle in env.obstacles:
            pygame.draw.rect(self.screen, BLACK, [obstacle[0], obstacle[1], obstacle[2], obstacle[3]])

        pygame.display.update()

    def draw_temp_rectangle(self):
        if self.mouse_down:
            x, y = pygame.mouse.get_pos()
            new_rect = [self.start_point[0], self.start_point[1], x - self.start_point[0], y - self.start_point[1]]
            if self.temp_rectangle is not None:
                pygame.draw.rect(self.screen, LIGHT_GREY, self.temp_rectangle)
            pygame.draw.rect(self.screen, RED, new_rect)

            pygame.display.update([self.temp_rectangle, new_rect])

            self.temp_rectangle = new_rect
