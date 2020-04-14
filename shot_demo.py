# !/usr/bin/env python
import pygame
import math
import random
import time
from pygame.locals import *
from sys import exit
import numpy as np
from Util import get_tri_plist, Vel, ball, Vel_util

class shot_demo(object):
    current_stat = None
    GATE_WIDTH = 160
    GATE_HEIGHT = 80
    GATE_POS = 0
    SCORE = 0
    ball_rad = 15
    ball_color = (0, 0, 0)
    background = None
    lunch_begin = None
    lunch_end = None
    ball = None
    lunch_v = None
    current_v = None
    V_FIC_SCALE = 15 # todo: add quility and gravity into physical system
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480), 0, 32)
        pygame.display.set_caption("shot")
        self.new_round()

    def new_round(self):
        background_color = (0, 255, 0)
        self.background = pygame.Surface((640, 480))
        self.background.fill(background_color, (0, 0, 640, 480))
        self.set_gate()
        self.draw_gate()
        self.lunch_begin = None
        self.lunch_end = None
        self.ball = ball(self.ball_rad, self.ball_color)
        self.lunch_v = None
        self.current_v = None
        self.current_stat = self.set_ball_stat

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
            time_pssed = clock.tick(20)
            self.screen.blit(self.background, (0, 0))
            even = pygame.event.poll()
            if even.type == QUIT:
                exit()
            self.current_stat(even)
            pygame.display.update()

    def set_ball_stat(self, even):
        mouse_pos = pygame.mouse.get_pos()
        self.ball.change_pos(mouse_pos)
        pygame.draw.circle(self.screen, self.ball.color, self.ball.pos, self.ball.rad)
        if even.type == MOUSEBUTTONDOWN:
            pos = even.pos
            print('set ball:', pos)
            pygame.draw.circle(self.screen, self.ball.color, self.ball.pos, self.ball.rad)
            self.current_stat = self.choose_lunch_stat

    def choose_lunch_stat(self, even):
        pygame.draw.circle(self.screen, self.ball.color, self.ball.pos, self.ball.rad)
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(self.screen, (255, 0, 0), mouse_pos, int(self.ball_rad/2))
        if even.type == MOUSEBUTTONDOWN:
            # draw begin lunch position
            self.lunch_begin = np.array(mouse_pos)
            pygame.draw.circle(self.screen, (255, 0, 0), self.lunch_begin, int(self.ball_rad/2))
            self.current_stat = self.ready_lunch_stat

    def ready_lunch_stat(self, even):
        pygame.draw.circle(self.screen, self.ball.color, self.ball.pos, self.ball.rad)
        pygame.draw.circle(self.screen, (255, 0, 0), self.lunch_begin, int(self.ball_rad / 2))
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(self.screen, (255, 0, 0), self.lunch_begin, mouse_pos)
        p1 = np.array(mouse_pos)
        plist = get_tri_plist(self.lunch_begin, p1)

        if p1[0] != 0 and p1[1] != 0:
            pygame.draw.polygon(self.screen, (255, 0, 0), plist)

        if even.type == MOUSEBUTTONDOWN:
            self.lunch_end = np.array(mouse_pos)
            self.begin_v = Vel((self.lunch_end - self.lunch_begin))
            dv_x = self.begin_v.cos * self.V_FIC_SCALE
            dv_y = self.begin_v.sin * self.V_FIC_SCALE
            self.v_firction = Vel(np.array((dv_x, dv_y)))
            self.current_v = self.begin_v
            self.current_stat = self.lunch_stat

    def lunch_stat(self, even):
        self.ball.move_ball(self.current_v)
        pygame.draw.circle(self.screen, self.ball.color, self.ball.pos, self.ball.rad)
        self.current_v = Vel_util.vel_sub(self.current_v, self.v_firction)
        # print(self.ball.pos)

        if self.check_goal():
            self.add_score()
            self.new_round()
            return

        if self.current_v.is_zero:
            print('MISSED SHOT.......')
            self.new_round()
            pass

    def check_goal(self):
        ball_x = self.ball.pos[0]
        ball_y = self.ball.pos[1]
        if ball_x in range(self.GATE_POS[0], self.GATE_POS[0] + self.GATE_WIDTH) and \
            ball_y in range(0, self.GATE_HEIGHT):
            return True
        return False

    def add_score(self):
        self.SCORE += 1
        print('GAOL!!!!!! SCORE %d' % self.SCORE)

    def background_mgr(self):
        pass

if __name__ == '__main__':
    dm = shot_demo()
    dm.main_loop()

