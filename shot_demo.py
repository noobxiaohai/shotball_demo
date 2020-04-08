# !/usr/bin/env python
import pygame
import math
import random
import time
from pygame.locals import *
from sys import exit

class shot_demo(object):
    current_statu = None
    GATE_WIDTH = 160
    GATE_HEIGHT = 80
    GATE_POS = 0
    ball_rad = 15
    ball_color = (0, 0, 0)
    background = None

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
        while True:
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
            self.current_stat = self.lunch_stat(even)

    def lunch_stat(self, even):

        pass


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

