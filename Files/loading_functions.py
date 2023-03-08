def convert_json(tile_info):
    tile_names = {}
    tile_des = {} # tile descriptions

    for block in tile_info.keys():
        tile_names[int(block)] = tile_info[block]['name']
        tile_des[int(block)] = tile_info[block]['description']

    return tile_names, tile_des