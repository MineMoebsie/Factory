import pygame as pg
import numpy as np
import time as t
import random as r

from Files.factory_functions import *

def generate_plane_list(grid, delivery_level):
    plane_list = []
    delivery_locations = np.where(grid==38)
    print(delivery_locations)
    plane_list.append(Plane(delivery_locations[1][0], delivery_locations[0][0], 1))
    return plane_list

class Plane:
    def __init__(self, rx, ry, plane_num):
        self.rx = rx # grid location of where the delivery thing is
        self.ry = ry
        self.landing_strip_height = 50
        self.plane_num = plane_num # which plane (1-5) top to bottom
        self.pic = "plane_1"

    def draw(self, screen, scrollx, scrolly, scale, scaled_pictures):
        screen.blit(scaled_pictures[self.pic][3], (self.rx * grid_size * scale + scrollx, (self.ry * grid_size + self.landing_strip_height * self.plane_num) * scale + scrolly))