import pygame
from pygame.locals import *

from utils.colorUtils import *


class Visualizer:
    def __init__(self, w, h):
        pygame.init()
        self.screen = pygame.display.set_mode((w, h), DOUBLEBUF)
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
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse down")
            if event.type == pygame.MOUSEBUTTONUP:
                print("mouse down")
                mouse_down = False

    def draw_initial_environment(self):
        self.screen.fill(LIGHT_GREY)
        pygame.display.update()
