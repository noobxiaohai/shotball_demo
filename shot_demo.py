# !/usr/bin/env python
import pygame
import math
import random
import time
from pygame.locals import *
from sys import exit
import numpy as np

class shot_demo(object):
    current_stat = None
    GATE_WIDTH = 160
    GATE_HEIGHT = 80
    GATE_POS = 0
    ball_rad = 15
    ball_color = (0, 0, 0)
    background = None
    lunch_begin = None
    lunch_end = 0
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480), 0, 32)
        pygame.display.set_caption("shot")
        self.ball = ball()
        self.reset_backgound()
        self.current_stat = self.set_ball_stat

    def reset_backgound(self):
        background_color = (0, 255, 0)
        self.background = pygame.Surface((640, 480))
        self.background.fill(background_color, (0, 0, 640, 480))
        self.set_gate()
        self.draw_gate()

    def set_gate(self):
        self.GATE_POS = (random.randint(0, 640 - self.GATE_WIDTH), 0)

    def draw_gate(self):
        gate_color = (255, 255, 255)
        gate_rec = Rect(self.GATE_POS[0], 0, self.GATE_WIDTH, self.GATE_HEIGHT)
        pygame.draw.rect(self.background, (255, 255, 255), gate_rec)
        self.background.fill(gate_color, (self.GATE_POS, (self.GATE_WIDTH, self.GATE_HEIGHT)))

    def main_loop(self):
        clock = pygame.time.Clock()
        while True:
            time_pssed = clock.tick(10)
            self.screen.blit(self.background, (0, 0))
            even = pygame.event.poll()
            if even.type == QUIT:
                exit()
            self.current_stat(even)
            pygame.display.update()

    def set_ball_stat(self, even):
        mouse_pos = pygame.mouse.get_pos()
        self.ball.change_pos(mouse_pos)
        pygame.draw.circle(self.screen, self.ball_color, self.ball.pos, self.ball_rad)
        if even.type == MOUSEBUTTONDOWN:
            pos = even.pos
            print('set ball:', pos)
            pygame.draw.circle(self.background, self.ball_color, self.ball.pos, self.ball_rad)
            self.current_stat = self.choose_lunch_stat

    def choose_lunch_stat(self, even):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(self.screen, (255, 0, 0), mouse_pos, int(self.ball_rad/2))
        if even.type == MOUSEBUTTONDOWN:
            # draw begin lunch position
            self.lunch_begin = np.array(mouse_pos)
            pygame.draw.circle(self.background, (255, 0, 0), mouse_pos, int(self.ball_rad/2))
            self.current_stat = self.ready_lunch_stat

    def ready_lunch_stat(self, even):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.polygon(self.screen, (255, 0, 0), [(50,50), (100,100), (50, 100)])
        pygame.draw.line(self.screen, (255, 0, 0), self.lunch_begin, mouse_pos)
        tri_p1 = np.array(mouse_pos)
        v1 = tri_p1 - self.lunch_begin
        dist = np.linalg.norm(v1)
        v2 = v1.copy()
        v2[0] = - v2[0]
        tri_length = 50

        if dist != 0:
            tri_p2 = tri_p1 - tri_length * v1/dist + tri_length * v2/dist
            tri_p3 = tri_p1 - tri_length * v1/dist - tri_length * v2/dist
            print('v', v1, v2)
            print(self.lunch_begin, tri_p1, tri_p2, tri_p3)
            pygame.draw.polygon(self.screen, (255, 0, 0), [tri_p1, tri_p2, tri_p3])


    def moving_stat(self):
        while True:
            for even in pygame.event.get():
                if even.type == QUIT:
                    exit()
        pass

class ball(object):
    rad = 0
    color = None
    pos = None
    def __init__(self,  rad=0, color=(0, 0, 0)):
        self.rad = rad
        self.color = color

    def change_pos(self, pos):
        self.pos = pos

if __name__ == '__main__':
    dm = shot_demo()
    dm.main_loop()

