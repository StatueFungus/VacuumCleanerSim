import pygame
from utils.confUtils import CONF as conf
from utils.confUtils import LOG as log


class VacuumCleanerSim:

    clock = None
    fps = conf["simulation"]["fps"]

    def __init__(self):
        self.clock = pygame.time.Clock()

    def start_simulation(self):
        log.error("Start simulation")
        while True:
            self.clock.tick(self.fps)


if __name__ == '__main__':
    VacuumCleanerSim().start_simulation()