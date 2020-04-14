import math
import numpy as np

class Vel(object):
    def __init__(self, array):
        self.x = array[0]
        self.y = array[1]
        self.array = array
        self.intent = np.linalg.norm(self.array)
        self.sin = self.y/self.intent
        self.cos = self.x/self.intent
        self.v_x = self.intent * self.cos
        self.v_y = self.intent * self.sin

    @property
    def get_tan(self):
        return self.y/self.x

    @property
    def is_zero(self):
        return False if self.intent else True

class Vel_util:

    @classmethod
    def vel_sub(self, v1, v2):
        new_v = Vel(v1.array - v2.array)
        flag = self.is_opposite_direction(v1, new_v)
        return new_v if flag else Vel(np.array((0, 0)))

    @classmethod
    # temporally for line move
    def is_opposite_direction(self, v1, v2):
        if v1.sin != 0:
            return True if v2.sin/v1.sin >= 0 else False
        elif v1.cos != 0:
            return True if v2.cos/v1.cos >=0 else False

class ball(object):
    rad = 0
    color = None
    float_pos = None
    pos = None
    def __init__(self,  rad=0, color=(0, 0, 0)):
        self.rad = rad
        self.color = color

    def change_pos(self, pos):
        self.float_pos = np.array(pos).astype(np.float64)
        self.pos = np.rint(self.float_pos).astype(np.int64)

    def move_ball(self, v):
        self.float_pos += v.array
        self.pos = np.rint(self.float_pos).astype(np.int64)

def get_tri_plist(p1, p2, tri_length=20):
        '''
        get tri points, p1 is begin pos, p2 is end pos
        :param p1, p2: numpy array(x, y)
        :return: plist[p1, p2, p3]
        '''
        v1 = p2 - p1
        if v1[1] != 0:
            v2_x = 1
            v2_y = - v1[0] / v1[1]
        else:
            v2_y = 1
            v2_x = - v1[1] / v1[0]
        v2 = np.array((v2_x, v2_y))
        tri_p1 = p2
        dist1 = np.linalg.norm(v1)
        dist2 = np.linalg.norm(v2)
        tri_p2 = tri_p1 - tri_length * v1 / dist1 + tri_length * v2 / dist2
        tri_p3 = tri_p1 - tri_length * v1 / dist1 - tri_length * v2 / dist2
        return [tri_p1.astype(np.int16), tri_p2.astype(np.int16), tri_p3.astype(np.int16)]


