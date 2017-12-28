from enum import Enum

import pygame
import sys

from pygame.locals import *

from RoomEnvironment import RoomEnvironment
from Visualizer import Visualizer
from algorithm.AbstractCleaningAlgorithm import BaseCleaningAlgorithm
from utils.Runmode import Runmode
from utils.confUtils import CONF as conf
from utils.confUtils import LOG as log


class VacuumCleanerSim:
    def __init__(self):

        self.run_mode = Runmode.BUILD
        self.event_stream = []
        self.fps = conf["simulation"]["fps"]
        env_conf = conf["environment"]
        tile_size = env_conf["tile_size"]

        self.clock = pygame.time.Clock()
        self.environment = RoomEnvironment(env_conf["width"], env_conf["height"], tile_size)
        self.visualizer = Visualizer(self.environment, self.clock)
        self.algorithm = BaseCleaningAlgorithm()

    def start_simulation(self):
        log.error("Start simulation")
        while True:
            self.clock.tick(self.fps)
            pygame_events = pygame.event.get()
            self.handle_pygame_events(pygame_events)

            new_events = []
            if self.run_mode == Runmode.BUILD:
                obstacle_drawn_event = self.visualizer.get_obstacle_added_event()

                if obstacle_drawn_event is not None:
                    log.error(obstacle_drawn_event.drawn_obstacle)
                    obstacle_added_event = self.environment.update(obstacle_drawn_event)
                    if obstacle_added_event is not None:
                        new_events.append(obstacle_added_event)

                self.visualizer.update(pygame_events=pygame_events, sim_events=new_events)

            elif self.run_mode == Runmode.SIM:
                # get configuration change events from algorithm. It does not affect the environment directly
                configuration_events = self.algorithm.update(self.environment)
                new_events.append(configuration_events)

                # apply configuration change event to the environment
                # and retrieve environment changes like covered tiles
                environment_events = self.environment.update(configuration_events)
                new_events.append(environment_events)

                # update the visualizer with all new events
                self.visualizer.update(new_events)

            # save all events into the event stream. this could be useful for re-simulating ...
            self.event_stream.append(new_events)

    def handle_pygame_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_c:
                log.error("Clear obstacles")
                self.environment.clear_obstacles()
                self.visualizer.clean_obstacles()
            if event.type == KEYDOWN and event.key == K_m:
                if self.run_mode == Runmode.BUILD:  # it is not possible to switch from sim to build mode
                    self.run_mode = Runmode.SIM
                    self.visualizer.set_run_mode(self.run_mode)
                log.error("Switched runmode to simulation")
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()


if __name__ == '__main__':
    VacuumCleanerSim().start_simulation()
