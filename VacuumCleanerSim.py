import pygame
import sys

from pygame.locals import *

from RoomEnvironment import RoomEnvironment
from Visualizer import Visualizer
from algorithm.RandomBounceWalkAlgorithm import RandomBounceWalkAlgorithm
from algorithm.SWalkAlgorithm import SWalkAlgorithm
from algorithm.SpiralWalkAlgorithm import SpiralWalkAlgorithm
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
        default_obstacles, default_robot = self.get_default_environment()
        self.environment = RoomEnvironment(env_conf["width"], env_conf["height"], tile_size, default_obstacles, default_robot)
        self.visualizer = Visualizer(self.environment, self.clock, self.environment.initial_events)
        self.algorithms = {"random": RandomBounceWalkAlgorithm(), "spiral": SpiralWalkAlgorithm(), "swalk": SWalkAlgorithm()}

        self.algorithm = self.algorithms[self.get_algorithm_name()]

    def start_simulation(self):
        log.info("Start simulation")
        while True:
            self.clock.tick(self.fps)
            pygame_events = pygame.event.get()
            self.handle_pygame_events(pygame_events)

            new_events = []
            if self.run_mode == Runmode.BUILD:
                draw_events = self.visualizer.get_draw_events()
                env_events = self.environment.update(draw_events)
                new_events.extend(env_events)

                self.visualizer.update(pygame_events=pygame_events, sim_events=new_events)

            elif self.run_mode == Runmode.SIM:
                # get configuration change events from algorithm. It does not affect the environment directly
                configuration_events = self.algorithm.update(self.environment.obstacles, self.environment.robot)
                new_events.extend(configuration_events)

                # apply configuration change event to the environment
                # and retrieve environment changes like covered tiles
                environment_events = self.environment.update(configuration_events)
                new_events.extend(environment_events)

                # update the visualizer with all new events
                self.visualizer.update(pygame_events=pygame_events, sim_events=new_events)

            # save all events into the event stream. this could be useful for re-simulating ...
            self.event_stream.append(new_events)

    def handle_pygame_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.visualizer.exit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_c:
                log.info("Clear obstacles")
                self.environment.clear_obstacles()
                self.visualizer.clean_obstacles()
            if event.type == KEYDOWN and event.key == K_m:
                if self.run_mode == Runmode.BUILD:  # it is not possible to switch from sim to build mode
                    self.run_mode = Runmode.SIM
                    self.visualizer.set_run_mode(self.run_mode)
                    self.visualizer.set_tile_count(self.environment.get_tile_count())
                    log.info("Switched run mode to simulation")
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.visualizer.exit()
                sys.exit()

    def get_algorithm_name(self):
        if len(sys.argv) > 1:
            return sys.argv[1]
        else:
            return conf["simulation"]["default_algorithm"]

    def get_default_environment(self):
        if len(sys.argv) > 2:
            default_index = sys.argv[2]
            default_conf = conf["environment"]["defaults"]
            if default_index in default_conf:
                return default_conf[default_index].get("obstacles", None), default_conf[default_index].get("robot", None)

        return None, None


if __name__ == '__main__':
    VacuumCleanerSim().start_simulation()
