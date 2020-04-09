import math
import numpy as np
class Vector(object):
    def __init__(self, *args):
        x = args[0]
        y = args[1]

    def sub(self):
        pass

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
