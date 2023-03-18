import numpy

noise = numpy.random.normal(0, 1, 100)

grid = numpy.zeros((10,10))
for x in range(10):
    for y in range(10):
        grid[y, x] = noise[y * 10 + x]

from matplotlib import pyplot as plt
plt.figure(1)
plt.pcolormesh(grid)
plt.colorbar()
plt.show()