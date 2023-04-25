import pygame as pg
import time as t
import random as r
import pdb
import numpy as np

from Files.factory_functions import *

with open("Data/recipes.json") as f:
    recipes = json.load(f)

def update_locations(grid, spawn_items):
    locations = np.array([])
    loc_grid = grid

    for item in spawn_items:
        if spawn_items[item] != []:
            loc_grid = np.where(loc_grid == int(item), -1, loc_grid)
    locations = np.where(loc_grid == -1)

    # loc_grid = np.where(loc_grid == 12, 13, loc_grid)  # transform all 13 into 14
    # loc13 = np.where(loc_grid == 13, 14, loc_grid)  # transform all 14 (and 13) into 15
    # loc14 = np.where(loc13 == 14, 16, loc_grid)
    # loc16 = np.where(loc14 == 16, 33, loc_grid)
    # loc33 = np.where(loc16 == 33, 34, loc_grid)
    # loc34 = np.where(loc33 == 34, 35, loc_grid)
    # locations = np.where(loc34 == 35)

    crafting_locations = np.where(grid == 15)

    cargo_spawn_locations = np.where(grid == 16)
    cargo_locations = np.where(grid == 17)
    return locations,crafting_locations,cargo_locations,cargo_spawn_locations

def generate_append_per_spawn(grid, spawn_time, spawn_items, locations, blocks_index):
    #blocks_index is for tile size
    append_per_spawn = {} # for ex.: key 1 corresponds to all the items that spawn in 1 second interval etc.
    # example of keys:
    '''
    append_per_spawn = {1: [{"spawn":[1,2,3], "loc": [[10,10], [11,10], [12,10]]}], 2: [], 3: [], 4: [], etc...}
    '''
    spawnable_tiles = [1]
    world_height, world_width = grid.shape
    for i in spawn_time.values(): # fill the dict with empty list keys for all the used seconds
        append_per_spawn[i] = []

    for loc in range(len(locations[0])):
        x = locations[1][loc]
        y = locations[0][loc]
        block = grid[y, x]
        size = blocks_index[block]
        spawn_dict = {"spawn": [], "loc": []}
        
        #items are spawned directly next to the spawner, so not diagonally, only directly adjacent
        #check for spawnable spots in the locations:

        #check spawn spots above/below block
        for x_check in range(x, x+size):
            if y > 0 and grid[y-1, x_check] in spawnable_tiles:
                spawn_dict["loc"].append([y-1, x_check])
            if y < world_height and grid[y+size, x_check] in spawnable_tiles:
                spawn_dict["loc"].append([y+size, x_check])
        #check spawn spots next to block (left/right)
        for y_check in range(y, y+size):
            if x > 0 and grid[ y_check, x-1] in spawnable_tiles:
                spawn_dict["loc"].append([y_check, x-1])
            if x < world_width and grid[y_check, x+size] in spawnable_tiles:
                spawn_dict["loc"].append([y_check, x+size])
        
        spawn_dict['spawn'] = spawn_items[block]

        append_per_spawn[spawn_time[block]].append(spawn_dict)

    return append_per_spawn

def spawn_pregenerated_items(items_list, craft_data, append_per_spawn, spawn_perf_counters, cargo_locations, cargo_spawn_locations, spawn_time, cargo_spawn_perf):
    for time in append_per_spawn.keys():
        if time != -1:
            if t.perf_counter() > spawn_perf_counters[time] + time: # spawn items
                for item in append_per_spawn[time]:
                    if len(item["loc"]) > 0:
                        spawn_loc = r.choice(item["loc"])
                        spawn_item = r.choice(item["spawn"])
                        items_list.append(Item(spawn_loc[1] * grid_size + int(grid_size / 2), spawn_loc[0] * grid_size + int(grid_size / 2), spawn_item))
                    
                spawn_perf_counters[time] = t.perf_counter()

    if cargo_spawn_perf + 5 < t.perf_counter():
        cargo_spawn_perf = t.perf_counter()
        for ind in range(len(cargo_spawn_locations[0])):
            x = cargo_spawn_locations[1][ind]
            y = cargo_spawn_locations[0][ind]

            items_dict = {}#dict for items inside of cargo item
            items_dict = craft_data[y, x]
            craft_data[y, x] = {} # delete items (else: infinite resources exploit...)

            items_list.append(Cargo((x+1) * grid_size + int(grid_size / 2), (y+1) * grid_size + int(grid_size / 2), items_dict))

    return items_list, craft_data, cargo_spawn_perf

def craft_items(crafting_locations, craft_data, grid, grid_rotation, grid_data, items_list, grid_size=grid_size):
    locations = crafting_locations
    for ind in range(len(locations[1])):
        x = locations[1][ind]
        y = locations[0][ind]
        if str(grid_data[y, x]["craft_recipe"]) != "0":
            #all the required "ingredients" for craft recipe required
            requirements = {}
            for item in recipes[str(grid_data[y, x]["craft_recipe"])]["recipe"]: #loops through for ex.: [1,2,2]
                if not item in requirements: 
                    requirements[item] = 1 
                else:
                    requirements[item] += 1
            
            can_craft = True # if it can craft the item
            for req in requirements.keys():
                if not (str(req) in list(craft_data[y, x].keys())):
                    can_craft = False
                elif requirements[req] > craft_data[y, x][str(req)]:
                    can_craft = False
        
            if can_craft:
                # subtract items from craft_data
                for req in requirements:
                    craft_data[y, x][str(req)] -= requirements[req]

                # spawn crafted item
                spawnx = -1
                spawny = -1
                if grid_rotation[y, x] == 0:
                    spawnx = (x + int(0.5 * 3 - 0.5)) * grid_size + int(grid_size / 2)
                    spawny = (y + 3) * grid_size + int(grid_size / 10)
                elif grid_rotation[y, x] == 1:
                    spawnx = x * grid_size - int(grid_size / 10)
                    spawny = (y + int(0.5 * 3 - 0.5)) * grid_size + int(grid_size / 2)
                elif grid_rotation[y, x] == 2:
                    spawnx = (x + int(0.5 * 3 - 0.5)) * grid_size + int(grid_size / 2)
                    spawny = y * grid_size - int(grid_size / 10)
                elif grid_rotation[y, x] == 3:
                    spawnx = (x + 3) * grid_size + int(grid_size / 10)
                    spawny = (y + int(0.5 * 3 - 0.5)) * grid_size + int(grid_size / 2)
                items_list.append(Item(int(spawnx), int(spawny), int(grid_data[y, x]["craft_recipe"])))

    return craft_data, items_list

def spawn_cargo(cargo_locations,grid,cargo_data,items_list, spawn_cooldown, grid_size=grid_size):
    loc_17 = cargo_locations
    set_spawn_cooldown = False
    for ind in range(len(loc_17[0])):
        x = loc_17[1][ind]
        y = loc_17[0][ind]

        if len(cargo_data[y, x]) > 0: # items to spawn
            spawn_spots = [] #places to spawn
            if grid[y-1,x+1] == 1:
                spawn_spots.append([max(0,y-1),x+1])
            if grid[y+1,x+3] == 1:
                spawn_spots.append([y+1,x+3])
            if grid[y+3,x+1] == 1:
                spawn_spots.append([y+3,x+1])
            if grid[y+1,x-1] == 1:
                spawn_spots.append([y+1,max(0,x-1)])
                
            if len(spawn_spots) > 0: # no spawn spots, not spawning!
                if (sum(cargo_data[y, x].values()) > 25) or (spawn_cooldown < t.perf_counter() - 0.5): #if a lot of items
                    set_spawn_cooldown = True
                    spawn_y, spawn_x = r.choice(spawn_spots)
                    dict_keys = list(cargo_data[y, x].keys())
                    spawn_type = r.choice(dict_keys)
                    spawn_type = int(spawn_type)
                    items_list.append(
                        Item(spawn_x * grid_size + int(grid_size / 2), spawn_y * grid_size + int(grid_size / 2), spawn_type))

                    spawn_type = str(spawn_type)
                    
                    if cargo_data[y, x][spawn_type] > 0:
                        cargo_data[y, x][spawn_type] -= 1
                    else:
                        del cargo_data[y,x][spawn_type]
            else:
                print("No spawn spots!")
    
    if set_spawn_cooldown:
        spawn_cooldown = t.perf_counter()

    return items_list, cargo_data, spawn_cooldown