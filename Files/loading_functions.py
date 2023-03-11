def convert_json(tile_info):
    tile_names = {}
    tile_des = {} # tile descriptions
    blocks_index = {}
    b_prices = {}
    big_tiles = [] # tile numbers of tile sizes > 2

    for block in tile_info.keys():
        tile_names[int(block)] = tile_info[block]['name']
        tile_des[int(block)] = tile_info[block]['description']
        blocks_index[int(block)] = tile_info[block]['size']
        if tile_info[block]['size'] > 1:
            big_tiles.append(int(block))

        b_prices[int(block)] = tile_info[block]['price'] if 'price' in tile_info[block] else {}


    return tile_names, tile_des, blocks_index, b_prices, big_tiles