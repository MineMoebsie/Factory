from perlin_noise import PerlinNoise
import numpy as np
import random as r

def generate_grid(width_grid, height_grid, default = False, plot = False):
    noise = PerlinNoise(octaves=15, seed=1)
            
    grid = np.zeros((height_grid,width_grid),dtype='int')
    grid_rotation = np.zeros((height_grid,width_grid),dtype='int') # 0 up, 1 right, 2 down, 3 left

    pic = [[noise([i/width_grid, j/height_grid]) for j in range(width_grid)] for i in range(height_grid)]
          
    grid_generation = pic
    for x in range(width_grid):
        for y in range(height_grid):
            grid_rotation[y, x] = r.randint(0,3)
            
            if pic[y][x] > -0.075:
                grid[y, x] = r.choice([10,11])
            elif pic[y][x] > -0.15:
                grid[y, x] = r.choice([23,24])
            else:
                grid[y,x] = r.choice([21,22])

    return grid, grid_rotation, grid_generation

with open("Data/Saves/another_world/grid.txt","w") as f:
    np.savetxt(f, generate_grid(500, 500)[0], fmt="%i")

with open("Data/Saves/another_world/grid_rotation.txt","w") as f:
    np.savetxt(f, generate_grid(500, 500)[1], fmt="%i")    