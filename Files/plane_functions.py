import pygame as pg
import numpy as np
import time as t
import random as r
import math

from Files.factory_functions import *

def generate_plane_list(grid, delivery_level):
    plane_list = []
    delivery_locations = np.where(grid==38)
    for i in range(delivery_level):
        plane_list.append(Plane(delivery_locations[1][0], delivery_locations[0][0], i))
    return plane_list

class Plane:
    def __init__(self, rx, ry, plane_num):
        self.rx = rx # grid location of where the delivery thing is
        self.ry = ry
        self.landing_strip_height = 80
        self.plane_num = plane_num # which plane (1-5) top to bottom
        self.x = self.rx * grid_size + 85
        self.y = self.ry * grid_size + self.landing_strip_height * self.plane_num - 10
        self.pic = "plane_1"

        self.width, self.height = scaled_pictures["plane_1"][1].get_size()

        self.shadow = pg.mask.from_surface(scaled_pictures["plane_1"][1])
        self.alpha_shadow_start = 130
        self.alpha_shadow_end = 60
        self.alpha_shadow = self.alpha_shadow_start
        self.prev_alpha_shadow = self.alpha_shadow
        self.shadow = self.shadow.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,self.alpha_shadow))
        self.shadow_scale = 1
        self.shadow_dist = 10
        self.shadow_dist_start = 10
        self.shadow_dist_end = 60

        self.direction = "right"

        self.in_flight = False # when "not touching ground", only when in "consistent" part
        self.taking_off = False # when taking off
        self.landing = False # when landing

        self.speed = 0 # how fast the plane is going
        self.flight_time = 0 # time in the graph used to accelerate "nicely"
        self.start_flight_time = 0 # when flight was started, as t.perf_counter()
        self.start_landing_time = 0
        self.x_flight = 0 # distance from new pos in flight to old pos at the "airport" thing
        self.goal = "" # can be taking off or landing. When landing, positioning should be precise to match up with the landing strips

        self.landing_dist = -1 # distance from place to land (where plane comes to standstill) to the point where it needs to start decelerating to line up with the landing spot
        self.start_landing_x = 0 # absolute point from whereon the plane needs to decelerate calculated with prev. var
        self.speed_plane_num_dict = {0: 1.6, 1: 1.2, 2: 0.75, 3: 1, 4: 1.4}
        # self.speed_plane_num_dict = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1}

        self.measure_dist_take_off = 0 # distance measured required to take off and reach constant speed
        self.measure_dist_point = 0 #point measured before take off where the plane is/was

        self.taxiing = False #taxiing to default pos
        self.start_taxiing_perf = 0

        self.particle_perf = 0 #t perf for when to start spawn particles

    def draw(self, screen, scrollx, scrolly, scale, scaled_pictures):
        if self.shadow_scale != scale or self.alpha_shadow != self.prev_alpha_shadow:
            self.shadow = pg.mask.from_surface(scaled_pictures["plane_1"][1])
            self.shadow = self.shadow.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,self.alpha_shadow))
            self.prev_alpha_shadow = self.alpha_shadow
        screen.blit(self.shadow, (self.x * scale + scrollx, (self.y + self.shadow_dist) * scale + scrolly))
        screen.blit(scaled_pictures[self.pic][1], (self.x * scale + scrollx, self.y * scale + scrolly))

    def update(self, dT, grid_wh, plane_particles):
        if self.in_flight:
            if self.taking_off:
                self.flight_time = t.perf_counter() - self.start_flight_time
                x = self.flight_time / 1.75
                if not x > 1:
                    if x < 0.5:
                        self.speed = 2 * x ** 2
                    else:
                        self.speed = 1 - math.pow(-2 * x + 2, 2) / 2

                    self.shadow_dist = (x**2 * (self.shadow_dist_end - self.shadow_dist_start)) + self.shadow_dist_start 
                    self.alpha_shadow = (x**2 * (self.alpha_shadow_end - self.alpha_shadow_start)) + self.alpha_shadow_start
                    if x > 0.1:
                        plane_particles.append([self.x, self.y + self.height / 2 - 10, self.speed * self.speed_plane_num_dict[self.plane_num] * dT, r.uniform(-1,1), 20])
                else:
                    self.speed = 1
                    self.taking_off = False
                    self.shadow_dist = self.shadow_dist_end

                    self.measure_dist_take_off = self.x - self.measure_dist_point

            if self.landing:
                self.flight_time = t.perf_counter() - self.start_landing_time
                x = self.flight_time / 1.75
                x = -x + 1
                if x > 0 and x < 1:
                    if x < 0.5:
                        self.speed = 2 * x ** 2
                    else:
                        self.speed = 1 - math.pow(-2 * x + 2, 2) / 2

                    self.shadow_dist = (x**4 * (self.shadow_dist_end - self.shadow_dist_start)) + self.shadow_dist_start  
                    self.alpha_shadow = (x**4 * (self.alpha_shadow_end - self.alpha_shadow_start)) + self.alpha_shadow_start 

                    if x > 0.1:
                        plane_particles.append([self.x, self.y + self.height / 2 - 10, self.speed * self.speed_plane_num_dict[self.plane_num] * dT, r.uniform(-1,1), 20])

                else:
                    self.in_flight = False
                    self.landing = True
                    self.taxiing = True
                    self.landing_dist = -1 #reset
                    self.start_taxiing_perf = t.perf_counter() + 3

            self.x = self.rx * grid_size + 85 + self.x_flight
            
            if not self.taking_off and not self.landing:
                self.shadow_dist = self.shadow_dist_end
                self.alpha_shadow = self.alpha_shadow_end
                self.speed = 1
                if self.goal == "landing":
                    self.landing_dist = self.measure_dist_take_off
                    point_to_land = self.rx * grid_size + 300 # target
                    self.start_landing_x = point_to_land - self.landing_dist

                    if self.x >= self.start_landing_x:
                        self.temp_x = self.x
                        self.landing = True
                        self.start_landing_time = t.perf_counter()
                        self.goal = ""
                
                if self.goal == "taking off":
                    if self.x > grid_wh * grid_size + 100:
                        self.goal = "landing"
                        self.x_flight = -5000
                        self.taking_off = False
                        self.landing = False

                if t.perf_counter() > self.particle_perf + 0.1:
                    plane_particles.append([self.x, self.y + self.height / 2 - 10, (self.speed * self.speed_plane_num_dict[self.plane_num] * dT) / 1.5, r.uniform(-1,1), r.randint(10, 20)])
                    self.particle_perf = t.perf_counter()
                
            self.speed *= self.speed_plane_num_dict[self.plane_num]
            self.x_flight += self.speed * dT
            self.x = self.rx * grid_size + 85 + self.x_flight

        elif (not self.in_flight) and self.taxiing:
            if self.start_taxiing_perf < t.perf_counter():
                self.landing = False
                self.x_flight -= 0.035 * dT 
                if self.x_flight < 0:
                    self.x_flight = 0
                    self.taxiing = False
                self.x = self.rx * grid_size + 85 + self.x_flight
            else:
                self.x = self.rx * grid_size + 85 + self.x_flight

        return plane_particles

def update_and_draw_plane_particles(screen, plane_particles, dT, scale, scrollx, scrolly):
    for i, particle in sorted(enumerate(plane_particles), reverse=True):
        particle_x = particle[0]
        particle_y = particle[1]
        particle_vx = particle[2]
        particle_vy = particle[3]
        particle_size = particle[4]

        if particle_size < 0.1:
            plane_particles.pop(i)

        particle[0] += particle_vx / 10 * dT
        particle[1] += particle_vy / 10 * dT

        particle[2] = particle_vx * 0.95
        particle[3] = particle_vy * 0.95

        particle[4] = particle_size * 0.97


        particle_surf = pg.Surface((particle_size, particle_size), pg.SRCALPHA)
        pg.draw.circle(particle_surf, (100, 100, 100  ), (particle_size / 2, particle_size / 2), particle_size / 2)
        particle_surf.set_alpha(200)
        screen.blit(particle_surf, (particle_x * scale + scrollx, particle_y * scale + scrolly))

    return plane_particles




