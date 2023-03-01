import numpy as np
import copy
import json

width_grid = 500
height_grid = 500
array_side_1 = []
for i in range(width_grid):
    array_side_1.append({}) 

grid_data = []
for i in range(height_grid):
    grid_data.append(copy.deepcopy(array_side_1))
grid_data = np.array(grid_data)

# with open("Data/Saves/another_world/grid_data.txt", "w") as f:
    # np.savetxt(f, grid_data, fmt="%s")

# json.dumps(grid_data)


json_obj = {"shape": grid_data.shape, "data": grid_data.flatten().tolist()}

with open("Data/Saves/another_world/grid_data.json", "w") as f:
    json.dump(json_obj, f)

file_data = json.loads(open("Data/Saves/another_world/grid_data.json").read())

my_arr = np.array(file_data["data"]).reshape(file_data["shape"])

print(my_arr)