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

    @classmethod
    def vel_sub(self, v1, v2):
        array = v1.array - v2.array
        print('vel:', v2.array, v1.array, array)
        return Vel(array)

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


