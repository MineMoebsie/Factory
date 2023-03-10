def convert_json(tile_info):
    tile_names = {}
    tile_des = {} # tile descriptions
    blocks_index = {}
    b_prices = {}
    big_tiles = [] # tile numbers of tile sizes > 2
    placed_on_only = {} # which tiles it can be placed on. Empty list by default
    cannot_place_on = {}
    ground_blocks = [] 

    for block in tile_info.keys():
        if block != "ground_blocks":
            tile_names[int(block)] = tile_info[block]['name']
            tile_des[int(block)] = tile_info[block]['description']
            blocks_index[int(block)] = tile_info[block]['size']
            if tile_info[block]['size'] > 1:
                big_tiles.append(int(block))
            placed_on_only[int(block)] = tile_info[block]['placed_on_only'] if 'placed_on_only' in tile_info[block] else []
            cannot_place_on[int(block)] = tile_info[block]['cannot_place_on'] if 'cannot_place_on' in tile_info[block] else []


            b_prices[int(block)] = tile_info[block]['price'] if 'price' in tile_info[block] else {}
        else:
            ground_blocks = tile_info['ground_blocks']

    return tile_names, tile_des, blocks_index, b_prices, big_tiles, placed_on_only, cannot_place_on, ground_blocks