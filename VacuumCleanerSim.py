import pygame
import sys

from pygame.locals import *

from Visualizer import Visualizer
from utils.confUtils import CONF as conf
from utils.confUtils import LOG as log


class VacuumCleanerSim:

    def __init__(self):

        self.fps = conf["simulation"]["fps"]
        envConf = conf["environment"]
        tileSize = envConf["tile_size"]

        self.clock = pygame.time.Clock()
        self.visualizer = Visualizer(envConf["width"] * tileSize, envConf["height"] * tileSize)

    def start_simulation(self):
        log.error("Start simulation")
        while True:
            self.clock.tick(self.fps)

            pygameEvents = pygame.event.get()
            self.handle_pygame_events(pygameEvents)

    def handle_pygame_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()


if __name__ == '__main__':
    VacuumCleanerSim().start_simulation()
