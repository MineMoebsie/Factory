import random as r
import os

def convert_json(tile_info):
    tile_names = {}
    tile_des = {} # tile descriptions
    blocks_index = {}
    b_prices = {}
    big_tiles = [] # tile numbers of tile sizes > 2
    placed_on_only = {} # which tiles it can be placed on. Empty list by default
    cannot_place_on = {}
    ground_blocks = [] 
    spawn_time = {}
    spawn_items = {}
    spawn_perf_counters = {}
    strict_placement_tiles = [] # which tiles require strict placement (only allows 1 type of ground block)
    can_spawn_items = [] # block numbers of which can spawn items

    for block in tile_info.keys():
        if block != "ground_blocks":
            tile_names[int(block)] = tile_info[block]['name']
            tile_des[int(block)] = tile_info[block]['description']
            blocks_index[int(block)] = tile_info[block]['size']
            if tile_info[block]['size'] > 1:
                big_tiles.append(int(block))
            placed_on_only[int(block)] = tile_info[block]['placed_on_only'] if 'placed_on_only' in tile_info[block] else []
            cannot_place_on[int(block)] = tile_info[block]['cannot_place_on'] if 'cannot_place_on' in tile_info[block] else []
            spawn_time[int(block)] = tile_info[block]['spawn_time'] if 'spawn_time' in tile_info[block] else -1
            spawn_items[int(block)] = tile_info[block]['spawn_items'] if 'spawn_items' in tile_info[block] else []
            b_prices[int(block)] = tile_info[block]['price'] if 'price' in tile_info[block] else {}
            if 'strict_placement' in tile_info[block] and tile_info[block]['strict_placement']:
                strict_placement_tiles.append(int(block)) 
            if "spawn_time" in tile_info[block] and "spawn_items" in tile_info[block]:
                can_spawn_items.append(int(block))
        else:
            ground_blocks = tile_info['ground_blocks']

    for time in spawn_time.values():
        spawn_perf_counters[time] = -1
    
    return tile_names, tile_des, blocks_index, b_prices, big_tiles, placed_on_only, cannot_place_on, ground_blocks, spawn_time, spawn_items, spawn_perf_counters, strict_placement_tiles, can_spawn_items

def convert_item_info(item_info):
    item_names = {} #should be {0: ["potato", "potatoes"] etc..}
    for item in item_info.keys():
        item_names[int(item)] = item_info[item]["name"]

    return item_names

def load_deliver_list(world_path):
    fpath = "Data/Saves/"+world_path+"deliver_list.txt"
    if os.path.isfile(fpath):
        with open(fpath, "r") as f:
            to_deliver_list = eval(f.read())
            delivery_level = 1
            for delivery in to_deliver_list:
                if delivery is not None:
                    delivery_level += 1
            return to_deliver_list, delivery_level
    else:
        return [[],[],None,[],[]], 1

def generate_block(x, y, grid, grid_rotation, grid_generation, grid_generation_features):
        grid_rotation[y, x] = int(grid_generation[y][x] * 1000) % 4
                
        if grid_generation[y][x] > -0.075:
            grid[y, x] = r.choice([10,11])
        elif grid_generation[y][x] > -0.15:
            grid[y, x] = r.choice([23,24])
        elif grid_generation[y][x] > -0.425:
            grid[y,x] = r.choice([21,22])
        else:
            grid[y,x] = r.choice([25, 26])

        if grid_generation_features[y][x] < -0.3:
            if grid_generation[y][x] < -0.125:
                if grid_generation[y][x] > -0.15:
                    grid[y,x] = r.choice([27, 28])
                else:
                    grid[y,x] = r.choice([29, 30])
        
        return grid, grid_rotation