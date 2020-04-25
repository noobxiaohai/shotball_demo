# !/usr/bin/env python
import pygame
import math
import random
import time
from pygame.locals import *
from sys import exit
import numpy as np
from Util import get_tri_plist, Vel, ball, Vel_util, color_dic

class shot_demo(object):
    # default value
    GATE_WIDTH = 160
    GATE_HEIGHT = 80
    GATE_POS = 0
    SCREEN_SIZE_X = 640
    SCREEN_SIZE_Y = 480
    SCREEN_SIZE = (SCREEN_SIZE_X, SCREEN_SIZE_Y)
    FINISH_STOP_FRAME = 200
    FONT = None
    FONT_COLOR = color_dic['black']
    SCORE_FONT_SIZE = 24
    SCOREBOARD_SIZE = (128, 96)
    RESULT_STR = {0: 'GOAL!!!', 1: 'OUT RANGE...', 2: 'MISS THE SHOT...'}

    SCORE = 0
    current_stat = None
    ball_rad = 15
    ball_color = color_dic['black']
    background = None
    lunch_begin = None
    lunch_end = None
    ball = None
    lunch_v = None
    current_v = None
    V_FIC_SCALE = 15 # todo: add quility and gravity into physical system
    count_frame = FINISH_STOP_FRAME
    round_result = 0 # 0 is win, 1 is out range, 2 is miss shot
    screen_rect = None

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, 0, 32)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("shot")
        self.new_round()

    def main_loop(self):
        clock = pygame.time.Clock()
        while True:
            time_pssed = clock.tick(20)
            self.screen.blit(self.background, (0, 0))
            self.set_scoreboard()
            even = pygame.event.poll()
            if even.type == QUIT:
                exit()
            self.current_stat(even)
            pygame.display.update()

    def set_scoreboard(self):
        font = pygame.font.SysFont('my_font.ttf', self.SCORE_FONT_SIZE)
        score_str = 'Now score: %d'%self.SCORE
        score_surface = font.render(score_str, True, self.FONT_COLOR)

        self.screen.blit(score_surface, (self.SCREEN_SIZE[0] - self.SCOREBOARD_SIZE[0], self.SCREEN_SIZE[1] - self.SCOREBOARD_SIZE[1]))

    def new_round(self):
        background_color = color_dic['green']
        self.background = pygame.Surface((self.SCREEN_SIZE_X, self.SCREEN_SIZE_Y))
        self.background.fill(background_color, (0, 0, self.SCREEN_SIZE_X, self.SCREEN_SIZE_Y))
        self.set_gate()
        self.draw_gate()
        self.lunch_begin = None
        self.lunch_end = None
        self.ball = ball(self.ball_rad, self.ball_color)
        self.lunch_v = None
        self.current_v = None
        self.current_stat = self.set_ball_stat
        print('begin new round.')
        print('current gate pos is', self.GATE_POS)

    def set_gate(self):
        self.GATE_POS = (random.randint(0, self.SCREEN_SIZE_X - self.GATE_WIDTH), 0)

    def draw_gate(self):
        gate_color = color_dic['white']
        self.background.fill(gate_color, (self.GATE_POS, (self.GATE_WIDTH, self.GATE_HEIGHT)))

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
            if not Vel_util.is_in_ball_rad(self.lunch_end, self.ball):
                self.current_v = Vel(np.array((0, 0)))
                self.current_stat = self.lunch_stat
            else:
                self.begin_v = Vel((self.lunch_end - self.lunch_begin))
                dv_x = self.begin_v.cos * self.V_FIC_SCALE
                dv_y = self.begin_v.sin * self.V_FIC_SCALE
                self.v_firction = Vel(np.array((dv_x, dv_y)))
                self.current_v = self.begin_v
                self.current_stat = self.lunch_stat

    def lunch_stat(self, even):
        if self.check_result():
            self.current_stat = self.finish_stat
            return
        self.ball.move_ball(self.current_v)
        pygame.draw.circle(self.screen, self.ball.color, self.ball.pos, self.ball.rad)
        self.current_v = Vel_util.vel_sub(self.current_v, self.v_firction)
        # print(self.ball.pos)


    def finish_stat(self, even):
        self.count_frame -= 1
        self.ball.move_ball(self.current_v)
        pygame.draw.circle(self.screen, self.ball.color, self.ball.pos, self.ball.rad)
        self.draw_result_font()

        if self.count_frame <= 0:
            self.count_frame = self.FINISH_STOP_FRAME
            self.new_round()
            return

        if even.type == MOUSEBUTTONDOWN:
            self.count_frame = self.FINISH_STOP_FRAME
            self.new_round()
            return

    def draw_result_font(self):
        font = pygame.font.SysFont('my_font.ttf', self.SCORE_FONT_SIZE)
        font_str = self.RESULT_STR[self.round_result]
        font_sf = font.render(font_str, True, self.FONT_COLOR)
        font_rect = font_sf.get_rect()
        s_mid = self.screen_rect.center
        f_mid = font_rect.center
        set_pos = (s_mid[0] - f_mid[0], s_mid[0] - f_mid[0])
        self.screen.blit(font_sf, set_pos)

    def check_result(self):
        if self.check_our_range() or self.check_goal() or self.check_miss_shot():
            return True
        return False

    def check_our_range(self):
        ball_x = self.ball.pos[0]
        ball_y = self.ball.pos[1]
        if ball_x < 0 or ball_x > self.SCREEN_SIZE_X or ball_y < 0 or ball_y > self.SCREEN_SIZE_Y:
            self.round_result = 1
            print('OUT RANGE...')
            return True

        if (ball_x in range(0, self.GATE_POS[0]) or ball_x in range(self.GATE_POS[0] + self.GATE_WIDTH, self.SCREEN_SIZE_Y))\
            and ball_y in range(0, self.GATE_HEIGHT):
            self.round_result = 1
            print('OUT RANGE...')
            return True
        return False

    def check_goal(self):
        ball_x = self.ball.pos[0]
        ball_y = self.ball.pos[1]
        if ball_x in range(self.GATE_POS[0], self.GATE_POS[0] + self.GATE_WIDTH) and \
            ball_y in range(0, self.GATE_HEIGHT):
            self.round_result = 0
            self.add_score()
            return True
        return False

    def check_miss_shot(self):
        if self.current_v.is_zero:
            self.round_result = 2
            print('MISS THE SHOT...')
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

