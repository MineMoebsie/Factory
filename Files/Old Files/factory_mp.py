import multiprocessing
import numpy as np

def _grid_function(coords):
    x, y, g_grid, g_grid_rotation, g_scale, g_scrollx, g_scrolly, g_grid_size = coords
    built = g_grid[y, x]
    orientation = g_grid_rotation[y, x]
    x_grid_scale = round(x * g_grid_size * g_scale) + g_scrollx
    y_grid_scale = round(y * g_grid_size * g_scale) + g_scrolly
    if built in [10, 11, 21, 22]:  # ground
        image = ["picture_" + str(built), orientation]
        loc = [(x_grid_scale, y_grid_scale)]
    else:
        image = []
        loc = []
    return [image, loc]



def teken_grid_mp_core(scherm, grid, grid_rotation, selected_x, selected_y, move, scrollx, scrolly, screen_size, 
                render_distance, storage, scale, scaled_pictures, blocks_index, grid_cables, brush, angle,grid_data, grid_size 
                ):

    x = np.arange(max(0, int(abs(scrollx) / (grid_size * scale))), min(grid.shape[1],
                                                                        int(int((abs(scrollx) + screen_size[0]) / (
                                                                                grid_size * scale) + 1) + np.ceil(
                                                                            (abs(scrollx) + screen_size[0]) / (
                                                                                        grid_size * scale) % 1))))
    y = np.arange(max(0, int(abs(scrolly) / (grid_size * scale))), min(grid.shape[0],
                                                                            int(int((abs(scrolly) + screen_size[1]) / (
                                                                                    grid_size * scale) + 1) + np.ceil(
                                                                                (abs(scrolly) + screen_size[1]) / (
                                                                                        grid_size * scale) % 1))))
    x = np.array([x for i in range(y.shape[0])])
    y = np.array([y for i in range(x.shape[1])]).T.flatten()
    x = x.flatten()
    coords = [[x[i], y[i]] for i in range(x.shape[0])]
    for i in range(len(coords)):
        coords[i].append(grid)
        coords[i].append(grid_rotation)
        coords[i].append(scale)
        coords[i].append(scrollx)
        coords[i].append(scrolly)
        coords[i].append(grid_size)
    with multiprocessing.Pool(3) as p:
        res = p.map(_grid_function, coords)
    return res