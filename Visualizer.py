import pygame
from pygame.locals import *

from events.EventType import EventType
from events.ObstacleDrawn import ObstacleDrawn
from events.RobotDrawn import RobotDrawn
from utils.Runmode import Runmode
from utils.colorUtils import *
from utils.confUtils import LOG as log
from utils.confUtils import CONF as conf


class Visualizer:
    def __init__(self, env, clock):
        pygame.init()
        w, h, _ = env.get_params()

        self.ticks = 0
        self.clock = clock
        self.run_mode = Runmode.BUILD

        self.screen = pygame.display.set_mode((w, h), DOUBLEBUF)
        self.screen.set_alpha(None)

        self.font = pygame.font.Font(None, 20)

        self.tile_group = pygame.sprite.Group()
        # self.tile_group.add(env.tiles)

        self.robot = None
        self.robot_group = pygame.sprite.Group()

        self.wall_group = pygame.sprite.Group()
        self.wall_group.add(env.walls)

        self.obstacle_group = pygame.sprite.Group()
        self.obstacle_group.add(env.obstacles)

        # --- Temp rectangle for placing new rectangles ---
        self.mouse_down = False
        self.start_point = None
        self.temp_rectangle = None
        self.new_rectangle = None

        # --- Temp robot tuple ---
        self.temp_robot = None

    def update(self, sim_events=None, pygame_events=None):
        if sim_events is not None and len(sim_events) != 0:
            self.handle_sim_events(sim_events)
        if pygame_events is not None:
            self.handle_pygame_events(pygame_events)

        if self.run_mode == Runmode.SIM:
            self.ticks = self.ticks + 1

        self.draw()

    def handle_pygame_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    x, y = pygame.mouse.get_pos()
                    diameter = conf["robot"]["diameter"]
                    self.temp_robot = (x, y, diameter)
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

    def handle_sim_events(self, events):
        for event in events:
            if event.type == EventType.OBSTACLE_ADDED:
                log.error("Add Obstacle")
                self.obstacle_group.add(event.new_obstacle)
            if event.type == EventType.ROBOT_PLACED:
                log.error("Robot placed")
                self.robot_group.add(event.placed_robot)
            if event.type == EventType.TILE_COVERED:
                self.tile_group.add(event.tile)

    def get_draw_events(self):
        events = []

        if self.new_rectangle is not None:
            ret = self.new_rectangle
            self.new_rectangle = None
            events.append(ObstacleDrawn(ret))

        if self.temp_robot is not None:
            events.append(RobotDrawn(self.temp_robot))
            self.temp_robot = None

        return events

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

    def draw_fps(self):
        if conf["debug"]["draw_fps"]:
            fps = self.font.render("FPS: " + str(int(self.clock.get_fps())), True, RED)
            self.screen.blit(fps, (20, 20))

    def draw_time(self):
        if conf["debug"]["draw_time"] and self.run_mode == Runmode.SIM:
            time = self.font.render("Time: " + str(self.ticks), True, RED)
            self.screen.blit(time, (20, 40))

    def draw(self):
        self.screen.fill(WHITE)

        self.tile_group.update()
        self.wall_group.update()
        self.obstacle_group.update()
        self.robot_group.update()

        self.tile_group.draw(self.screen)
        self.wall_group.draw(self.screen)
        self.obstacle_group.draw(self.screen)
        self.robot_group.draw(self.screen)

        self.draw_temp_rectangle()
        self.draw_fps()
        self.draw_time()

        pygame.display.flip()
