import random as r
import time as t
import numpy as np
import pygame as pg
import pdb
import matplotlib.pyplot as plt
import json
from perlin_noise import PerlinNoise
from Files.loading_functions import generate_block
import copy

pg.init()
pg.font.init()


def import_foto(name, sizex=50, sizey=50, convert=False):
    photo_raw = pg.image.load('Assets/' + str(name))
    if convert:  # convert = faster, but no transparency
        foto_af = pg.transform.scale(photo_raw, (sizex, sizey)).convert()
    else:
        foto_af = pg.transform.scale(photo_raw, (sizex, sizey)).convert_alpha()
    return foto_af


grid_size = 50
item_size = 15
side_size = int(grid_size / 5)

#static files: these files always stay the same (unless if there is an update or something)
with open("Data/r_crafter_grid.txt") as f:
    r_crafter_grid = eval(f.read())

with open("Data/recipes.json") as f:
    recipes = json.load(f)

with open("Data/creater_btn_order.json") as f:
    creater_btn_order = json.load(f)

with open("Data/creater_prices.json") as f:
    creater_prices = json.load(f)

conveyor_connect_list = [1, 2, 3, 4, 5, 6, 7, 15, -15]

item_font = pg.font.Font('Fonts/Lato.ttf', 20)
r_display_font = pg.font.Font('Fonts/Roboto-Light.ttf', 30)
r_title_font = pg.font.Font('Fonts/Roboto-Bold.ttf', 19)
r_subtitle_font = pg.font.Font('Fonts/Roboto-Light.ttf', 16)
r_font = pg.font.Font('Fonts/Roboto.ttf', 15)

i_title_font = pg.font.Font('Fonts/Roboto-Bold.ttf', 25)
i_text_font = pg.font.Font('Fonts/Roboto.ttf', 16)
i_des_font = pg.font.Font('Fonts/Roboto-Light.ttf', 17)

edit_tile_font = pg.font.Font('Fonts/Roboto.ttf', 35)
edit_tile_font_small = pg.font.Font('Fonts/Roboto.ttf', 30)
edit_tile_font_small_small = pg.font.Font('Fonts/Roboto.ttf', 25)
edit_tile_font_item = pg.font.Font('Fonts/Roboto.ttf', 25)

picture_arrow = import_foto('Blocks/arrow-single.png', grid_size, grid_size)
picture_arrow_cross = import_foto('Blocks/arrow-cross.png', grid_size, grid_size)
picture_arrow_split_r = import_foto('Blocks/arrow-split-right.png', grid_size, grid_size)
picture_arrow_split_l = import_foto('Blocks/arrow-split-left.png', grid_size, grid_size)
picture_arrow_sort_r = import_foto('Blocks/arrow-sorting-right.png', grid_size, grid_size)
picture_arrow_sort_l = import_foto('Blocks/arrow-sorting-left.png', grid_size, grid_size)
picture_arrow_highway = import_foto('Blocks/arrow-highway.png', grid_size, grid_size)

picture_arrow_cable = import_foto('Blocks/arrow-cable.png', grid_size, grid_size)

r_particle_picture = import_foto('Items/itemr.png', item_size * 3, item_size * 3)
r_icon_picture = import_foto('Items/itemr.png', 29, 29)
r_display_picture = import_foto('Items/itemr.png', 44, 44)

# menu stuff
menu_bar_picture = import_foto('UI/menu_bar.png', 1000, 200)
icon_clicked_picture = import_foto('UI/menu_icon_clicked.png', 50, 50)
icon_unclicked_picture = import_foto('UI/menu_icon_unclicked.png', 50, 50)

button_clicked_picture = import_foto('UI/menu_button_clicked.png', 125, 125)
button_unclicked_picture = import_foto('UI/menu_button_unclicked.png', 125, 125)


info_ui = import_foto('UI/info_ui.png',600,400)

lock_picture = import_foto('UI/lock.png', 50, 50)

rect_ui = import_foto('UI/rect_ui.png', 2500, 2500, True)
rect_info = import_foto('UI/info_rect.png', 750, 1000)
rect_keybinds = import_foto('UI/keybind_rect.png', 750, 2000)

data_display = import_foto('UI/data_display.png', 250, 165)
data_arrow = import_foto('UI/data_arrow.png', 250, 215)

research_button_clicked = import_foto('UI/research_button_clicked.png', 1000, 500)
research_button_unclicked = import_foto('UI/research_button.png', 1000, 500)
research_display = import_foto('UI/research_display.png', 1000, 500)

research_crafter_btn_clicked = import_foto("UI/research_crafter_clicked.png",175,175)
research_crafter_btn = import_foto("UI/research_crafter.png",175,175)
research_crafter_btn_start = import_foto("UI/research_crafter_start.png",175,175)

research_creater_btn = import_foto("UI/research_creater.png", 200, 200)
research_creater_btn_clicked = import_foto("UI/research_creater_clicked.png", 200, 200)

research_creater_item_btn = import_foto("UI/research_creater.png", 150, 150)
research_creater_item_btn_clicked = import_foto("UI/research_creater_clicked.png", 150, 150)

not_enough_picture = import_foto('UI/not_enough.png', 2000, 500)

icon_1 = import_foto('UI/menu_icon_1.png', 50, 50)
icon_2 = import_foto('UI/menu_icon_2.png', 50, 50)
icon_3 = import_foto('UI/menu_icon_3.png', 50, 50)
icon_4 = import_foto('UI/menu_icon_4.png', 50, 50)
icon_5 = import_foto('UI/menu_icon_5.png', 50, 50)
icon_6 = import_foto('UI/menu_icon_6.png', 50, 50)
icon_cross = import_foto('UI/menu_icon_cross.png', 50, 50)

craft_select_menu_picture = import_foto("UI/craft_select_menu.png", 500, 375)
craft_select_btn_picture = import_foto("UI/craft_select_btn.png", 375, 125)
craft_select_btn_hover_picture = import_foto("UI/craft_select_btn_hover.png", 375, 125)
craft_select_menu_border_picture = import_foto("UI/craft_select_menu_border.png", 500, 375)
edit_mode_menu_picture = import_foto("UI/edit_mode_menu.png", 550, 550)

tile_menu_w, tile_menu_h = 200, 50
tile_info_menu_1 = import_foto("UI/tile_info_menu_1.png", tile_menu_w, tile_menu_h)
tile_info_menu_2 = import_foto("UI/tile_info_menu_2.png", tile_menu_w, tile_menu_h)
tile_info_menu_3 = import_foto("UI/tile_info_menu_3.png", tile_menu_w, tile_menu_h)
tile_info_menu_4 = import_foto("UI/tile_info_menu_4.png", tile_menu_w, tile_menu_h)

# blocks
unsc_pics = {} # unscaled pictures

with open("Data/tile_info.json") as f:
    tile_info = json.load(f)
    tile_info.pop("ground_blocks")

unsc_pics['picture_0'] = import_foto('Blocks/0.png', grid_size, grid_size)
unsc_pics['picture_1'] = import_foto('Blocks/01.png', grid_size, grid_size, True)  # conveyor
unsc_pics['picture_2'] = import_foto('Blocks/01.png', grid_size, grid_size, True)  # cross-conveyor
unsc_pics['picture_3'] = import_foto('Blocks/01.png', grid_size, grid_size, True)  # split-conveyor-r
unsc_pics['picture_4'] = import_foto('Blocks/01.png', grid_size, grid_size, True)  # split-conveyor-l
unsc_pics['picture_5'] = import_foto('Blocks/01.png', grid_size, grid_size, True)  # sort-conveyor-r
unsc_pics['picture_6'] = import_foto('Blocks/01.png', grid_size, grid_size, True)  # sort-conveyor-l
unsc_pics['picture_7'] = import_foto('Blocks/01.png', grid_size, grid_size, True)  # highway-conveyor

exclude = [1,2,3,4,5,6,7]

for block in tile_info.keys():
    if not int(block) in exclude:
        convert = True
        if "convert_alpha" in tile_info[block]:
            convert = False
        size = int(grid_size * tile_info[block]["size"])
        if "varients" in tile_info[block]: # background tiles varients
            unsc_pics[f'picture_{block}'] = import_foto(f'Blocks/{block}.png', size, size, convert)

            temp_pic = pg.Surface((size, size), pg.SRCALPHA)
            varients = tile_info[block]["varients"]

            for i in range(int(len(varients) / 2)):
                for x in range(tile_info[block]["size"]):
                    for y in range(tile_info[block]["size"]):
                        tile = r.choice(varients[i*2:i*2+2])
                        tile_pic = import_foto(f"Blocks/{tile}.png", size, size, True)
                        temp_pic.blit(tile_pic, (x * 50, y * 50))
                    
                foreground = import_foto(f'Blocks/{block}.png', size, size, convert)
                temp_pic.blit(foreground, (0,0))

                unsc_pics[f'picture_{block}-{varients[i*2]}-{varients[i*2+1]}'] = temp_pic

        elif not convert:
            temp_pic = pg.Surface((size, size), pg.SRCALPHA)

            if tile_info[block]["background_tile"] != [0]:
                for x in range(tile_info[block]["size"]):
                    for y in range(tile_info[block]["size"]):
                        if type(tile_info[block]["background_tile"]) is list:
                            tile = r.choice(tile_info[block]["background_tile"])
                        else:
                            tile = tile_info[block]["background_tile"]
                        tile_pic = import_foto(f"Blocks/{tile}.png", grid_size, grid_size, True)
                        temp_pic.blit(tile_pic, (x * grid_size, y * grid_size))

            foreground = import_foto(f'Blocks/{block}.png', size, size, convert)
            temp_pic.blit(foreground, (0,0))

            unsc_pics[f'picture_{block}'] = temp_pic

        else: # single image
            unsc_pics[f'picture_{block}'] = import_foto(f'Blocks/{block}.png', size, size, convert)

# # picture_25 = import_foto('Blocks/25_base.png', grid_size, grid_size, True)
# # picture_26 = import_foto('Blocks/25_arm.png', grid_size * 3, grid_size * 3) legacy code

picture_list = []
with open("Data/tile_info.json") as f:
    tile_info = json.load(f)
    for block in tile_info.keys():
        if block != "ground_blocks":
            picture_list.append(int(block))

# items
with open("Data/item_info.json") as f:
    item_info = json.load(f)
    largest_val = 0
    for i in item_info:
        if int(i) > largest_val:
            item_count = int(i) 

items_pictures = list(range(0, item_count+1))  # list of all the items (0,1,2 etc)
items_pictures.append('c')
items_pictures.append('random')
for x in items_pictures:
    unsc_pics[f"item_{x}_picture"] = import_foto('Items/item{}.png'.format(x if x != 0 else 'r'), item_size, item_size)

# add to scale lists

scaled_pictures = {}
pictures_scales = {}



for i in range(len(picture_list)):
    scaled_pictures[str('picture_' + str(picture_list[i]))] = [pg.transform.rotate(
        unsc_pics['picture_' + str(picture_list[i])], -angle) for angle in range(0, 360, 90)]
    pictures_scales[str('picture_' + str(picture_list[i]))] = [round(
        float(unsc_pics['picture_' + str(picture_list[i])].get_size()[0] / grid_size)) for angle in range(0, 360, 90)]
    
for i in range(len(items_pictures)):
    scaled_pictures[str('item_' + str(items_pictures[i]) + '_picture')] = [pg.transform.rotate(unsc_pics[
        'item_' + str(items_pictures[i]) + '_picture'], -angle) for angle in range(0, 360, 90)]
    pictures_scales[str('item_' + str(items_pictures[i]) + '_picture')] =[1 for angle in range(0, 360, 90)]

scaled_pictures['picture_arrow'] = [pg.transform.rotate(picture_arrow, -angle) for angle in range(0, 360, 90)]
pictures_scales['picture_arrow'] = [1 for angle in range(0, 360, 90)]
scaled_pictures['picture_arrow_cross'] = [pg.transform.rotate(picture_arrow_cross, -angle) for angle in range(0, 360, 90)]
pictures_scales['picture_arrow_cross'] = [1 for angle in range(0, 360, 90)]
scaled_pictures['picture_arrow_split_r'] = [pg.transform.rotate(picture_arrow_split_r, -angle) for angle in range(0, 360, 90)]
pictures_scales['picture_arrow_split_r'] = [1 for angle in range(0, 360, 90)]
scaled_pictures['picture_arrow_split_l'] = [pg.transform.rotate(picture_arrow_split_l, -angle) for angle in range(0, 360, 90)]
pictures_scales['picture_arrow_split_l'] = [1 for angle in range(0, 360, 90)]
scaled_pictures['picture_arrow_sort_r'] = [pg.transform.rotate(picture_arrow_sort_r, -angle) for angle in range(0, 360, 90)]
pictures_scales['picture_arrow_sort_r'] = [1 for angle in range(0, 360, 90)]
scaled_pictures['picture_arrow_sort_l'] = [pg.transform.rotate(picture_arrow_sort_l, -angle) for angle in range(0, 360, 90)]
pictures_scales['picture_arrow_sort_l'] = [1 for angle in range(0, 360, 90)]
scaled_pictures['picture_arrow_highway'] = [pg.transform.rotate(picture_arrow_highway, -angle) for angle in range(0, 360, 90)]
pictures_scales['picture_arrow_highway'] = [1 for angle in range(0, 360, 90)]
scaled_pictures['picture_arrow_cable'] = [pg.transform.rotate(picture_arrow_cable, -angle) for angle in range(0, 360, 90)]
pictures_scales['picture_arrow_cable'] = [1 for angle in range(0, 360, 90)]

# conveyor frames
conveyor_frames = {}
for i in range(25):
    conveyor_frames['picture_1_' + str(i + 1)] = [import_foto("Blocks/01-" + str(i + 1) + ".png", grid_size, grid_size) for angle in range(0, 360, 90)]
    scaled_pictures['picture_1_' + str(i + 1)] = [pg.transform.rotate(import_foto("Blocks/01-" + str(i + 1) + ".png", grid_size, grid_size), -angle) for angle in range(0, 360, 90)]
    pictures_scales['picture_1_' + str(i + 1)] = [1 for angle in range(0, 360, 90)]

# research frames (25)
research_frames = {}

def generate_random_background(tile1,tile2,size):
    picture = pg.Surface((grid_size * size, grid_size * size))
    for x in range(3):
        for y in range(3):
            picture.blit(pg.transform.rotate(unsc_pics['picture_'+str(r.choice([tile1,tile2]))],r.randint(0,3)*90),(x*grid_size,y*grid_size))
    return picture

picture_random = generate_random_background(10,11,3)

for i in range(0,25):
    picture = pg.Surface((grid_size * 3, grid_size * 3))
    picture.blit(picture_random,(0,0))
    picture.blit(import_foto("Blocks/15-" + str(i + 1) + ".png", grid_size * 3, grid_size * 3),(0,0))
    picture = pg.transform.rotate(picture, 180) #image is upside down
    research_frames['picture_15_' + str(i + 1)] = [picture for angle in range(0, 360, 90)]
    scaled_pictures['picture_15_' + str(i + 1)] = [picture for angle in range(0, 360, 90)]
    pictures_scales['picture_15_' + str(i + 1)] = [3 for angle in range(0, 360, 90)]

#for little part of exporters/importers of cable things that gets blit over
picture_cable_in = pg.Surface((grid_size*3,grid_size*3),pg.SRCALPHA)
picture_cable_in.blit(scaled_pictures['picture_8'][0],(grid_size,grid_size))
picture_cable_in.blit(scaled_pictures['picture_18'][2],(grid_size,0))

picture_cable_out = pg.Surface((grid_size*3,grid_size*3),pg.SRCALPHA)
picture_cable_out.blit(scaled_pictures['picture_9'][0],(grid_size,grid_size))
picture_cable_out.blit(scaled_pictures['picture_18'][0],(grid_size,0))

scaled_pictures['picture_cable_in'] = [pg.transform.rotate(picture_cable_in, -angle) for angle in range(0, 360, 90)]
pictures_scales['picture_cable_in'] = [3 for angle in range(0, 360, 90)]
scaled_pictures['picture_cable_out'] = [pg.transform.rotate(picture_cable_out, -angle) for angle in range(0, 360, 90)]
pictures_scales['picture_cable_out'] = [3 for angle in range(0, 360, 90)]

picture_plane_1 = import_foto("Other/plane.png", 2 * grid_size, 2 * grid_size)
unsc_pics["plane_1"] = picture_plane_1

scaled_pictures['plane_1'] = [pg.transform.rotate(picture_plane_1, -angle) for angle in range(0, 360, 90)]
pictures_scales['plane_1'] = [2 for angle in range(0, 360, 90)]

crafter_frames = {}
crafter_colors = ["black","dark_blue","dark_green","dark_red","gray","light_blue","light_green","orange","pink","purple","red","yellow"]
crafter_picture_colors = {}
for i in crafter_colors:
    crafter_picture_colors[i] = [pg.transform.rotate(import_foto("Blocks/base_research_"+str(i)+".png",150,150), -angle) for angle in range(0, 360, 90)]

crafter_craftables = {0: ""}
for item in recipes:
    if item != "_":
        crafter_craftables[int(item)] = recipes[item]["color"]

for color in crafter_colors:
    crafter_frames[str(color)] = {}
    picture_random = generate_random_background(10,11,3)
    for i in range(25):
        final_picture = pg.Surface((150,150))
        final_picture.blit(picture_random,(0,0))
        final_picture.blit(research_frames["picture_15_"+str(i + 1)][0],(0,0))
        final_picture.blit(crafter_picture_colors[color][0],(0,0))

        crafter_frames[str(color)][i+1] = [pg.transform.rotate(final_picture, -angle) for angle in range(0, 360, 90)]
        pictures_scales['picture_15_' + str(i + 1)] = [3 for angle in range(0, 360, 90)]

for craftable in crafter_craftables.keys():
    crafter_frames[craftable] = {}
    picture_random = generate_random_background(10,11,3)
    for i in range(25):
        if crafter_craftables[craftable] != "": # 0 is exception: it won't be drawn
            color = crafter_craftables[craftable]
        final_picture = pg.Surface((150,150))
        final_picture.blit(picture_random,(0,0))
        final_picture.blit(research_frames["picture_15_"+str(i + 1)][0],(0,0))
        if crafter_craftables[craftable] != "":
            final_picture.blit(crafter_picture_colors[color][0],(0,0))

            item_blit_size = 50
            item_blit_picture = import_foto("Items/item"+str(craftable)+".png")
            item_blit_picture = pg.transform.scale(item_blit_picture,(item_blit_size,item_blit_size))

            final_picture.blit(item_blit_picture,(int((150-item_blit_size)/2),int((150-item_blit_size)/2)))

        #crafter_frames[craftable][i+1] = [pg.transform.rotate(final_picture, -angle) for angle in range(0, 360, 90)]
        research_frames["picture_15_{}_{}".format(i+1, craftable)] = [pg.transform.rotate(final_picture, -angle) for angle in range(0, 360, 90)]
        pictures_scales['picture_15_' + str(i + 1) + "_" + str(craftable)] = [3 for angle in range(0, 360, 90)]
        scaled_pictures["picture_15_{}_{}".format(i+1, craftable)] = [pg.transform.scale(research_frames["picture_15_{}_{}".format(i+1, craftable)][int(angle/90)], (
                int(np.ceil(pictures_scales["picture_15_{}_{}".format(i+1, craftable)][int(angle/90)] * 1 * grid_size)),
                int(np.ceil(pictures_scales["picture_15_{}_{}".format(i+1, craftable)][int(angle/90)] * 1 * grid_size)))) for angle in range(0, 360, 90)] 

scaled_pictures_scales = {} #all the images with all the scales preloaded so faster when zooming in or out
min_scale = 0.1
max_scale = 1.5

for scale_int in range(int(min_scale * 10), int((max_scale + 0.1) * 10), 1):
    scale = scale_int / 10
    scaled_pictures_scales[scale] = {}
    for key in scaled_pictures.keys():
        if 'item' in key:  # item
            scaled_pictures_scales[scale][key] = [pg.transform.rotate(pg.transform.scale(unsc_pics[key], (
                int(np.ceil(pictures_scales[key][int(angle/90)] * scale * item_size)),
                int(np.ceil(pictures_scales[key][int(angle/90)] * scale * item_size)))), -angle) for angle in range(0, 360, 90)]
        elif 'picture_1_' in key:  # animated conveyor
            scaled_pictures_scales[scale][key] = [pg.transform.rotate(pg.transform.scale(conveyor_frames[key][int(angle/90)], (
                int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
                int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))), -angle) for angle in range(0, 360, 90)]
        elif 'picture_15_' in key:
            scaled_pictures_scales[scale][key] = [pg.transform.scale(research_frames[key][int(angle/90)], (
                int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
                int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))) for angle in range(0, 360, 90)]   
        elif 'picture_arrow' in key or 'picture_cable' in key:
            scaled_pictures_scales[scale][key] = [pg.transform.rotate(pg.transform.scale(eval(key), (
                int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
                int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))), -angle) for angle in range(0, 360, 90)]
        else:
            scaled_pictures_scales[scale][key] = [pg.transform.rotate(pg.transform.scale(unsc_pics[key], (
                int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
                int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))), -angle) for angle in range(0, 360, 90)]

def scale_pictures(scale, grid_size=grid_size, item_size=item_size, scaled_pictures=scaled_pictures, scaled_pictures_scales=scaled_pictures_scales):
    for key in scaled_pictures.keys():
        scaled_pictures[key] = scaled_pictures_scales[scale][key]
        # if 'item' in key:  # item
        # elif 'picture_1_' in key:  # animated conveyor
        #     scaled_pictures[key] = [pg.transform.rotate(pg.transform.scale(conveyor_frames[key][int(angle/90)], (
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))), -angle) for angle in range(0, 360, 90)]
        # elif 'picture_15_' in key:
        #     scaled_pictures[key] = [pg.transform.scale(research_frames[key][int(angle/90)], (
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))) for angle in range(0, 360, 90)]   
        # elif 'picture_arrow' in key or 'picture_cable' in key:
        #     scaled_pictures[key] = [pg.transform.rotate(pg.transform.scale(eval(key), (
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))), -angle) for angle in range(0, 360, 90)]
        # else:
        #     scaled_pictures[key] = [pg.transform.rotate(pg.transform.scale(unsc_pics[key], (
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))), -angle) for angle in range(0, 360, 90)]

        # if 'item' in key:  # item
        #     scaled_pictures[key] = [pg.transform.rotate(pg.transform.scale(unsc_pics[key], (
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * item_size)),
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * item_size)))), -angle) for angle in range(0, 360, 90)]
        # elif 'picture_1_' in key:  # animated conveyor
        #     scaled_pictures[key] = [pg.transform.rotate(pg.transform.scale(conveyor_frames[key][int(angle/90)], (
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))), -angle) for angle in range(0, 360, 90)]
        # elif 'picture_15_' in key:
        #     scaled_pictures[key] = [pg.transform.scale(research_frames[key][int(angle/90)], (
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))) for angle in range(0, 360, 90)]   
        # elif 'picture_arrow' in key or 'picture_cable' in key:
        #     scaled_pictures[key] = [pg.transform.rotate(pg.transform.scale(eval(key), (
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))), -angle) for angle in range(0, 360, 90)]
        # else:
        #     scaled_pictures[key] = [pg.transform.rotate(pg.transform.scale(unsc_pics[key], (
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
        #         int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))), -angle) for angle in range(0, 360, 90)]
    return scaled_pictures

def teken_grid(screen, grid, grid_rotation, selected_x, selected_y, move, scrollx, scrolly, screen_size,
               render_distance, storage, scale, scaled_pictures, blocks_index, grid_cables, brush, angle,grid_data, queue=None,
               conveyor_connect_list=conveyor_connect_list):
    screen = screen
    drawn_xy = []
    move_dict = {1: 0, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4}
    draw_last_list = []
    for x in range(max(0, int(abs(scrollx) / (grid_size * scale))), min(grid.shape[1],
                                                                        int(int((abs(scrollx) + screen_size[0]) / (
                                                                                grid_size * scale) + 1) + np.ceil(
                                                                            (abs(scrollx) + screen_size[0]) / (
                                                                                        grid_size * scale) % 1)))):
        for y in range(max(0, int(abs(scrolly) / (grid_size * scale))), min(grid.shape[0],
                                                                            int(int((abs(scrolly) + screen_size[1]) / (
                                                                                    grid_size * scale) + 1) + np.ceil(
                                                                                (abs(scrolly) + screen_size[1]) / (
                                                                                        grid_size * scale) % 1)))):
            built = grid[y, x]
            orientation = grid_rotation[y, x]
            x_grid_scale = round(x * grid_size * scale) + scrollx
            y_grid_scale = round(y * grid_size * scale) + scrolly

            

            if built in [10, 11, 21, 22, 23, 24, 25, 26]:  # ground
                screen.blit(scaled_pictures["picture_" + str(built)][orientation],
                                 (x_grid_scale, y_grid_scale))

            elif built in [1, 2, 3, 4, 5, 6, 7]:  # conveyors
                screen.blit(scaled_pictures["picture_1_" + str(int(move[move_dict[built]] + 1))][orientation], (x_grid_scale, y_grid_scale))

                if built == 1:  # conveyor
                    screen.blit(scaled_pictures["picture_arrow"][orientation],
                                     (x_grid_scale, y_grid_scale))
                elif built == 2:  # cross-conveyor
                    screen.blit(scaled_pictures["picture_arrow_cross"][orientation],
                                     (x_grid_scale, y_grid_scale))
                elif built == 3:  # split-conveyor-r
                    screen.blit(scaled_pictures["picture_arrow_split_r"][orientation],
                                     (x_grid_scale, y_grid_scale))
                elif built == 4:  # split-conveyor-l
                    screen.blit(scaled_pictures["picture_arrow_split_l"][orientation],
                                     (x_grid_scale, y_grid_scale))
                elif built == 5:  # sort-conveyor-r
                    screen.blit(scaled_pictures["picture_arrow_sort_r"][orientation],
                                     (x_grid_scale, y_grid_scale))
                elif built == 6:  # sort-conveyor-l
                    screen.blit(scaled_pictures["picture_arrow_sort_l"][orientation],
                                     (x_grid_scale, y_grid_scale))
                elif built == 7:  # highway-conveyor
                    screen.blit(scaled_pictures["picture_arrow_highway"][orientation],
                                     (x_grid_scale, y_grid_scale))

                pg.draw.rect(screen, (82, 82, 82), (
                (x_grid_scale, y_grid_scale), (round(side_size * scale), round(side_size * scale))))  # linksboven
                pg.draw.rect(screen, (82, 82, 82), (
                (round((x * grid_size + grid_size - side_size) * scale + scrollx), round(y * grid_size * scale) + scrolly),
                (round(side_size * scale), round(side_size * scale))))  # rechtsboven
                pg.draw.rect(screen, (82, 82, 82), (
                (round(x * grid_size * scale)+ scrollx, round((y * grid_size + grid_size - side_size) * scale)+ scrolly),
                (round(side_size * scale), round(side_size * scale))))  # linksonder
                pg.draw.rect(screen, (82, 82, 82), ((round((x * grid_size + grid_size - side_size) * scale)+ scrollx,
                                                          round((y * grid_size + grid_size - side_size) * scale)+ scrolly), (
                                                         round(side_size * scale),
                                                         round(side_size * scale))))  # rechtsonder

                side_scale = round(side_size * scale)
                if y > 0:
                    if not grid[y - 1, x] in conveyor_connect_list:
                        pg.draw.rect(screen, (82, 82, 82),
                                     ((x_grid_scale, y_grid_scale), (round(grid_size * scale), side_scale)))
                else:
                    pg.draw.rect(screen, (82, 82, 82),
                                 ((x_grid_scale, y_grid_scale), (round(grid_size * scale), side_scale)))

                if x > 0:
                    if not grid[y, x - 1] in conveyor_connect_list:
                        pg.draw.rect(screen, (82, 82, 82),
                                     ((x_grid_scale, y_grid_scale), (side_scale, round(grid_size * scale))))
                else:
                    pg.draw.rect(screen, (82, 82, 82),
                                 ((x_grid_scale, y_grid_scale), (side_scale, round(grid_size * scale))))

                if x < grid.shape[0] - 1:
                    if y + 1 == grid.shape[0]:
                        pg.draw.rect(screen, (82, 82, 82), (
                        (x_grid_scale, round((y * grid_size + grid_size - side_size) * scale)+ scrolly),
                        (round(grid_size * scale), side_scale)))
                    elif not grid[y + 1, x] in conveyor_connect_list:
                        pg.draw.rect(screen, (82, 82, 82), (
                        (x_grid_scale, round((y * grid_size + grid_size - side_size) * scale)+ scrolly),
                        (round(grid_size * scale), side_scale)))
                else:
                    pg.draw.rect(screen, (82, 82, 82), (
                    (x_grid_scale, round((y * grid_size + grid_size - side_size) * scale)+ scrolly),
                    (round(grid_size * scale), side_scale)))

                if y < grid.shape[1] - 1:
                    if x + 1 == grid.shape[1]:
                        pg.draw.rect(screen, (82, 82, 82), (
                        (round((x * grid_size + grid_size - side_size) * scale)+ scrollx, y_grid_scale),
                        (side_scale, round(grid_size * scale))))
                    elif not grid[y, x + 1] in conveyor_connect_list:
                        pg.draw.rect(screen, (82, 82, 82), (
                        (round((x * grid_size + grid_size - side_size) * scale)+ scrollx, y_grid_scale),
                        (side_scale, round(grid_size * scale))))
                else:
                    pg.draw.rect(screen, (82, 82, 82), (
                    (round((x * grid_size + grid_size - side_size) * scale)+ scrollx, y_grid_scale),
                    (side_scale, round(grid_size * scale))))

            # elif built == 25:
            #     screen.blit(scaled_pictures["picture_25"][orientation], (x_grid_scale, y_grid_scale))
            #     draw_last_list.append([orientation, (round((x - 1) * grid_size * scale) + scrollx, round((y - 1) * grid_size * scale) + scrolly)])

            else:
                screen, drawn_xy, grid_cables = render_building(built,x,y,orientation,drawn_xy,screen,scale,grid,grid_rotation,grid_cables,blocks_index,scaled_pictures,scrollx,scrolly,move,grid_data)

            #temp stuff
            if grid_cables[y,x] > 0:
                if brush in [16,17,18,19]:
                    screen.blit(scaled_pictures["picture_arrow_cable"][grid_cables[y,x]-1],
                                     (x_grid_scale, y_grid_scale))

    # for i in draw_last_list:
    #     rotated_scaled = pg.transform.rotate(scaled_pictures["picture_26"][i[0]], angle)
    #     new_rect = rotated_scaled.get_rect(center = scaled_pictures["picture_26"][i[0]].get_rect(topleft =  i[1]).center)
    #     screen.blit(rotated_scaled, new_rect.topleft)

    pg.draw.rect(screen, (0, 72, 245), (
    (round(selected_x * grid_size * scale) + scrollx, round(selected_y * grid_size * scale) +scrolly),
    (round(grid_size * scale), round(grid_size * scale))), width=2)
    
    return grid_cables

def render_building(built,x,y,orientation,drawn_xy,main_screen,scale,grid,grid_rotation,grid_cables,blocks_index,scaled_pictures,scrollx, scrolly,move,grid_data,grid_size=grid_size,crafter_frames=crafter_frames,research_frames=research_frames):
    x_grid_scale = round(x * grid_size * scale)+scrollx
    y_grid_scale = round(y * grid_size * scale)+scrolly
    
    if built in [16, 17, 18]:
        if [x, y] not in drawn_xy:
            drawn_xy.append([x, y])
            main_screen, grid_cables = draw_cables(x,y,main_screen,built,orientation,grid,grid_rotation, grid_cables, scale, scaled_pictures,scrollx, scrolly)
    elif -built in [16,17,18]:
        x_, y_ = outside_screen_render(x, y, grid, grid_rotation, blocks_index, abs(built))
        if [x_, y_] not in drawn_xy:
            drawn_xy.append([x_, y_])
            main_screen,grid_cables = draw_cables(x_,y_,main_screen,abs(built),orientation,grid,grid_rotation, grid_cables, scale, scaled_pictures,scrollx, scrolly)

    elif built == abs(built):#positive render
        #main_screen.blit(scaled_pictures["picture_15_" + str(int(move[move_dict[built]] + 1))][orientation], (x_grid_scale, y_grid_scale))

        if [x, y] not in drawn_xy:
            drawn_xy.append([x, y])
            if built == 15:
                main_screen.blit(scaled_pictures["picture_15_" + str(int(move[0]+1)) + "_" + str(grid_data[y,x]["craft_recipe"] if grid_data[y, x]["craft_recipe"] != -1 else "r")][orientation],
                                (x_grid_scale, y_grid_scale))

            else:
                main_screen.blit(scaled_pictures["picture_"+str(abs(built))][orientation],
                                (x_grid_scale, y_grid_scale))

    else:#negative render
        x_, y_ = outside_screen_render(x, y, grid, grid_rotation, blocks_index, abs(built))
        if [x_, y_] not in drawn_xy:
            drawn_xy.append([x_, y_])
            if built == -15:
                if grid_data[y,x]["craft_recipe"] == -1:
                    main_screen.blit(scaled_pictures["picture_15_" + str(int(move[0]+1)) + "_" + str(grid_data[y,x]["craft_recipe"] if grid_data[y, x]["craft_recipe"] != -1 else "r")][orientation],
                                (round(x_ * grid_size * scale)+scrollx, round(y_ * grid_size * scale)+scrolly))

                else:
                    main_screen.blit(scaled_pictures["picture_15_" + str(int(move[0]+1))][orientation],
                                (round(x_ * grid_size * scale)+scrollx, round(y_ * grid_size * scale)+scrolly))
            else:
                main_screen.blit(scaled_pictures["picture_"+str(abs(built))][grid_rotation[y_, x_]],
                                (round(x_ * grid_size * scale)+scrollx, round(y_ * grid_size * scale)+scrolly))

        
    return main_screen, drawn_xy, grid_cables

def draw_cables(x_in, y_in, main_screen, built, orientation, grid, grid_rotation, grid_cables, scale, scaled_pictures,scrollx, scrolly):
    height_grid, width_grid = grid.shape
    x = x_in
    y = y_in

    x_grid_scale = round(x * grid_size * scale)+scrollx
    y_grid_scale = round(y * grid_size * scale)+scrolly
    
    if built in [16,17]:
        main_screen.blit(scaled_pictures['picture_'+str(built)][0],(x_grid_scale,y_grid_scale))
        #main_screen.blit(scaled_pictures['picture_cable_in'][0],(x_grid_scale,y_grid_scale))
        blit_up = False
        blit_down = False
        blit_left = False
        blit_right = False

        built_16 = built == 16
        built_17 = built == 17

        if grid_cables[max(y-1,0), x+1] > 0:#up (max prevents index error)
            if grid_cables[max(y-1,0), x+1] == 1 and built_16:
                blit_up = True

            elif grid_cables[max(y-1,0), x+1] == 3 and built_17:
                blit_up = True

        if grid_cables[min(y+3,height_grid),x+1] > 0:#down
            if grid_cables[min(y+3,height_grid),x+1] == 1 and built_17:
                blit_down = True

            elif grid_cables[min(y+3,height_grid),x+1] == 3 and built_16:
                blit_down = True

        if grid_cables[y+1,min(x+3,width_grid)] > 0:#right
            if grid_cables[y+1,min(x+3,width_grid)] == 2 and built_16:
                blit_right = True

            elif grid_cables[y+1,min(x+3,width_grid)] == 4 and built_17:
                blit_right = True

        if grid_cables[y+1,max(x-1,0)] > 0:#left
            if grid_cables[y+1,max(x-1,0)] == 2 and built_17:
                blit_left = True
            elif grid_cables[y+1,max(x-1,0)] == 4 and built_16:
                blit_left = True

        blit_picture = ''
        if built == 16:
            blit_picture = 'picture_cable_out' #dict key of scaled_pictures
        elif built == 17:
            blit_picture = 'picture_cable_in'

        blit_16 = False #outgoing cable tile can only have 1 output (other can have multiple inputs)
        if blit_up:
            main_screen.blit(scaled_pictures[blit_picture][0],(x_grid_scale,y_grid_scale))
            if built_16:
                blit_16 = True
                grid_cables[y,x+1] = 1
                grid_cables[y+1,x+1] = 1
            else:
                grid_cables[y,x+1] = 3
        else:
            grid_cables[y,x+1] = 0

        if blit_down and not blit_16:
            main_screen.blit(scaled_pictures[blit_picture][2],(x_grid_scale,y_grid_scale))
            if built_16:
                blit_16 = True
                grid_cables[y+1,x+1] = 3
                grid_cables[y+2,x+1] = 3
            else:
                grid_cables[y+2,x+1] = 1
        else:
            grid_cables[y+2,x+1] = 0

        if blit_left and not blit_16:
            main_screen.blit(scaled_pictures[blit_picture][3],(x_grid_scale,y_grid_scale))
            if built_16:
                blit_16 = True
                grid_cables[y+1,x] = 4
                grid_cables[y+1,x+1] = 4
            else:
                grid_cables[y+1,x] = 2
        else:
            grid_cables[y+1,x] = 0

        if blit_right and not blit_16:
            main_screen.blit(scaled_pictures[blit_picture][1],(x_grid_scale,y_grid_scale))
            if built_16:
                blit_16 = True
                grid_cables[y+1,x+1] = 2
                grid_cables[y+1,x+2] = 2
            else:
                grid_cables[y+1,x+2] = 4
        else:
            grid_cables[y+1,x+2] = 0
            
    elif built == 18:
        cable_up = False
        cable_down = False
        cable_left = False
        cable_right = False
        own_rotation = grid_cables[y,x]
        if (grid_cables[y-1, x] == 1 and own_rotation == 1) or own_rotation == 1:#up
            cable_up = True
        if grid_cables[y-1, x] == 3:#up
            cable_up = True

        if grid_cables[y+1,x] == 1:#down
            cable_down = True
        if (grid_cables[y+1,x] == 3 and own_rotation == 3) or own_rotation == 3:#down
            cable_down = True

        if (grid_cables[y,x+1] == 2 and own_rotation == 2) or own_rotation == 2: #right
            cable_right = True
        if grid_cables[y,x+1] == 4: #right
            cable_right = True
        
        if grid_cables[y,x-1] == 2: #left
            cable_left = True
        if (grid_cables[y,x-1] == 4 and own_rotation == 4) or own_rotation == 4: #left
            cable_left = True

        #TEMP!!!
        main_screen.blit(scaled_pictures["picture_10"][2],
                                        (x_grid_scale, y_grid_scale))
        if orientation in [0,2] and not cable_left and not cable_right:
            main_screen.blit(scaled_pictures["picture_18"][orientation],(x_grid_scale,y_grid_scale))
        elif orientation in [1,3] and not cable_up and not cable_down:
            main_screen.blit(scaled_pictures["picture_18"][orientation],(x_grid_scale,y_grid_scale))
        else: #draw shorter cable thingy
            if cable_up:
                if grid_cables[y-1, x] == 1 or own_rotation == 1:
                    main_screen.blit(scaled_pictures["picture_9"][0],
                                        (x_grid_scale, y_grid_scale))
                elif grid_cables[y-1, x] == 3:
                    main_screen.blit(scaled_pictures["picture_8"][0],
                                        (x_grid_scale, y_grid_scale))

            if cable_down:
                if grid_cables[y+1,x] == 1:
                    main_screen.blit(scaled_pictures["picture_8"][2],
                                        (x_grid_scale, y_grid_scale))
                elif grid_cables[y+1,x] == 3 or own_rotation == 3:
                    main_screen.blit(scaled_pictures["picture_9"][2],
                                        (x_grid_scale, y_grid_scale))
 
            if cable_right:
                if grid_cables[y,x+1] == 2 or own_rotation == 2:
                    main_screen.blit(scaled_pictures["picture_9"][1],
                                        (x_grid_scale, y_grid_scale))
                elif grid_cables[y,x+1] == 4:
                    main_screen.blit(scaled_pictures["picture_8"][1],
                                        (x_grid_scale, y_grid_scale))

            if cable_left:
                if grid_cables[y,x-1] == 2:
                    main_screen.blit(scaled_pictures["picture_8"][3],
                                        (x_grid_scale, y_grid_scale))
                elif grid_cables[y,x-1] == 4 or own_rotation == 4:
                    main_screen.blit(scaled_pictures["picture_9"][3],
                                        (x_grid_scale, y_grid_scale))

    return main_screen, grid_cables
    

def outside_screen_render(x, y, grid, grid_rotation, blocks_index, blocks_type):
    if x > blocks_index[blocks_type] and y > blocks_index[blocks_type]:
        cut = grid[y - blocks_index[blocks_type] + 1:y + 1, x - blocks_index[blocks_type] + 1:x + 1]
        dx = x - blocks_index[blocks_type] + 1
        dy = y - blocks_index[blocks_type] + 1
    elif x >= blocks_index[blocks_type] and y >= blocks_index[blocks_type]:
        cut = grid[y - blocks_index[blocks_type] + 1:y + 1, x - blocks_index[blocks_type] + 1:x + 1]
        dx = x - blocks_index[blocks_type] + 1
        dy = y - blocks_index[blocks_type] + 1
    else:  # on edge of grid
        if not x >= blocks_index[blocks_type] and (y >= blocks_index[blocks_type]):
            cut = grid[y - blocks_index[blocks_type] + 1:y + 1, 0:x + 1]
            dx = 0
            dy = y - blocks_index[blocks_type] + 1
        elif (x >= blocks_index[blocks_type]) and not y >= blocks_index[blocks_type]:
            cut = grid[0:y + 1, x - blocks_index[blocks_type] + 1:x + 1]
            dx = x - blocks_index[blocks_type] + 1
            dy = 0
        else:  # cornered
            cut = grid[0:y + 1, 0:x + 1]
            dx = 0
            dy = 0

    linksboven = np.where(cut == blocks_type)
    x_ = dx + linksboven[1][0]
    y_ = dy + linksboven[0][0]
    return x_, y_


def bereken_muis_pos(mx, my, scrollx, scrolly, scale, grid_size=grid_size):
    mrx = round((mx - scrollx - (scale*grid_size) / 2) / scale / grid_size)
    mry = round((my - scrolly - (scale*grid_size) / 2) / scale / grid_size)
    return mrx, mry


def draw_preview_box(screen, selecting_tile, mrx, mry, mrr, brush, scrollx, scrolly, scale, scaled_pictures, size, placeable, editing_tile, grid_size=grid_size):
    if not brush in [10, 11]:
        if not selecting_tile and not editing_tile:
            color = (18, 230, 194) if placeable else (235, 42, 16) 
            screen.blit(scaled_pictures["picture_" + str(brush)][mrr],
                        (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
            if brush == 1:
                screen.blit(scaled_pictures["picture_arrow"][mrr],
                            (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
            elif brush == 2:
                screen.blit(scaled_pictures["picture_arrow_cross"][mrr],
                            (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
            elif brush == 3:
                screen.blit(scaled_pictures["picture_arrow_split_r"][mrr],
                            (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
            elif brush == 4:
                screen.blit(scaled_pictures["picture_arrow_split_l"][mrr],
                            (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
            elif brush == 5:
                screen.blit(scaled_pictures["picture_arrow_sort_r"][mrr],
                            (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
            elif brush == 6:
                screen.blit(scaled_pictures["picture_arrow_sort_l"][mrr],
                            (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
            elif brush == 7:
                screen.blit(scaled_pictures["picture_arrow_highway"][mrr],
                            (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
        elif selecting_tile:
            size = 1
            color = (32, 18, 230)
        elif editing_tile:
            size = 1
            color = (24, 147, 214)
        
        pg.draw.rect(screen, color, (
        (int(mrx * grid_size * scale + scrollx), int(mry * grid_size * scale + scrolly)),
        (int(grid_size * size * scale), int(grid_size * size * scale))), width=2)

def check_build_prices(b_prices, brush, storage, item_names):
    buildable = True
    for item in b_prices[brush].keys():
        storage_available = storage[item_names[0].index(item)]
        if storage_available < b_prices[brush][item]:
            buildable = False
    return buildable


def build(rx, ry, rr, grid, grid_rotation, grid_data, brush, size, b_prices, storage, item_names, draw_brush=None,
          free=False, spawn=False,crafter=-100):
    if draw_brush is None:
        draw_brush = brush
    free = True
    if check_build_prices(b_prices, brush, storage, item_names) or free:
        grid[ry, rx] = draw_brush
        grid_rotation[ry, rx] = rr
        if not spawn:
            grid_data[ry, rx] = {}
            if crafter != -100:
                grid_data[ry, rx]["craft_recipe"] = crafter
            if brush in [3, 4]:
                grid_data[ry, rx]["split_side"] = 0
                grid_data[ry, rx]["split_count"] = 2
            elif brush in [5, 6]:
                grid_data[ry, rx]["sort_item"] = 0
        else:
            grid_data[ry, rx] = {"spawn_item": brush, "spawn_perf": t.perf_counter(), "selected_item": "random"}

        if not free:
            for item in b_prices[brush].keys():
                storage[item_names[0].index(item)] -= b_prices[brush][item]
    else:
        print("not enough resources!")
    return grid, grid_rotation, grid_data, storage

def check_placeable(rx, ry, rr, grid, grid_rotation, brush, size, blocks_index, storage, b_prices, grid_cables, big_tiles, placed_on_only, cannot_place_on, ground_blocks, strict_placement_tiles, item_names):
    placeable = False

    if brush != 0 and not (grid[ry, rx] == brush and grid_rotation[ry, rx] == rr):
        if size == 1:
            placeable = False # if it is placeable or not
            if placed_on_only[brush] == [] and cannot_place_on[brush] == []: # default tile placement required: defaults to ground blocks
                if grid[ry, rx] in ground_blocks:
                    placeable = True
            elif placed_on_only[brush] != [] and grid[ry, rx] in placed_on_only[brush]:
                placeable = True
            elif (cannot_place_on[brush] != []) and (not grid[ry, rx] in cannot_place_on[brush]):
                placeable = True

        else:  # size > 1
            placeable = False

            if placed_on_only[brush] == [] and cannot_place_on[brush] == []: # default tile placement required: defaults to ground blocks
                if grid[ry, rx] in ground_blocks:
                    placeable = True
            elif placed_on_only[brush] != [] and grid[ry, rx] in placed_on_only[brush]:
                placeable = True
            elif (cannot_place_on[brush] != []) and (not grid[ry, rx] in cannot_place_on[brush]):
                placeable = True

            if placeable and brush in strict_placement_tiles:
                ground_block = int(grid[ry, rx])
                ground_block_index = ground_blocks.index(ground_block)
                if ground_block_index % 2 == 0:
                    allowed_ground_blocks = [ground_block, ground_blocks[ground_block_index + 1]]
                else: 
                    allowed_ground_blocks = [ground_block, ground_blocks[ground_block_index - 1]]

            if placeable:
                for x in range(rx, rx + size):
                    for y in range(ry, ry + size):
                        if grid[y, x] in cannot_place_on[brush]:                            
                            placeable = False
                        elif placed_on_only != [] and not grid[y, x] in placed_on_only[brush]:
                            placeable = False
                        elif (brush in strict_placement_tiles) and (not grid[y, x] in allowed_ground_blocks):
                            placeable = False

    elif brush == 0: # red x removing thing
        if not grid[ry, rx] in ground_blocks:
            placeable = True

    if (not check_build_prices(b_prices, brush, storage, 1230)) and False:
        placeable = False

    return placeable


def add_to_grid(rx, ry, rr, grid, grid_rotation, grid_data, brush, size, blocks_index, storage, item_names, b_prices,grid_cables,big_tiles,placed_on_only,cannot_place_on,ground_blocks, grid_generation, grid_generation_features, strict_placement_tiles):
    placeable = False
    cable_delete = False #default value
    grid_h, grid_w = grid.shape
    grid_h -= 1
    grid_w -= 1
    if brush != 0 and not (grid[ry, rx] == brush and grid_rotation[ry, rx] == rr):
        if size == 1:
            placeable = False # if it is placeable or not
            if placed_on_only[brush] == [] and cannot_place_on[brush] == []: # default tile placement required: defaults to ground blocks
                if grid[ry, rx] in ground_blocks:
                    placeable = True
            elif placed_on_only[brush] != [] and grid[ry, rx] in placed_on_only[brush]:
                placeable = True
            elif (cannot_place_on[brush] != []) and (not grid[ry, rx] in cannot_place_on[brush]):
                placeable = True

            if placeable:
                if brush == 1:
                    if True:  # grid[ry,rx] == 1:
                        cross = False
                        if grid[min(grid_h,ry + 1), rx] == 1 and grid[min(0,ry - 1), rx] == 1:
                            if grid_rotation[min(grid_h,ry + 1), rx] == grid_rotation[min(grid_h,ry - 1), rx] and grid_rotation[
                                min(grid_h,ry + 1), rx] % 2 == 0:
                                if grid[ry, min(grid_w,rx + 1)] == 1 and grid[ry, min(grid_w,rx - 1)] == 1:
                                    if grid_rotation[ry, min(grid_w,rx + 1)] == grid_rotation[ry, min(grid_w,rx - 1)] and grid_rotation[
                                        ry, min(grid_w,rx + 1)] % 2 == 1:
                                        cross = True

                        if cross:  # conveyor overlapping: cross
                            grid, grid_rotation, grid_data, storage = build(rx, ry, grid_rotation[ry + 1, rx], grid,
                                                                            grid_rotation, grid_data, 2, size, b_prices,
                                                                            storage, item_names)

                        else:
                            grid, grid_rotation, grid_data, storage = build(rx, ry, rr, grid, grid_rotation, grid_data,
                                                                            brush, size, b_prices, storage, item_names)
                
                else:  # normal
                    grid, grid_rotation, grid_data, storage = build(rx, ry, rr, grid, grid_rotation, grid_data, brush,
                                                                    size,
                                                                    b_prices, storage, item_names)
                    
                    if brush == 18:
                        grid_cables[ry,rx] = rr + 1 #update grid cables list

        else:  # size > 1
            placeable = False

            if placed_on_only[brush] == [] and cannot_place_on[brush] == []: # default tile placement required: defaults to ground blocks
                if grid[ry, rx] in ground_blocks:
                    placeable = True
            elif placed_on_only[brush] != [] and grid[ry, rx] in placed_on_only[brush]:
                placeable = True
            elif (cannot_place_on[brush] != []) and (not grid[ry, rx] in cannot_place_on[brush]):
                placeable = True

            if placeable and brush in strict_placement_tiles:
                ground_block = int(grid[ry, rx])
                ground_block_index = ground_blocks.index(ground_block)
                if ground_block_index % 2 == 0:
                    allowed_ground_blocks = [ground_block, ground_blocks[ground_block_index + 1]]
                else: 
                    allowed_ground_blocks = [ground_block, ground_blocks[ground_block_index - 1]]

            if placeable:
                for x in range(rx, rx + size):
                    for y in range(ry, ry + size):
                        if grid[y, x] in cannot_place_on[brush]:                            
                            placeable = False
                        elif placed_on_only != [] and not grid[y, x] in placed_on_only[brush]:
                            placeable = False
                        elif (brush in strict_placement_tiles) and (not grid[y, x] in allowed_ground_blocks):
                            placeable = False

            if placeable:
                crafter = 0
                if check_build_prices(b_prices, brush, storage, item_names) or True:
                    free_build = False
                    for x in range(rx, rx + size):
                        for y in range(ry, ry + size):
                            grid, grid_rotation, grid_data, storage = build(x, y, rr, grid, grid_rotation, grid_data,
                                                                            brush, size,
                                                                            b_prices, storage, item_names,
                                                                            draw_brush=-brush, free=True, crafter=crafter)
                            
                    grid, grid_rotation, grid_data, storage = build(rx, ry, rr, grid, grid_rotation, grid_data, brush,
                                                                    size,
                                                                    b_prices, storage, item_names, draw_brush=brush, free=free_build, crafter=crafter)

                    if brush == 16: #spawn cargo items
                        grid_data[ry, rx] = {"spawn_item": brush, "spawn_perf": t.perf_counter()}
                        
                else:
                    print("not enough resources!")

    elif brush == 0: # red x removing thing
        cable_delete = False
        if not grid[ry, rx] in ground_blocks:
            if abs(grid[ry,rx]) in [16, 17, 18, 19]:
                cable_delete = True
                
            if grid[ry, rx] in big_tiles:
                if abs(grid[ry,rx]) == 18 and grid_cables[ry,rx] > 0:
                    grid_cables[ry,rx] = 0
                else:
                    index = grid[ry, rx]
                    for y_ in range(blocks_index[index]):
                        for x_ in range(blocks_index[index]):
                            grid, grid_rotation = generate_block(rx + x_, ry + y_, grid, grid_rotation, grid_generation, grid_generation_features)
                            grid_data[ry + y_, rx + x_] = {}

            elif -grid[ry, rx] in big_tiles:
                if abs(grid[ry,rx]) == 18 and grid_cables[ry,rx] > 0:
                    grid_cables[ry,rx] = {}
                else:
                    index = -1 * grid[ry, rx]
                    xlinksboven, ylinksboven = outside_screen_render(rx, ry, grid, grid_rotation, blocks_index,
                                                                    -1 * grid[ry, rx])
                    for y_ in range(ylinksboven, ylinksboven + blocks_index[index]):
                        for x_ in range(xlinksboven, xlinksboven + blocks_index[index]):
                            grid, grid_rotation = generate_block(x_, y_, grid, grid_rotation, grid_generation, grid_generation_features)
                            grid_data[y_, x_] = {}

            else: # 1x1 tile
                grid, grid_rotation = generate_block(rx, ry, grid, grid_rotation, grid_generation, grid_generation_features)
                grid_data[ry, rx] = {}

    if cable_delete:
        cable_locations = np.where(grid_cables > 0) #delete 'floating' cable directions things
        for x in cable_locations[1]:
            for y in cable_locations[0]:
                if not abs(grid[y,x]) in [16,17,18,19]: # not on cable blocks
                    grid_cables[y,x] = 0

    return grid, grid_rotation, grid_data, storage, placeable

class Item:
    def __init__(self, x0, y0, item_type, item_size=item_size):
        self.x = x0
        self.y = y0
        self.vx = 0
        self.vy = 0
        self.item_type = item_type
        self.kapot = False
        self.lengte = item_size
        self.breedte = item_size
        self.split_x = -1
        self.split_y = -1
        self.split_side = 1
        self.floatx = self.x
        self.floaty = self.y

    def beweeg(self, deltaTime):
        self.floatx = self.floatx + self.vx * deltaTime
        self.floaty = self.floaty + self.vy * deltaTime
        self.x = round(self.floatx)
        self.y = round(self.floaty)

    def bepaal_richting(self, grid, grid_rotation, grid_data, storage, craft_data, conveyor_speed, deltaTime,grid_cables,cargo_data,
                        grid_size=grid_size):
        rx_ = self.x / grid_size  # int((self.x+self.vx-grid_size*self.vx-grid_size/20*9*np.sign(self.vx))/grid_size)
        ry_ = self.y / grid_size  # int((self.y+self.vy-grid_size*self.vy-grid_size/20*9*np.sign(self.vy))/grid_size)
        rx = int(rx_)
        ry = int(ry_)
        part_x = rx_ % 1
        part_y = ry_ % 1
        if self.vx < 0:
            part_x = 1 - part_x
        if self.vx == 0 and part_x < 0.49:
            part_x = 1 - part_x
        if self.vy < 0:
            part_y = 1 - part_y
        if self.vy == 0 and part_y < 0.49:
            part_y = 1 - part_y
        volgend_blokje = grid[ry, rx]
        orientatie_blokje = grid_rotation[ry, rx]
        if part_x >= 0.49 and part_y >= 0.49:
            if volgend_blokje not in [3, 4]:
                self.split_x = self.split_y = -1
            if volgend_blokje == 1:  # conveyor
                self.vx = ((2 - orientatie_blokje) % 2) / conveyor_speed[0] * np.sign(2 - orientatie_blokje)
                self.vy = ((orientatie_blokje - 1) % 2) / conveyor_speed[0] * np.sign(orientatie_blokje - 1)
            elif volgend_blokje == 2:  # cross
                self.vx = np.ceil(abs(self.vx)) / conveyor_speed[1] * np.sign(self.vx)
                self.vy = np.ceil(abs(self.vy)) / conveyor_speed[1] * np.sign(self.vy)
            elif volgend_blokje in [3, 4]:  # split-r-l
                if rx != self.split_x or ry != self.split_y:  # on new splitter
                    self.split_x = rx
                    self.split_y = ry
                    grid_data[ry, rx]["split_side"] = (grid_data[ry, rx]["split_side"] + 1) % grid_data[ry, rx]["split_count"]

                    if grid_data[ry, rx]["split_side"] == grid_data[ry, rx]["split_count"] - 1:  # to side
                        self.split_side = 1
                    else:  # straight
                        self.split_side = 0

                if volgend_blokje == 3:
                    orientatie_blokje += self.split_side
                elif volgend_blokje == 4:
                    orientatie_blokje -= self.split_side
                orientatie_blokje = orientatie_blokje % 4
                self.vx = ((2 - orientatie_blokje) % 2) / conveyor_speed[2] * np.sign(2 - orientatie_blokje)
                self.vy = ((orientatie_blokje - 1) % 2) / conveyor_speed[2] * np.sign(orientatie_blokje - 1)

            elif volgend_blokje in [5, 6]:  # sort-r-l
                if grid_data[ry, rx]["sort_item"] == self.item_type:  # go left/right (wanted item)
                    if volgend_blokje == 5:
                        orientatie_blokje += 1
                    elif volgend_blokje == 6:
                        orientatie_blokje -= 1
                    orientatie_blokje %= 4

                # else, go straight (not wanted item)
                self.vx = ((2 - orientatie_blokje) % 2) / conveyor_speed[3] * np.sign(2 - orientatie_blokje)
                self.vy = ((orientatie_blokje - 1) % 2) / conveyor_speed[3] * np.sign(orientatie_blokje - 1)
            elif volgend_blokje == 7:  # highway conveyor
                self.vx = ((2 - orientatie_blokje) % 2) / conveyor_speed[4] * np.sign(2 - orientatie_blokje)
                self.vy = ((orientatie_blokje - 1) % 2) / conveyor_speed[4] * np.sign(orientatie_blokje - 1)
            else:  # not on conveyor
                if volgend_blokje in [-20, 20]:
                    storage[self.item_type] += 1
                elif volgend_blokje in [-15, 15, 16, -16]:  # research thing
                    x_start = max(0,rx - 2)
                    x_end = rx + 1
                    y_start = max(0,ry - 2)
                    y_end = ry + 1
                    grid_cut = grid[y_start:y_end,x_start:x_end]
                    

                    r_corner = np.where(grid_cut == abs(volgend_blokje))
                    if str(self.item_type) in craft_data[max(0,ry - 2) + r_corner[0][0]][max(0,rx - 2) + r_corner[1][0]]:  
                        craft_data[max(0,ry - 2) + r_corner[0][0]][max(0,rx - 2) + r_corner[1][0]][str(self.item_type)] += 1
                    else:
                        craft_data[max(0,ry - 2) + r_corner[0][0]][max(0,rx - 2) + r_corner[1][0]][str(self.item_type)] = 1
                else:
                    storage[self.item_type] -= 1
                self.vx = self.vy = 0
                self.kapot = True

        return storage, craft_data, grid_data, cargo_data

    def teken(self, screen, scale, scaled_pictures, scrollx, scrolly):
        item_margin = 10
        tekenx = int((self.x - int(self.breedte / 2)) * scale + scrollx)
        tekeny = int((self.y - int(self.lengte / 2)) * scale + scrolly)
        screen_x, screen_y = screen.get_size()
        if not (tekenx + item_size + item_margin < 0 or tekeny + item_size + item_margin < 0) and not (
                tekenx + item_size + item_margin > screen_x or tekeny + item_size + item_margin > screen_y):
            screen.blit(scaled_pictures["item_" + str(self.item_type) + "_picture"][0], (
                int((self.x - int(self.breedte / 2)) * scale + scrollx),
            int((self.y - int(self.lengte / 2)) * scale + scrolly)))

class Cargo(Item):
    def __init__(self, x0, y0, cargo_storage, item_size=item_size):
        self.x = x0
        self.y = y0
        self.vx = 0
        self.vy = 0
        self.item_type = 'c' #cargo
        self.kapot = False
        self.lengte = item_size
        self.breedte = item_size
        self.split_x = -1
        self.split_y = -1
        self.split_side = 1
        self.floatx = self.x
        self.floaty = self.y
        self.cargo_storage = cargo_storage

    def bepaal_richting(self, grid, grid_rotation, grid_data, storage, craft_data, conveyor_speed, deltaTime, grid_cables, cargo_data,
                        grid_size=grid_size):
        rx_ = self.x / grid_size
        ry_ = self.y / grid_size
        rx = int(rx_)
        ry = int(ry_)
        part_x = rx_ % 1
        part_y = ry_ % 1
        if self.vx < 0:
            part_x = 1 - part_x
        if self.vx == 0 and part_x < 0.49:
            part_x = 1 - part_x
        if self.vy < 0:
            part_y = 1 - part_y
        if self.vy == 0 and part_y < 0.49:
            part_y = 1 - part_y
        #volgend_blokje = grid_cables[ry, rx]
        #volgend_blokje = 0
        if grid_cables[ry,rx] > 0:
            volgend_blokje = 1
        elif grid[ry,rx] == -17:
            volgend_blokje = 2
        else:
            volgend_blokje = 0
        orientatie_blokje = grid_cables[ry, rx]-1
        if part_x >= 0.49 and part_y >= 0.49:
            if volgend_blokje == 1:  # cable
                self.vx = ((2 - orientatie_blokje) % 2) / conveyor_speed[5] * np.sign(2 - orientatie_blokje)
                self.vy = ((orientatie_blokje - 1) % 2) / conveyor_speed[5] * np.sign(orientatie_blokje - 1)
            elif volgend_blokje == 2: # end of cable
                out_dict = {}
                for x in self.cargo_storage.keys():
                    if x in cargo_data[ry, rx].keys(): #both have same keys: merge
                        val = cargo_data[ry, rx][x] + self.cargo_storage[x]
                        out_dict[x] = val
                    else: # no matching keys: create new
                        out_dict[x] = self.cargo_storage[x]

                x_start = max(0,rx - 2)
                x_end = rx + 1
                y_start = max(0,ry - 2)
                y_end = ry + 1

                grid_cut = grid[y_start:y_end,x_start:x_end]
                r_corner = np.where(grid_cut == 17)
                
                cargo_data[max(0,ry - 2 + r_corner[0][0])][max(0,rx - 2 + r_corner[1][0])] = out_dict
                        
                self.vx = self.vy = 0
                self.kapot = True
            else: # not connected to end
                self.vx = self.vy = 0
                self.kapot = True

        return storage, craft_data, grid_data, cargo_data
            
def draw_tile_menu(screen, data_display, data_arrow, item_names, tile_names, tile_des, rect_info, grid, mrx, mry,
                   grid_data, craft_data):
    def blit_text(surface, rect_info, text, pos, font, color=pg.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = rect_info.get_size()
        max_width -= 23
        x, y = pos
        word_height = 0
        for line in words:
            for word in line:
                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    rect_w, rect_h = rect_info.get_size()
    rect_w -= 10
    width, height = screen.get_size()
    screen.blit(rect_info, (-2, height - rect_h))
    # i_title_font,i_text_font,i_des_font

    arrow_width = data_arrow.get_size()[0]
    arrow_height = data_arrow.get_size()[1]
    up_button = pg.Rect((150, height - rect_h + 133), (arrow_width, arrow_height))  # data editing x and y
    down_button = pg.Rect((151, height - rect_h + 170), (arrow_width, arrow_height))

    # title
    text = i_title_font.render("View Tile Information:", True, (0, 0, 0))
    screen.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 33))
    tile_block = grid[mry, mrx]

    if tile_block in [3, 4, 5, 6]:  # splitters & sorters
        # text for splitters/sorters
        if tile_block in [3, 4]:
            tile_mode = "splitter"
            text1 = i_text_font.render("Edit tile data for splitter:", True, (0, 0, 0))
            text2 = i_des_font.render("Splits item for every " + str(grid_data[mry, mrx]["split_count"] - 1) + " item(s):", True,
                                      (0, 0, 0))
            text3 = i_title_font.render(str(grid_data[mry, mrx]["split_count"] - 1), True, (0, 0, 0))
        else:
            tile_mode = "sorter"
            text1 = i_text_font.render("Edit tile data for sorter:", True, (0, 0, 0))
            text2 = i_des_font.render(f"Sorts {item_names[grid_data[mry, mrx]['sort_item']][1]}.", True, (0, 0, 0))
            text3 = pg.Surface((1,1))

        screen.blit(text1, (int((rect_w - text1.get_size()[0]) / 2), height - rect_h + 65))
        screen.blit(text2, (int((rect_w - text2.get_size()[0]) / 2), height - rect_h + 95))

        # display bit
        screen.blit(data_display, (60, height - rect_h + 140))
        screen.blit(data_arrow, (150, height - rect_h + 133))
        screen.blit(pg.transform.rotate(data_arrow, 180), (151, height - rect_h + 170))

        if tile_block in [3, 4]:  # number for splitter
            screen.blit(text3, (int((rect_w - text3.get_size()[0]) / 2) - 42, height - rect_h + 155))
        elif tile_block in [5, 6]:  # item for sorter
            if grid_data[mry, mrx]["sort_item"] != 0:  # not research item
                screen.blit(pg.transform.scale(unsc_pics["item_" + str(grid_data[mry, mrx]["sort_item"]) + "_picture"], (45, 45)),
                            (80, height - rect_h + 145))
            else:
                screen.blit(pg.transform.scale(r_icon_picture, (43, 43)), (80, height - rect_h + 146))
        # x,y
        text = i_des_font.render("Tile at x: " + str(mrx) + ", y: " + str(mry), True, (0, 0, 0))
        screen.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 215))
        # type
        text = i_des_font.render("Item type: " + str(tile_names[abs(tile_block)]), True, (0, 0, 0))
        screen.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 245))
        # descrition
        blit_text(screen, rect_info, str(tile_des[abs(tile_block)]), (25, height - rect_h + 275), i_des_font)

    elif tile_block in [15, -15]:
        tile_mode = ""  # no tile mode
        text1 = i_text_font.render("Edit tile data via Edit Mode:", True, (0, 0, 0))
        if grid_data[mry, mrx]['craft_recipe'] != 0:
            text2 = i_des_font.render(f"Crafts {item_names[grid_data[mry, mrx]['craft_recipe']][1]}.", True, (0, 0, 0))
        else:
            text2 = i_des_font.render(f"No recipe selected.", True, (0, 0, 0))
        text3 = i_des_font.render("Select a recipe via the Edit Mode", True, (0, 0, 0))
        text4 = i_des_font.render("(click the edit icon or press F2)", True, (0, 0, 0))

        screen.blit(text1, (int((rect_w - text1.get_size()[0]) / 2), height - rect_h + 65))
        screen.blit(text2, (int((rect_w - text2.get_size()[0]) / 2), height - rect_h + 95))
        screen.blit(text3, (int((rect_w - text3.get_size()[0]) / 2), height - rect_h + 125))
        screen.blit(text4, (int((rect_w - text4.get_size()[0]) / 2), height - rect_h + 150))

        # x,y
        text = i_des_font.render("Tile at x: " + str(mrx) + ", y: " + str(mry), True, (0, 0, 0))
        screen.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 215))
        # type
        text = i_des_font.render("Item type: " + str(tile_names[abs(tile_block)]), True, (0, 0, 0))
        screen.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 245))
        # descrition
        blit_text(screen, rect_info, str(tile_des[abs(tile_block)]), (25, height - rect_h + 275), i_des_font)


    else:  # no info to edit, show defeault info
        tile_mode = ""  # no tile mode
        text = i_text_font.render("No information to edit.", True, (0, 0, 0))
        screen.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 65))
        # x,y
        text = i_des_font.render("Tile at x: " + str(mrx) + ", y: " + str(mry), True, (0, 0, 0))
        screen.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 95))
        # type
        text = i_des_font.render("Item type: " + str(tile_names[abs(tile_block)]), True, (0, 0, 0))
        screen.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 125))
        # descrition
        blit_text(screen, rect_info, str(tile_des[abs(tile_block)]), (25, height - rect_h + 155), i_des_font)

    return tile_mode, up_button, down_button  # buttons = pg.Rect of buttons (collidepoint)

def draw_edit_menu(tile_menu_type, unlocked_recipes, craft_scrolly, item_names, creater_unlocked_recipes, creater_type, hover_recipe=-1):
    edit_menu_surf = pg.Surface(edit_mode_menu_picture.get_size(), pg.SRCALPHA)
    edit_menu_surf.blit(edit_mode_menu_picture, (0, 0))

    crafter_btn_collidepoints = []

    craft_buffer = 5
    temp_surf = pg.Surface(craft_select_menu_picture.get_size(), pg.SRCALPHA)

    #buttons
    if tile_menu_type == "crafter":
        loop_recipes = unlocked_recipes # select random as recipe 
    else:
        loop_recipes = ["Random"]
        loop_recipes.extend(creater_unlocked_recipes[creater_type])

    for n, recipe in enumerate(loop_recipes):
        btn_y = craft_scrolly + n * (craft_select_btn_picture.get_height() + craft_buffer)
        if temp_surf.get_height() >= btn_y >= -craft_select_btn_picture.get_height():
            if recipe == hover_recipe:
                temp_surf.blit(craft_select_btn_hover_picture, ((temp_surf.get_width() - craft_select_btn_picture.get_width()) / 2, btn_y))
            else:
                temp_surf.blit(craft_select_btn_picture, ((temp_surf.get_width() - craft_select_btn_picture.get_width()) / 2, btn_y))
            
            topleft = ((temp_surf.get_width() - craft_select_btn_picture.get_width()) / 2, btn_y)
            color_size = 110
 
            if tile_menu_type == "crafter":
                color = recipes[str(recipe)]["color"]

                requirements = {}
                for item in recipes[str(recipe)]["recipe"]: #loops through for ex.: [1,2,2]
                    if not item in requirements: 
                        requirements[item] = 1 
                    else:
                        requirements[item] += 1

                color_pic = crafter_picture_colors[color][0]
                color_pic = pg.transform.scale(color_pic, (color_size, color_size))

                temp_surf.blit(color_pic, ((temp_surf.get_width() - craft_select_btn_picture.get_width()) / 2 + (craft_select_btn_picture.get_height() - color_size) / 2 + 10, topleft[1] + (craft_select_btn_picture.get_height() - color_size) / 2))

            if recipe != "Random":
                item_pic = unsc_pics[f"item_{recipe}_picture"]
            else:
                item_pic = unsc_pics[f"item_random_picture"]

            item_size = 50
            item_pic = pg.transform.scale(item_pic, (item_size, item_size))

            temp_surf.blit(item_pic, ((temp_surf.get_width() - craft_select_btn_picture.get_width()) / 2 + (craft_select_btn_picture.get_height() - item_size) / 2 + 10, topleft[1] + (craft_select_btn_picture.get_height() - item_size) / 2))

            surf_w, surf_h = edit_menu_surf.get_size()    
            add_x, add_y = (surf_w - temp_surf.get_width()) / 2, int((surf_h - temp_surf.get_height()) / 1.5)
            
            if tile_menu_type == "crafter":
                recipe_text = edit_tile_font_small.render(str(item_names[recipe][0]), True, (0, 0, 0))
                if recipe_text.get_width() > craft_select_btn_picture.get_width() - 70 - item_size:
                    recipe_text = edit_tile_font_small_small.render(str(item_names[recipe][0]), True, (0, 0, 0))

                y_blit = topleft[1] + 30
                if len(requirements) > 4:
                    y_blit = topleft[1] + 18

                temp_surf.blit(recipe_text, ((temp_surf.get_width() - craft_select_btn_picture.get_width()) / 2 + (craft_select_btn_picture.get_height() - item_size) / 2 + color_size - 15, y_blit))

                x_blit = (temp_surf.get_width() - craft_select_btn_picture.get_width()) / 2 + (craft_select_btn_picture.get_height() - item_size) / 2 + color_size - 15
                y_blit = topleft[1] + 65
                if len(requirements) > 4:
                    y_blit = topleft[1] + 50

                for item in requirements.keys():
                    if x_blit > (temp_surf.get_width() - craft_select_btn_picture.get_width()) / 2 + craft_select_btn_picture.get_width() - 30:
                        x_blit = (temp_surf.get_width() - craft_select_btn_picture.get_width()) / 2 + (craft_select_btn_picture.get_height() - item_size) / 2 + color_size - 15
                        y_blit += 30
                    item_pic = unsc_pics[f"item_{item}_picture"]
                    item_pic_size = 30
                    item_pic = pg.transform.scale(item_pic, (item_pic_size, item_pic_size))

                    temp_surf.blit(item_pic, (x_blit, y_blit))

                    x_blit += item_pic_size + 3

                    req_text = edit_tile_font_item.render(str(requirements[item]), True, (0, 0, 0))
                    temp_surf.blit(req_text, (x_blit, y_blit))

                    x_blit += edit_tile_font_item.size(str(requirements[item]))[0] + 7

            elif tile_menu_type == "creater":
                if recipe != "Random":
                    recipe_text = edit_tile_font_small.render(str(item_names[recipe][0]), True, (0, 0, 0))
                else:
                    recipe_text = edit_tile_font_small.render("Random", True, (0, 0, 0))

                if recipe_text.get_width() > craft_select_btn_picture.get_width() - 70 - item_size:
                    recipe_text = edit_tile_font_small_small.render(str(item_names[recipe][0]), True, (0, 0, 0))

                y_blit = topleft[1] + 45
                temp_surf.blit(recipe_text, ((temp_surf.get_width() - craft_select_btn_picture.get_width()) / 2 + (craft_select_btn_picture.get_height() - item_size) / 2 + color_size - 15, y_blit))

            crafter_btn_collidepoints.append(
                [pg.Rect(((temp_surf.get_width() - craft_select_btn_picture.get_width()) / 2 + add_x, btn_y + add_y), (craft_select_btn_picture.get_width(),craft_select_btn_picture.get_height())),
                    recipe])

    temp_surf.blit(craft_select_menu_border_picture, (0,0))
    surf_w, surf_h = edit_menu_surf.get_size()    
    edit_menu_surf.blit(temp_surf, ((surf_w - temp_surf.get_width()) / 2, int((surf_h - temp_surf.get_height()) / 1.5)))

    recipe_text = edit_tile_font.render("Select recipe", True, (0, 0, 0))
    edit_menu_surf.blit(recipe_text, ((surf_w - recipe_text.get_width()) / 2, 45))

    line_1 =  int((surf_h - temp_surf.get_height()) / 1.5)
    line_2 =  int((surf_h - temp_surf.get_height()) / 1.5) + temp_surf.get_height()

    edit_menu_surf.set_alpha(230)
    return edit_menu_surf, crafter_btn_collidepoints, line_1, line_2

def blit_tile_edit_menu(screen, edit_menu_surf, crafter_btn_collidepoints, line_1_basis, line_2_basis, update=True):
    scr_w, scr_h = screen.get_size()
    screen.blit(edit_menu_surf, ((scr_w - edit_menu_surf.get_width()) / 2, (scr_h - edit_menu_surf.get_height()) / 2))

    x_add, y_add = (scr_w - edit_menu_surf.get_width()) / 2, (scr_h - edit_menu_surf.get_height()) / 2

    if update:
        new_list = []
        for i, btn_obj in enumerate(crafter_btn_collidepoints):
            btn = btn_obj[0]
            new_list.append([pg.Rect((btn.x + x_add, btn.y + y_add),(btn.w, btn.h)), btn_obj[1]])

        line_1 = line_1_basis + (scr_h - edit_menu_surf.get_height()) / 2
        line_2 = line_2_basis + (scr_h - edit_menu_surf.get_height()) / 2
        
        return pg.Rect(((scr_w - edit_menu_surf.get_width()) / 2, (scr_h - edit_menu_surf.get_height()) / 2), (edit_menu_surf.get_width(), edit_menu_surf.get_height())), new_list, line_1, line_2
    else:
        return pg.Rect(((scr_w - edit_menu_surf.get_width()) / 2, (scr_h - edit_menu_surf.get_height()) / 2), (edit_menu_surf.get_width(), edit_menu_surf.get_height())), crafter_btn_collidepoints

def update_recipe(grid,grid_data,hover_recipe,x,y, blocks_index, creater_type, update=""):
    blocks_type = 15 if update == "crafter" else creater_type
    tile_size = blocks_index[blocks_type]

    if grid[y, x] == blocks_type:
        for x_loop in range(x, x+tile_size):
            for y_loop in range(y, y+tile_size):
                if update == "crafter":
                    grid_data[y_loop, x_loop]["craft_recipe"] = hover_recipe
                elif update == "creater":
                    grid_data[y_loop, x_loop]["selected_item"] = hover_recipe

    elif grid[y, x] == -blocks_type:
        #find the topleft of block to change recipe there
        if x > blocks_index[blocks_type] and y > blocks_index[blocks_type]:
            cut = grid[y - blocks_index[blocks_type] + 1:y + 1, x - blocks_index[blocks_type] + 1:x + 1]
            dx = x - blocks_index[blocks_type] + 1
            dy = y - blocks_index[blocks_type] + 1
        elif x >= blocks_index[blocks_type] and y >= blocks_index[blocks_type]:
            cut = grid[y - blocks_index[blocks_type] + 1:y + 1, x - blocks_index[blocks_type] + 1:x + 1]
            dx = x - blocks_index[blocks_type] + 1
            dy = y - blocks_index[blocks_type] + 1
        else:  # on edge of grid
            if not x >= blocks_index[blocks_type] and (y >= blocks_index[blocks_type]):
                cut = grid[y - blocks_index[blocks_type] + 1:y + 1, 0:x + 1]
                dx = 0
                dy = y - blocks_index[blocks_type] + 1
            elif (x >= blocks_index[blocks_type]) and not y >= blocks_index[blocks_type]:
                cut = grid[0:y + 1, x - blocks_index[blocks_type] + 1:x + 1]
                dx = x - blocks_index[blocks_type] + 1
                dy = 0
            else:  # cornered
                cut = grid[0:y + 1, 0:x + 1]
                dx = 0
                dy = 0

        linksboven = np.where(cut == blocks_type)
        x_ = dx + linksboven[1][0]
        y_ = dy + linksboven[0][0]

        for x_loop in range(x_, x_+tile_size):
            for y_loop in range(y_, y_+tile_size):
                if update == "crafter":
                    grid_data[y_loop, x_loop]["craft_recipe"] = hover_recipe
                elif update == "creater":
                    grid_data[y_loop, x_loop]["selected_item"] = hover_recipe

    return grid_data

def draw_keybind_menu(screen, k_scrolly, unlocked_blocks, data_display, data_arrow, rect_keybinds, keybinds):
    rect_w, rect_h = rect_keybinds.get_size()
    rect_w -= 10
    width, height = screen.get_size()
    screen.blit(rect_keybinds, (-2, height - rect_h + k_scrolly))
    # i_title_font,i_text_font,i_des_font
    conveyor_arrow_dict = {'1': 'picture_arrow', '2': 'picture_arrow_cross', '3': 'picture_arrow_split_r',
                           '4': 'picture_arrow_split_l', '5': 'picture_arrow_sort_r', '6': 'picture_arrow_sort_l',
                           '7': 'picture_arrow_highway'}

    arrow_width = data_arrow.get_size()[0]
    arrow_height = data_arrow.get_size()[1]
    up_button = pg.Rect((150, height - rect_h + 133), (arrow_width, arrow_height))  # keybind editing x and y
    down_button = pg.Rect((151, height - rect_h + 170), (arrow_width, arrow_height))

    # title
    text = i_title_font.render("Edit Key Shortcuts:", True, (0, 0, 0))
    screen.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 33 + k_scrolly))

    # list of keys with numbers and stuff
    key_distance = 73
    up_button = {}
    down_button = {}
    for k_index, k_item in enumerate(keybinds):
        # display bit
        screen.blit(data_display, (90, height - rect_h + 70 + k_index * key_distance + k_scrolly))

        # pint("picture_"+str(keybinds[k_index]))
        screen.blit(pg.transform.smoothscale(unsc_pics["picture_" + str(keybinds[k_index])], (50, 50)),
                    (107, height - rect_h + 73 + k_index * key_distance + k_scrolly))
        if str(keybinds[k_index]) in list(conveyor_arrow_dict.keys()):
            screen.blit(pg.transform.scale(eval(conveyor_arrow_dict[str(keybinds[k_index])]), (50, 50)),
                        (107, height - rect_h + 73 + k_index * key_distance + k_scrolly))

        screen.blit(data_arrow, (180, height - rect_h + 63 + k_index * key_distance + k_scrolly))
        screen.blit(pg.transform.rotate(data_arrow, 180),
                    (181, height - rect_h + 100 + k_index * key_distance + k_scrolly))
        up_button[k_index] = pg.Rect((180, height - rect_h + 63 + k_index * key_distance + k_scrolly),
                                     (arrow_width, arrow_height))  # keybind editing x and y
        down_button[k_index] = pg.Rect((181, height - rect_h + 100 + k_index * key_distance + k_scrolly),
                                       (arrow_width, arrow_height))

        text = i_title_font.render(str(k_index) + ":", True, (0, 0, 0))
        screen.blit(text, (55, height - rect_h + 90 + k_index * key_distance + k_scrolly))

    return up_button, down_button  # buttons = list of pg.Rect buttons (collidepoint)

def draw_info_popup(screen,mx,my,menu_pictures,clicked_icon,clicked_button,tile_names,b_prices,info_ui,item_names,tile_des):
    def blit_text(surface, max_w, text, pos, font, color=pg.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width = max_w - 10 #margin val
        #max_width -= 23
        x, y = pos
        word_height = 0
        for line in words:
            for word in line:
                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    #draw box
    w, h = info_ui.get_size()
    scr_w, scr_h = screen.get_size()
    if mx + w > scr_w:
        blit_x = mx - w
    else:
        blit_x = mx
    blit_y =  my - h
    screen.blit(info_ui,(blit_x,blit_y))
    tile_hover = tile_names[menu_pictures[clicked_icon][clicked_button]]
    
    #draw title
    screen.blit(i_title_font.render(str(tile_hover),True,(0,0,0)),(blit_x + 15, blit_y + 5))

    #draw building price
    height_text = 0
    b_price_list = b_prices[menu_pictures[clicked_icon][clicked_button]]
    x_start = 15
    b_price_blit_y = blit_y + i_title_font.size("Test")[1] + 10
    for b_material in b_price_list.keys():
        item_type = item_names[0].index(b_material) # in numbers
        item_quantity = b_price_list[b_material]
        item_pic = unsc_pics["item_"+str(item_type)+"_picture"]
        item_pic_size = item_pic.get_width() #width and height are the same
        screen.blit(item_pic,(blit_x+x_start,b_price_blit_y))
        x_start += item_pic_size + 5
        screen.blit(i_des_font.render(str(item_quantity),True,(0,0,0)),(blit_x+x_start,b_price_blit_y))
        width_text, height_text = i_des_font.size(str(item_quantity))
        x_start += width_text + 10
    
    #draw description
    blit_text(screen,blit_x + w,tile_des[menu_pictures[clicked_icon][clicked_button]],(blit_x + 10, b_price_blit_y + height_text + 10),i_text_font,(0,0,0))


def draw_tile_mode_menu(screen, tile_mode):
    match tile_mode:
        case "place":
            img = tile_info_menu_1
        case "edit":
            img = tile_info_menu_2
        case "info":
            img = tile_info_menu_3
        case "view": 
            img = tile_info_menu_4
    margin_screen = 10
    screen.blit(img, (screen.get_width() - img.get_width() - margin_screen, margin_screen))
    tile_mode_btns = []
    for i, mode in enumerate(["place", "edit", "info", "view"]):
        tile_mode_btns.append([pg.Rect((screen.get_width() - img.get_width() - margin_screen + i * 50 ,margin_screen),(50,50)), mode])
    edit_tile_menu_rect = pg.Rect((screen.get_width() - img.get_width() - margin_screen, margin_screen), (tile_menu_w, tile_menu_h))
    return tile_mode_btns,edit_tile_menu_rect


def teken_menu(screen, conveyor_research_progress_dict, research_progress, menu_pictures, open_menu, clicked_icon,
               clicked_button, menu_scrollx, scaled_pictures, b_prices,creater_unlocked_recipes):
    # bar
    width, height = screen.get_size()
    if open_menu:
        ratio_menu = 1 / 6
        bar_height = int(height * ratio_menu)
        bar_width = width
        screen.blit(pg.transform.scale(menu_bar_picture, (bar_width, bar_height)), (0, height - bar_height))
    else:
        bar_height = 0
        bar_width = width
    # buy buttons
    button_margin = 25
    button_click_list = []
    button_distance = bar_height
    button_width = bar_height - button_margin
    if open_menu:

        conveyor_arrow_dict = {'picture_1': 'picture_arrow', 'picture_2': 'picture_arrow_cross',
                               'picture_3': 'picture_arrow_split_r', 'picture_4': 'picture_arrow_split_l',
                               'picture_5': 'picture_arrow_sort_r', 'picture_6': 'picture_arrow_sort_l',
                               'picture_7': 'picture_arrow_highway'}
        index_for_research_progress_dict = {1:1,2:2,3:3,4:4,5:5,6:6,7:7,16:8,17:8,18:8}
        
        for button in range(len(menu_pictures[clicked_icon])):
            button_click_list.append([button_distance * button + int(button_margin / 2) - menu_scrollx,
                                      height - bar_height + int(button_margin / 2)])
            if clicked_button == button:
                screen.blit(pg.transform.scale(button_clicked_picture,
                                               (int(bar_height - button_margin), int(bar_height - button_margin))), (
                            button_distance * button + int(button_margin / 2) - menu_scrollx,
                            height - bar_height + int(button_margin / 2)))
            else:
                screen.blit(pg.transform.scale(button_unclicked_picture,
                                               (int(bar_height - button_margin), int(bar_height - button_margin))), (
                            button_distance * button + int(button_margin / 2) - menu_scrollx,
                            height - bar_height + int(button_margin / 2)))

        button = 0
        picture_margin = 20
        for index, scaled_picture in list(sorted(enumerate(list(scaled_pictures.keys())))):
            do_continue = True
            for i in range(len(menu_pictures[clicked_icon])):
                if "picture_" + str(menu_pictures[clicked_icon][i]) == scaled_picture and not 'item' in scaled_picture:
                    do_continue = False
                    break

            if do_continue:
                continue

            screen.blit(pg.transform.scale(unsc_pics[scaled_picture], (
                int(bar_height - button_margin - picture_margin), int(bar_height - button_margin - picture_margin))), (
                            button_distance * button + int(button_margin / 2) - menu_scrollx + int(picture_margin / 2),
                            height - bar_height + int(button_margin / 2) + int(picture_margin / 2)))
            
            if clicked_icon == 0:
                if scaled_picture in conveyor_arrow_dict:
                    screen.blit(pg.transform.scale(eval(conveyor_arrow_dict[scaled_picture]), (
                    int(bar_height - button_margin - picture_margin), int(bar_height - button_margin - picture_margin))), (
                                button_distance * button + int(button_margin / 2) - menu_scrollx + int(picture_margin / 2),
                                height - bar_height + int(button_margin / 2) + int(picture_margin / 2)))

                if research_progress[clicked_icon][conveyor_research_progress_dict[index_for_research_progress_dict[index]]] < 0:
                    screen.blit(pg.transform.scale(lock_picture, (
                    int(bar_height - button_margin - picture_margin), int(bar_height - button_margin - picture_margin))), (
                                button_distance * button + int(button_margin / 2) - menu_scrollx + int(picture_margin / 2),
                                height - bar_height + int(button_margin / 2) + int(picture_margin / 2)))

            elif clicked_icon in [1,2,3]: #creater research icons, draw lock when not unlocked yet
                block = scaled_picture[8:]
                try:
                    if not int(block) in creater_unlocked_recipes: #locked 
                        screen.blit(pg.transform.scale(lock_picture, (
                        int(bar_height - button_margin - picture_margin), int(bar_height - button_margin - picture_margin))), (
                                    button_distance * button + int(button_margin / 2) - menu_scrollx + int(picture_margin / 2),
                                    height - bar_height + int(button_margin / 2) + int(picture_margin / 2)))
                except Exception as e:
                    print(e)
            
            
            button += 1

    # tab buttons
    buttons = 6  # button count
    button_distance = 75
    icon_click_list = []  # pos icons
    for icon in range(buttons):
        icon_click_list.append([(icon * button_distance) + int((bar_width - (buttons * button_distance)) / 2),
                                height - bar_height - button_distance])
        if clicked_icon == icon:
            screen.blit(icon_clicked_picture, (
            (icon * button_distance) + int((bar_width - (buttons * button_distance)) / 2),
            height - bar_height - button_distance))
        else:
            screen.blit(icon_unclicked_picture, (
            (icon * button_distance) + int((bar_width - (buttons * button_distance)) / 2),
            height - bar_height - button_distance))
        if icon in [0, 1, 2, 3, 4, 5]:
            screen.blit(eval("icon_" + str(icon + 1)), (
            (icon * button_distance) + int((bar_width - (buttons * button_distance)) / 2),
            height - bar_height - button_distance))
    return icon_click_list, bar_width, bar_height, button_distance, button_click_list, button_width


def render_images(screen, new, not_enough_picture=not_enough_picture, rect_keybinds=rect_keybinds, data_display=data_display, data_arrow=data_arrow, rect_info=rect_info, rect_ui=rect_ui, research_button_clicked=research_button_clicked, research_button_unclicked=research_button_unclicked, research_display=research_display,info_ui=info_ui):
    width, height = screen.get_size()
    rect_info = pg.transform.scale(rect_info, (300, 400))
    rect_info.set_alpha(235)
    rect_keybinds = pg.transform.scale(rect_keybinds, (300, 800))
    rect_keybinds.set_alpha(235)
    rect_ui = pg.transform.scale(rect_ui, (width, height))
    research_button_clicked = pg.transform.scale(research_button_clicked, (200, 100))
    research_button_unclicked = pg.transform.scale(research_button_unclicked, (200, 100))
    research_display = pg.transform.scale(research_display, (200, 100))
    research_display.set_alpha(210)
    not_enough_picture = pg.transform.scale(not_enough_picture, (
    int(width / 2), int((int(width / 2)) / not_enough_picture.get_width() * not_enough_picture.get_height())))
    if new:
        data_display = pg.transform.scale(data_display,
                                          (int(data_display.get_size()[0] / 3), int(data_display.get_size()[1] / 3)))
        data_arrow = pg.transform.scale(data_arrow,
                                        (int(data_arrow.get_size()[0] / 7), int(data_arrow.get_size()[1] / 7)))
    info_ui = pg.transform.scale(info_ui,(300,200))
    return not_enough_picture, rect_keybinds, data_display, data_arrow, rect_info, rect_ui, research_button_clicked, research_button_unclicked, research_display,info_ui


def update_r_screen_func(screen, rect_ui):
    r_screen_transparent = pg.Surface(screen.get_size())
    r_screen_transparent.blit(rect_ui,(0,0))
    r_screen_transparent.set_alpha(150)
    return r_screen_transparent


def draw_research(screen, r_points, r_screen, rect_ui, r_scrollx, r_scrolly, research_display, research_button_clicked,
                  research_button_unclicked, research_progress, research_text, r_tile_text, research_subtext, r_prices, r_screen_page, research_grid, creater_unlocked_recipes):
    width, height = screen.get_size()
    creater_menu_collidepoints = [] # creater menu button collidepoints are stored here

    if r_screen_page == 0: # conveyor research menu
        #screen.blit(rect_ui, (0, 0))  # background
        button_space_x = 50
        button_space_y = 25
        button_size_x, button_size_y = research_button_clicked.get_size()
        button_dist_x = button_space_x + button_size_x
        button_dist_y = button_space_y + button_size_y

        # buttons & lines
        for category in range(len(research_progress)):  # per category
            for row in range(len(research_progress[category])):  # per row per category
                if not research_progress[category][max(row - 1, 0)] < 0:
                    if (not row == len(research_progress[category]) - 1) and (
                            research_progress[category][row] > -1):  # if not last item, no line
                        pg.draw.line(r_screen, (40, 140, 144),
                                    (int(button_size_x / 2) - r_scrollx, row * button_dist_y + button_size_y - r_scrolly),
                                    (int(button_size_x / 2) - r_scrollx, row * button_dist_y + button_dist_y - r_scrolly),
                                    width=5)
                    for button in range(research_progress[category][row] + 2):
                        if not button == research_progress[category][row] + 1:  # not last item, draw line
                            if not button == 5:  # not last item, max research
                                pg.draw.line(r_screen, (40, 140, 144), (
                                button * button_dist_x + button_size_x - 5 - r_scrollx,
                                row * button_dist_y + int(button_size_y / 2) - r_scrolly), (
                                            button * button_dist_x + button_dist_x + 5 - r_scrollx,
                                            row * button_dist_y + int(button_size_y / 2) - r_scrolly), width=5)
                            r_screen.blit(research_button_clicked,
                                        (button * button_dist_x - r_scrollx, row * button_dist_y - r_scrolly))
                        else:  # last item, unclicked
                            if not button > 5:  # not max research item
                                r_screen.blit(research_button_unclicked,
                                            (button * button_dist_x - r_scrollx, row * button_dist_y - r_scrolly))
                        if not button > 5:  # text and icon thingies
                            r_screen.blit(r_title_font.render(str(research_text[0][button]), True, (0, 0, 0)),
                                        (button * button_dist_x + 10 - r_scrollx, row * button_dist_y + 8 - r_scrolly))
                            r_screen.blit(r_subtitle_font.render(str(r_tile_text[0][row]), True, (0, 0, 0)),
                                        (button * button_dist_x + 10 - r_scrollx, row * button_dist_y + 29 - r_scrolly))
                            r_screen.blit(r_font.render(str(research_subtext[0][button]), True, (0, 0, 0)),
                                        (button * button_dist_x + 10 - r_scrollx, row * button_dist_y + 50 - r_scrolly))
                            r_screen.blit(r_icon_picture, (
                            button * button_dist_x + button_size_x - 105 - r_scrollx, row * button_dist_y + 3 - r_scrolly))
                            r_screen.blit(r_font.render(str(r_prices[row][button]), True, (0, 0, 0)), (
                            button * button_dist_x + button_size_x - 75 - r_scrollx, row * button_dist_y + 9 - r_scrolly))
    
    elif r_screen_page in [1,2,3]: # creater research menu (creater research menus farm, water and mining)
        creater_unlocked_recipes_keys = sorted(list(creater_unlocked_recipes.keys()))
        unlocked_creaters = [] # all of the creaters (blocks that produce items periodically) that are unlocked for the currently viewed research screen
        for creater in creater_btn_order[str(r_screen_page)].keys():
            if int(creater) in creater_unlocked_recipes_keys:
                unlocked_creaters.append(int(creater))
        unlocked_creaters = sorted(unlocked_creaters)
        
        topleft_margin = 10
        #research_creater_btn_clicked
        crtr_btn_w, crtr_btn_h = research_creater_btn.get_size()
        item_btn_w, item_btn_h = research_creater_item_btn.get_size()
        margin_w = 30
        margin_h = 25
        margin_h_creater_item = 50
        line_width = 15
        line_width_items = 10

        creater_size = research_creater_btn.get_width() - 90
        item_size = research_creater_item_btn.get_width() - 90

        r_size = r_icon_picture.get_width() # for the cost display
        margin_r_price = 5 # distance between r_icon and the cost text

        item_btn_add_w = (crtr_btn_w - item_btn_w) / 2

        #draw the "thicc" first line horizontally
        pos_left = (topleft_margin + crtr_btn_w / 2, topleft_margin + crtr_btn_h / 2)
        num_of_creaters_unlocked = len(unlocked_creaters)
        if num_of_creaters_unlocked == len(creater_btn_order[str(r_screen_page)]): # research of items is maxed
            num_of_creater_btns = num_of_creaters_unlocked
        else: # research of items is not maxed so draw an additional line for purchase option next item
            num_of_creater_btns = num_of_creaters_unlocked + 1
        pos_right = (topleft_margin + (crtr_btn_w + margin_w) * num_of_creater_btns - crtr_btn_w / 2, topleft_margin + crtr_btn_h / 2)
        pg.draw.line(r_screen, (40, 140, 144), pos_left, pos_right, width=line_width)

        #draw the rest of the vertical lines
        for i, unlocked_creater in enumerate(unlocked_creaters):
            pos_top = (topleft_margin + (crtr_btn_w + margin_w) * i + (crtr_btn_w / 2), topleft_margin + (crtr_btn_h / 2))

            num_of_items_unlocked = len(creater_unlocked_recipes[unlocked_creater])
            if num_of_items_unlocked == len(creater_btn_order[str(r_screen_page)][str(unlocked_creater)]): # research of items is maxed
                num_of_items_btns = num_of_items_unlocked
            else: # research of items is not maxed so draw an additional line for purchase option next item
                num_of_items_btns = num_of_items_unlocked + 1
            pos_bottom = (topleft_margin + (crtr_btn_w + margin_w) * i + (crtr_btn_w / 2), topleft_margin + crtr_btn_h + margin_h_creater_item + num_of_items_btns * (item_btn_h + margin_h) - item_btn_h / 2)

            pg.draw.line(r_screen, (40, 140, 144), pos_top, pos_bottom, width=line_width_items)

        #draw the buttons
        for i, unlocked_creater in enumerate(unlocked_creaters):
            #draw the button
            btn_rect = r_screen.blit(research_creater_btn_clicked, (topleft_margin + (crtr_btn_w + margin_w) * i, topleft_margin))
            #draw the block on the button
            creater_pic = unsc_pics[f"picture_{unlocked_creater}"]
            creater_pic = pg.transform.scale(creater_pic, (creater_size, creater_size))
            r_screen.blit(creater_pic, (topleft_margin + (crtr_btn_w + margin_w) * i + (crtr_btn_w - creater_size) / 2, topleft_margin + (crtr_btn_w - creater_size) / 2 + 10))
            #render the "price tag" text
            price = creater_prices[str(unlocked_creater)][0]
            price_img = r_font.render(str(price), True, (0,0,0))
            price_img_w, price_img_h = price_img.get_size()
            #calculate coords for blit(s)
            topleft = (topleft_margin + (crtr_btn_w + margin_w) * i, topleft_margin) # relative to current btn
            blit_y = topleft[1] + 20
            total_size = r_size + margin_r_price + price_img_w # total width of "price tag"
            r_blit_x = (crtr_btn_w - total_size) / 2 # in the middle
            text_blit_x = r_blit_x + r_size + margin_r_price
            #blit research icon
            r_screen.blit(r_icon_picture, (topleft[0] + r_blit_x, blit_y))
            #blit text
            r_screen.blit(price_img, (topleft[0] + text_blit_x, blit_y + 6)) # 3px offset because of font
            #check for extra trailing item at the end (if not research maxed)
            unlocked_items = copy.deepcopy(creater_unlocked_recipes[int(unlocked_creater)]) # items that are unlocked for this specific creater
            num_of_items_unlocked = len(creater_unlocked_recipes[unlocked_creater])
            #add to list of collidepoints so its easier to handle clicks in main loop
            creater_menu_collidepoints.append([btn_rect, "creater", unlocked_creater, True, int(price)])
            
            if num_of_items_unlocked < len(creater_btn_order[str(r_screen_page)][str(unlocked_creater)]): # research of items is NOT maxed
                unlocked_items.append(creater_btn_order[str(r_screen_page)][str(unlocked_creater)][num_of_items_unlocked])

            for j, unlocked_item in enumerate(unlocked_items):
                #draw btn
                locked = j == len(creater_unlocked_recipes[int(unlocked_creater)])

                if locked:
                    btn_rect = r_screen.blit(research_creater_item_btn, (topleft_margin + (crtr_btn_w + margin_w) * i + item_btn_add_w, topleft_margin + crtr_btn_h + margin_h_creater_item + j * (item_btn_h + margin_h)))
                else:
                    btn_rect = r_screen.blit(research_creater_item_btn_clicked, (topleft_margin + (crtr_btn_w + margin_w) * i + item_btn_add_w, topleft_margin + crtr_btn_h + margin_h_creater_item + j * (item_btn_h + margin_h)))

                #draw item on btn
                item_pic = unsc_pics[f"item_{int(unlocked_item)}_picture"]
                item_pic = pg.transform.scale(item_pic, (item_size, item_size))
                r_screen.blit(item_pic, (topleft_margin + (crtr_btn_w + margin_w) * i + item_btn_add_w + (item_btn_w - item_size) / 2, topleft_margin + crtr_btn_h + margin_h_creater_item + j * (item_btn_h + margin_h) + (item_btn_w - item_size) / 2 + 15))
                #render the "price tag" text
                price = creater_prices[str(unlocked_creater)][j+1] # see creater_prices.json
                price_img = r_font.render(str(price), True, (0,0,0))
                price_img_w, price_img_h = price_img.get_size()
                #calculate coords for blit(s)
                topleft = (topleft_margin + (crtr_btn_w + margin_w) * i + item_btn_add_w, topleft_margin + crtr_btn_h + margin_h_creater_item + j * (item_btn_h + margin_h)) # relative to current btn
                blit_y = topleft[1] + 20
                total_size = r_size + margin_r_price + price_img_w # total width of "price tag"
                r_blit_x = (item_btn_w - total_size) / 2 # in the middle
                text_blit_x = r_blit_x + r_size + margin_r_price
                #blit research icon
                r_screen.blit(r_icon_picture, (topleft[0] + r_blit_x, blit_y))
                #blit text
                r_screen.blit(price_img, (topleft[0] + text_blit_x, blit_y + 6)) # 3px offset because of font
                #add to collidepoints and data for handeling clicks
                creater_menu_collidepoints.append([btn_rect, "item", unlocked_item, not locked, int(price), unlocked_creater])

        #extra creater button at the end if research on that point is not maxed completely.
        if num_of_creaters_unlocked < len(creater_btn_order[str(r_screen_page)]): # not maxed so draw another creater button at the end
            btn_rect = r_screen.blit(research_creater_btn, (topleft_margin + (crtr_btn_w + margin_w) * len(unlocked_creaters), topleft_margin))

            #find the tile that should be blit on the creater research button
            if unlocked_creaters == []:
                keys_btn_order = list(creater_btn_order[str(r_screen_page)].keys())
                key_ununlocked = keys_btn_order[0]
            else:
                last_unlocked_creater = unlocked_creaters[-1]
                keys_btn_order = list(creater_btn_order[str(r_screen_page)].keys())
                index_last_unlocked = keys_btn_order.index(str(last_unlocked_creater))
                key_ununlocked = keys_btn_order[index_last_unlocked + 1]

            #actually blit it (and transform it etc.)
            creater_pic = unsc_pics[f"picture_{key_ununlocked}"]
            creater_pic = pg.transform.scale(creater_pic, (creater_size, creater_size))
            r_screen.blit(creater_pic, (topleft_margin + (crtr_btn_w + margin_w) * len(unlocked_creaters) + (crtr_btn_w - creater_size) / 2, topleft_margin + (crtr_btn_w - creater_size) / 2 + 10))

            #render the "price tag" text
            price = creater_prices[key_ununlocked][0] # see creater_prices.json
            price_img = r_font.render(str(price), True, (0,0,0))
            price_img_w, price_img_h = price_img.get_size()
            #calculate coords for blit(s)
            topleft = (topleft_margin + (crtr_btn_w + margin_w) * len(unlocked_creaters), topleft_margin) # relative to current btn
            blit_y = topleft[1] + 20
            total_size = r_size + margin_r_price + price_img_w # total width of "price tag"
            r_blit_x = (crtr_btn_w - total_size) / 2 # in the middle
            text_blit_x = r_blit_x + r_size + margin_r_price
            #blit research icon
            r_screen.blit(r_icon_picture, (topleft[0] + r_blit_x, blit_y))
            #blit text
            r_screen.blit(price_img, (topleft[0] + text_blit_x, blit_y + 6)) # 3px offset because of font

            creater_menu_collidepoints.append([btn_rect, "creater", key_ununlocked, False, price])

    elif r_screen_page == 4: #crafting research menu
        half_size = 175/2
        for x in range(15):
            for y in range(15):#research_crafter_btn_clicked
                lines = r_crafter_grid[y][x][0]
                for line in lines:
                    if research_grid[y][x][0] and research_grid[line[1]][line[0]][0]:
                        pg.draw.line(r_screen, (40, 140, 144), (round(175 * np.sqrt(3) / 2 * x + half_size),175*y + (x % 2) *half_size+half_size), (round(175 * np.sqrt(3) / 2 * line[0]+half_size),175*line[1] + (line[0] % 2) *175/2+half_size), width=10)
        
        for x in range(15):
            for y in range(15):
                if x == 7 and y == 7: # centre of grid
                    r_screen.blit(research_crafter_btn_start, (round(175 * np.sqrt(3) / 2 * x),175*y + (x % 2) *half_size))
                else:    
                    if research_grid[y][x][0]:
                        if research_grid[y][x][1]:
                            r_screen.blit(research_crafter_btn_clicked, (round(175 * np.sqrt(3) / 2 * x),175*y + (x % 2) *half_size))
                        else:
                            r_screen.blit(research_crafter_btn, (round(175 * np.sqrt(3) / 2 * x),175*y + (x % 2) *half_size))

                        x_, y_ = (round(175 * np.sqrt(3) / 2 * x),175*y + (x % 2) *half_size)
                        if r_crafter_grid[y][x][1] is not None:
                            # get w/h of text
                            cost = str(r_crafter_grid[y][x][2])
                            cost_w, cost_h = r_font.size(cost)
                            #get w of research icon picture
                            r_icon_w = r_icon_picture.get_width()

                            margin_cost_r = 7
                            y_offset = 25

                            length = r_icon_w + margin_cost_r + cost_w
                            r_screen.blit(r_icon_picture, (x_ + (175 - length) / 2, y_ + y_offset))
                            
                            cost_render = r_font.render(cost, True, (0, 0, 0))

                            r_screen.blit(cost_render, (x_ + (175 - length) / 2 + margin_cost_r + r_icon_w, y_ + 30))

                            pic = unsc_pics["item_{}_picture".format(r_crafter_grid[y][x][1])]
                            pic = pg.transform.scale(pic, (half_size, half_size))
                            r_screen.blit(pic, (x_ + (175 - half_size) / 2, y_ + (175 - half_size) / 1.5))

    elif r_screen_page == 2:
        pass

    return r_screen, creater_menu_collidepoints
    
def draw_research_fixed(screen, r_screen, research_display, r_points, r_screen_page, mx,my,r_scrollx, r_scrolly):
    width, height = screen.get_size()
    # research points count in left-bottom corner
    r_screen.blit(research_display, (0, height - 53))
    r_screen.blit(r_display_picture, (5, height - 45))
    r_screen.blit(r_display_font.render(str(r_points), True, (0, 0, 0)), (50, height - 41))

    # cross icon in right-top corner
    cross_margin = 10
    r_screen.blit(icon_unclicked_picture, (width - 50 - cross_margin, cross_margin))
    r_screen.blit(icon_cross, (width - 50 - cross_margin, cross_margin))

    # tab buttons
    bar_width = width
    bar_height = 0
    buttons = 6 # button count
    button_distance = 75
    r_icons_click_list = []  # pos icons
    for icon in range(buttons):
        r_icons_click_list.append([(icon * button_distance) + int((bar_width - (buttons * button_distance)) / 2),
                                height - bar_height - button_distance])
        if r_screen_page == icon:
            screen.blit(icon_clicked_picture, (
            (icon * button_distance) + int((bar_width - (buttons * button_distance)) / 2),
            height - bar_height - button_distance))
        else:
            screen.blit(icon_unclicked_picture, (
            (icon * button_distance) + int((bar_width - (buttons * button_distance)) / 2),
            height - bar_height - button_distance))
        if icon in [0, 1, 2, 3, 4, 5]:
            screen.blit(eval("icon_" + str(icon + 1)), (
            (icon * button_distance) + int((bar_width - (buttons * button_distance)) / 2),
            height - bar_height - button_distance))

    return [width - 50 - cross_margin, cross_margin], r_icons_click_list

def research_mouse_check(shortage_timer, shortage_item, r_points, r_prices, r_scrollx, r_scrolly, mx, my,research_progress, research_scrollx, research_scrolly, research_button_clicked, r_screen_page, research_grid, r_crafter_grid, unlocked_recipes,creater_menu_collidepoints,creater_unlocked_recipes,unlocked_blocks):
    clicked_button = -1
    clicked_row = -1
    update_r_screen = False
    creater_clicked_btn = None

    if r_screen_page == 0: # conveyor research menu
        button_space_x = 50
        button_space_y = 25
        button_size_x, button_size_y = research_button_clicked.get_size()
        button_dist_x = button_space_x + button_size_x
        button_dist_y = button_space_y + button_size_y
        for category in range(len(research_progress)):  # per category
            for row in range(len(research_progress[category])):  # per row per category
                if not research_progress[category][max(row - 1, 0)] < 0:
                    for button in range(research_progress[category][row] + 2):
                        if button == research_progress[category][row] + 1:
                            if mx > button * button_dist_x - r_scrollx and mx < button * button_dist_x + button_size_x - r_scrollx:
                                if my > row * button_dist_y - r_scrolly and my < row * button_dist_y + button_size_y - r_scrolly:
                                    if button < 6:
                                        if r_prices[row][button] <= r_points:
                                            r_points -= r_prices[row][button]
                                            clicked_button = button
                                            clicked_row = row
                                            update_r_screen = True

                                        else:  # not enough research points
                                            shortage_timer = t.perf_counter()
                                            shortage_item = 0

    elif r_screen_page in [1,2,3]: #creater research menu
        for btn in creater_menu_collidepoints:
            btn_x = btn[0].x - r_scrollx
            btn_y = btn[0].y - r_scrolly
            btn_rect = pg.Rect((btn_x, btn_y),(btn[0].w, btn[0].h))
            if btn_rect.collidepoint(mx, my):
                if btn[3] == False: # not unlocked yet
                    if btn[4] <= r_points: # enough r_points to buy it
                        update_r_screen = True
                        unlock_type = btn[1] # can be "item" or "creater"
                        unlocked = btn[2] # what item/creater is unlocked
                        if unlock_type == "creater":
                            creater_unlocked_recipes[int(unlocked)] = []
                            unlocked_blocks.append(int(unlocked))
                            unlocked_blocks = sorted(unlocked_blocks)
                        elif unlock_type == "item":
                            creater_unlocked_recipes[btn[5]].append(unlocked)
                        r_points -= btn[4]
                        creater_clicked_btn = btn #store btn for later particle gen
                    else:  # not enough research points
                        shortage_timer = t.perf_counter()
                        shortage_item = 0

    elif r_screen_page == 4: # crafting research menu
        mouse_x = mx + r_scrollx
        mouse_y = my + r_scrolly
        half_size = 175/2
        for row in range(len(r_crafter_grid)):
            for button in range(len(r_crafter_grid[0])):
                if research_grid[row][button][0]:
                    mid_loc = (round(half_size * np.sqrt(3) * button) + half_size,2*half_size*row + (button % 2) *half_size + half_size)
                    distance = np.sqrt((mouse_x - mid_loc[0])**2 + (mouse_y - mid_loc[1])**2)
                    if distance <= half_size:
                        if r_crafter_grid[row][button][2] <= r_points:
                            if research_grid[row][button][1] != True:
                                research_grid[row][button][1] = True
                                update_r_screen = True
                                for line in r_crafter_grid[row][button][0]:
                                    research_grid[line[1]][line[0]][0] = True
                                r_points -= r_crafter_grid[row][button][2]
                                if not r_crafter_grid[row][button][1] is None:
                                    unlocked_recipes.append(r_crafter_grid[row][button][1])
                        else:  # not enough research points
                            shortage_timer = t.perf_counter()
                            shortage_item = 0

    return shortage_timer, shortage_item, r_points, clicked_row, clicked_button, research_grid, update_r_screen, unlocked_recipes, creater_unlocked_recipes, creater_clicked_btn,unlocked_blocks

def draw_shortage_notification(screen, not_enough_picture, shortage_item):
    width, height = screen.get_size()
    width_rect, height_rect = not_enough_picture.get_size()
    screen.blit(not_enough_picture, (int((width - width_rect) / 2), int(height / 75)))
    item_size = int(height_rect / 3 * 2)
    if shortage_item != 0:  # not research item
        screen.blit(pg.transform.scale(unsc_pics["item_" + str(shortage_item) + "_picture"], (item_size, item_size)),
                    (int((width - width_rect) / 2), int((height / 75) + (height_rect - item_size) / 2)))
    elif shortage_item == 0:
        screen.blit(pg.transform.scale(r_icon_picture, (item_size, item_size)), (
        int((width - width_rect) / 2 + (width_rect - item_size * 1.5 - (height_rect - item_size) / 2)),
        int((height / 75) + (height_rect - item_size) / 2)))


def research_clicked_item(unlocked_blocks, clicked_row, clicked_button, research_progress, conveyor_speed, move_speed):
    research_progress[0][clicked_row] += 1
    if clicked_button == 0:  # unlock
        conveyor_dict = {0: [1], 1: [2], 2: [3, 4], 3: [5, 6], 4: [7], 5:[16,17,18]}
        for x in conveyor_dict[clicked_row]:
            unlocked_blocks.append(x)
        unlocked_blocks = sorted(unlocked_blocks)
    elif clicked_button == 1:  # savings 1
        pass
    elif clicked_button == 2:  # effeciency 1
        conveyor_speed[clicked_row] -= conveyor_speed[clicked_row] / 3
        move_speed[clicked_row] = move_speed[clicked_row] / 3 * 6
    elif clicked_button == 3:  # savings 2
        pass
    elif clicked_button == 4:  # effeciency 2
        conveyor_speed[clicked_row] -= conveyor_speed[clicked_row] / 3
        move_speed[clicked_row] = move_speed[clicked_row] / 3 * 4.6

    return unlocked_blocks, conveyor_speed, move_speed

def circle_surf(radius, color):
    temp_surf = pg.Surface((radius * 2, radius * 2))
    pg.draw.circle(temp_surf, color, (radius, radius), radius)
    temp_surf.set_colorkey((0,0,0))
    return temp_surf

def research_particles(screen, r_particles, deltaTime):
    # index 0=x,1=y,2=size
    particles_pop = []
    img_transformed = -1
    for p in range(len(r_particles)):
        # draw "luminous" background 
        radius = int(r_particles[p][2]) * 0.75

        backg_circle = circle_surf(radius, (30, 3, 30))
        screen.blit(backg_circle, (int(r_particles[p][0] - radius), int(r_particles[p][1] - radius)), special_flags=pg.BLEND_RGB_ADD)

        # draw
        img_transformed = pg.transform.scale(r_particle_picture, (int(r_particles[p][2]), int(r_particles[p][2])))
        screen.blit(img_transformed,
                    (int(r_particles[p][0] - r_particles[p][2] / 2), int(r_particles[p][1] - r_particles[p][2] / 2)))
        # process
        r_particles[p][2] -= 0.1 * deltaTime
        if r_particles[p][2] < 1:  # size < ...
            particles_pop.append(p)

    for index in list(sorted(particles_pop))[::-1]:
        r_particles.pop(index)
    return r_particles


def generate_r_particles_square(r_particles, x0, y0, x1, y1, size_range,spawn_rate=25):
    for x in range(x0, x1):  # top,bottom row
        size = r.randint(size_range[0], size_range[1])
        offset = r.randint(-15, 15)
        if r.randint(0, spawn_rate) == 0:
            r_particles.append([x, y0, size, size])
        if r.randint(0, spawn_rate) == 0:
            r_particles.append([x, y1, size, size])
    for y in range(y0, y1):  # left,right row
        size = r.randint(size_range[0], size_range[1])
        if r.randint(0, spawn_rate) == 0:
            r_particles.append([x0, y, size, size])
        if r.randint(0, spawn_rate) == 0:
            r_particles.append([x1, y, size, size])
    return r_particles

if __name__ == '__main__':
    pg.font.quit()
    pg.quit()

#1908 lines of code!