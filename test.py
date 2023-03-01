test = 2

if test == 1:
    import matplotlib.pyplot as plt
    from perlin_noise import PerlinNoise
    import numpy as np
    import random as r

    noise = PerlinNoise(octaves=20, seed=1)
    breedte, hoogte = 200,200
    pic = [[noise([i/breedte, j/hoogte]) for j in range(breedte)] for i in range(hoogte)]

    plt.imshow(pic)

    grid = np.zeros((breedte, hoogte))
    grid_rotation = np.zeros((breedte, hoogte))
    for x in range(breedte):
        for y in range(hoogte):
            grid_rotation[y, x] = r.randint(0,3)
            if pic[y][x] >= 0.2:
                grid[y, x] = r.choice([10, 11])
            else:
                grid[y, x] = r.choice([21, 22])

                
    plt.figure(2)
    plt.pcolormesh(grid)
    plt.colorbar()
    plt.show()

elif test == 2:
    import pygame
    import timeit
    import os

    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode((480, 320))
    screen.fill(pygame.Color('black'))

    image = pygame.image.load("Assets/35.png").convert_alpha()

    def test(image, angle):
        pygame.transform.rotate(image, angle)

    test_angle = []
    test_time = []
    test_time2 = []
    test_time3 = []

    for x in range(0, 360, 5):
        test_times = timeit.timeit("test(image, {})".format(x),
                                    setup="from __main__ import test, image",
                                    number=500)/500
        test_time2.append(timeit.timeit("test(image, {})".format(x),
                                    setup="from __main__ import test, image",
                                    number=50)/50)
        test_time3.append(timeit.timeit("test(image, {})".format(x),
                                    setup="from __main__ import test, image",
                                    number=10000)/10000)
        print(x, ":", test_times)
        test_time.append(test_times)
        test_angle.append(x)
    from matplotlib import pyplot as plt
    plt.plot(test_angle, test_time)
    plt.plot(test_angle, test_time2)
    plt.plot(test_angle, test_time3)
    plt.show()
