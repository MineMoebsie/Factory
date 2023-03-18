import pygame as pg
import numpy as np
pg.init()
screen = pg.display.set_mode((600,600),pg.RESIZABLE|pg.DOUBLEBUF)
playing = True
pg.display.set_caption("template")
clock = pg.time.Clock()

class Orbit:
    def __init__(self, x, y):
        self.deg_rotation = 0
        self.x = x
        self.y = y
        self.center = [200 + x, 200 + y]
        self.dist_to_center = 50

    def draw(self, screen):
        pg.draw.circle(screen, (255,255,255), self.center, 10)


        x, y = self.center
        x += np.cos(self.deg_rotation) * self.dist_to_center
        y += np.sin(self.deg_rotation) * self.dist_to_center

        pg.draw.circle(screen, (255,255,255), center=(x,y), radius= 5)
        self.deg_rotation += 0.1


orbit = Orbit(50,50)
while playing:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            playing = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                playing = False
        pg.event.pump()

    screen.fill((0,0,0))
    orbit.draw(screen)
    pg.display.flip()
    clock.tick(60)

pg.quit()
