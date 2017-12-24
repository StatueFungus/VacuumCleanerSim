import pygame
from pygame.locals import *

from utils.colorUtils import *


class Visualizer:
    def __init__(self, env):
        pygame.init()
        w, h, tile_size = env.get_params()
        self.screen = pygame.display.set_mode((w * tile_size, h * tile_size), DOUBLEBUF)
        self.screen.set_alpha(None)
        self.draw_initial_environment()

    def update(self, sim_events=None, pygame_events=None):
        if sim_events is None:
            sim_events = []
        if pygame_events is not None:
            self.handle_pygame_events(pygame_events)

        if len(sim_events) != 0:
            self.handle_sim_events(sim_events)

    def handle_sim_events(self, events):
        pass

    def handle_pygame_events(self, events):
        # evtl auf runmode prüfen, um das Hinzufügen von Hindernisse zu verbieten wenn man im SIM mode ist
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse down")
            if event.type == pygame.MOUSEBUTTONUP:
                print("mouse down")
                mouse_down = False

    def get_updates(self):
        return []

    def draw_initial_environment(self):
        self.screen.fill(LIGHT_GREY)
        pygame.display.update()
