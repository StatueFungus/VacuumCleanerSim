from enum import Enum

import pygame
import sys

from pygame.locals import *

from RoomEnvironment import RoomEnvironment
from Visualizer import Visualizer
from utils.confUtils import CONF as conf
from utils.confUtils import LOG as log

class Runmode(Enum):
    # should be enumtype
    BUILD = 1
    SIM = 2

class VacuumCleanerSim:
    def __init__(self):

        self.run_mode = Runmode.BUILD
        self.event_stream = []
        self.fps = conf["simulation"]["fps"]
        env_conf = conf["environment"]
        tile_size = env_conf["tile_size"]

        self.clock = pygame.time.Clock()
        self.environment = RoomEnvironment(env_conf["width"], env_conf["height"], tile_size)
        self.visualizer = Visualizer(self.environment)

    def start_simulation(self):
        log.error("Start simulation")
        while True:
            self.clock.tick(self.fps)
            pygame_events = pygame.event.get()
            self.handle_pygame_events(pygame_events)

            new_events = []
            if self.run_mode == Runmode.BUILD:
                new_rectangles = self.visualizer.get_updates()
                for rect in new_rectangles:
                    if self.environment.add_obstacle(
                            rect):  # prüft, ob das Hindernis gesetzt werden kann, oder ob der Roboter gerade an der Position steht
                        new_events.append(rect)

                pass
            elif self.run_mode == Runmode.SIM:
                configuration_events = []
                # configuration_events = self.algorithm.update(environment)
                new_events.append(configuration_events)

                environment_events = self.environment.update(configuration_events)
                new_events.append(environment_events)

                self.visualizer.update(new_events)
                pass

            self.event_stream.append(new_events)

    def handle_pygame_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_m:
                if self.run_mode == Runmode.BUILD:
                    self.run_mode = Runmode.SIM
                elif self.run_mode == Runmode.SIM:
                    self.run_mode = Runmode.BUILD
                log.error("Switched runmode")
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()


if __name__ == '__main__':
    VacuumCleanerSim().start_simulation()


