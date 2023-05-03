##############################################
#Import pygame and sys to draw loading screen#
##############################################
import pygame as pg
import sys

#########
#Version#
#########

with open("Data/ver.txt") as f:
    version = f.read()

from Files.loading_screen import *

pg.init()
pg.font.init()
pg.display.init()

screen_w, screen_h = (1280, 720)
screen = pg.display.set_mode((screen_w, screen_h) ,pg.RESIZABLE|pg.DOUBLEBUF|pg.HWSURFACE, vsync=1)

pg.display.set_caption(f"Factory {version}")
pg.display.set_icon(pg.image.load("Assets/Blocks/11.png"))

percent_vals = [0]
load_font = pg.font.Font('Fonts/Roboto-Light.ttf', 25)
percent_vals = loading_screen(screen,percent_vals,10,load_font,"Importing modules")

screen_info = pg.display.Info()
screen_size = pg.display.get_surface().get_size()


################
#Import modules#
################

import random as r
import time as t
import numpy as np

import os
import pdb
import copy

import multiprocessing

percent_vals = loading_screen(screen,percent_vals,30,load_font,"Loading functions")

#load files path
from Files.factory_functions import *
from Files.menu_functions import *
from Files.loading_functions import *
from Files.item_spawn import *
from Files.save_world import *

percent_vals = loading_screen(screen,percent_vals,70,load_font,"Reading save files")

playing = True
width_grid = 500
height_grid = 500

grid = np.zeros((height_grid,width_grid),dtype='int')
grid_rotation = np.zeros((height_grid,width_grid),dtype='int') # 0 up, 1 right, 2 down, 3 left
grid_cables = np.zeros((height_grid,width_grid),dtype='int') # for cables' path

############
#.txt files#
############

r_prices = open('Data/research_prices.txt','r')
r_prices = eval(r_prices.read())
r_prices = np.array(r_prices)

with open("Data/tile_info.json") as f:
    tile_info = json.load(f)
    tile_names, tile_des, blocks_index, b_prices, big_tiles, placed_on_only, cannot_place_on, ground_blocks, spawn_time, spawn_items, spawn_perf_counters, strict_placement_tiles, can_spawn_items = convert_json(tile_info)

with open("Data/item_info.json") as f:
    item_info = json.load(f)
    item_names = convert_item_info(item_info)

# item_names = open('Data/item_names.txt','r')
# item_names = eval(item_names.read())

percent_vals = loading_screen(screen,percent_vals,80,load_font,"Creating arrays")

###################################
#Create grid, craft and cargo data#
###################################

array_side_1 = []
array_side_2 = []
array_side_3 = []

'''
Grid data by default:
{}
Can contain: (with default values)
"spawn_item": -1 -> which item it spawns
"spawn_perf": 3 -> time.perf_counter() for cooldown spawning
"split_side": 0 -> splitter: which item it splits (flips from 0 to 1 to 0...)
"split_count": 0 -> splitter: counts splits in case of 2 right and 1 left etc.
"sort_item": 0 -> sorter: which item it sorts
"craft_recipe": 0 -> crafter: which item it crafts. -1 is for "r" (research point).

{"spawn_item": -1, "spawn_perf": 3, "split_side": 0, "split_count": 2, "sort_item": 0, "craft_recipe": 0}
'''

for i in range(width_grid):
    array_side_1.append({})     
    array_side_2.append({})
    array_side_3.append({}) #items to spawn will be in the dictionary

craft_data = []
grid_data = []
cargo_data = []
for i in range(height_grid):
    grid_data.append(copy.deepcopy(array_side_1))
    craft_data.append(copy.deepcopy(array_side_2))
    cargo_data.append(copy.deepcopy(array_side_3))

craft_data = np.array(craft_data)
grid_data = np.array(grid_data)
cargo_data = np.array(cargo_data)

percent_vals = loading_screen(screen,percent_vals,85,load_font,"Setting variables")

################
#Game variables#
################

#scroll
scale = 1
scrollx = 0
scrolly = 0
scroll_keys_hold = [False,False,False,False]#w,a,s,d
scroll_speed = 1
menu_scrollx = 0
menu_scrollspeed = 10

#drawing
mrx = 0
mry = 0
mrr = 0
mouse_down = False
brush = 1

mousebutton_pressed = False
draggable_brushes = [0,1,2,3,4,5,6,7,18]
mouse_drag_brush = False
stop_mouse_placement = False

#menu
open_menu = False
bar_width = 0
bar_height = 0

menu_pictures = [[1,2,3,4,5,6,7,16,17,18],[12,13,14],[],[33, 34, 35],[15],[]]

clicked_icon = -1
icon_click_list = []
icon_width = 75

clicked_button = -1
button_click_list = []
button_distance = 0
button_width = 100

shortage_timer = -10
shortage_item = -1

keyb_up_buttons = []
keyb_down_buttons = []

#research
research_progress = [[0, -1, -1, -1, -1, -1]]
conveyor_speed = [25.0,25.0,25.0,25.0,12.5,5]#conveyor,cross conveyor,split_conveyor,sorting conveyor,highway conveyor (lower=faster)
conveyor_research_progress_dict = {1:0,2:1,3:2,4:2,5:3,6:3,7:4,8:5,9:5,10:5}

#research menu
r_screen_transparent = update_r_screen_func(screen, rect_ui) #screen for the transparent background
r_width = [1500, 680, 0, 680, 2500, 0]
r_height = [800, 800, 0, 1350, 2750, 0]
r_screen_page = 5 #which page r screen is
r_screen = pg.Surface((r_width[r_screen_page], r_height[r_screen_page]), pg.SRCALPHA) #entire research screen: uses scrolling (not re-rendering)
update_r_screen = True #True when screen needs to update: only for 1 frame
update_r_scroll = True
research_menu = False
r_scrollx = [-5,0,0,0,530,0]
r_scrolly = [-5,0,0,0,1060,0]
r_icons_click_list = [] # click list icons research menu

research_text = [["Unlock:","Savings:","Efficiency:","Savings:","Efficiency:","Savings:"]]
research_subtext = [["Unlocks new tile","Decreases building price","Increases speed","Decreases building price","Increases speed","Decreases building price"]]
r_tile_text = [["Conveyor","Cross Conveyor","Split Conveyor","Sorting Conveyor","Highway Conveyor","Cable transport"]]

#categories: (from min 0 to max 6)
#0=conveyors (0=conveyor,1=cross conveyor,2=split conveyor,3=sorting conveyor,4=highway conveyor)
r_clicked_row = -1
r_clicked_button = -1

r_particles = []#x center,y center,size
exit_corner = [] #collidepoint of rect research menu

#tile selecting menu
selected_x = -1#tile data editing (when selected)
selected_y = -1
tile_mode = ""#0, splitter, sorter
up_button = pg.Rect((0,0),(0,0))
down_button = pg.Rect((0,0),(0,0))
tile_menu_open = ""
tile_mode = "place" # can be place, edit (=select recipe etc.), info (=name tile+description x,y etc.), view(=view, only tile mode menu visible).  
tile_mode_btns = [] # btns of tile mode menu, used for collidepoint

rect_edit_menu = pg.Rect((0,0),(0,0))
crafter_btn_collidepoints = []
#edit tile menu
edit_tile_menu_open = False
tile_menu_type = "" # can be splitter, sorter, crafter
creater_type = 0 # creater type that is selected in edit tile menu. For example, the farm (13) or barn (15) etc. 
craft_scrolly = {"crafter": 15, "creater": 15}
update_edit_menu = True
hover_recipe = -1 # which recipe is hovered
line_1 = 0
line_2 = 0

#keybinds
keybind_menu = False
keybinds = {0:0,1:1,2:12,3:16,4:15,5:18,6:19,7:33,8:34,9:35}
unlocked_blocks = [0,1,12,13,14,15,20,23, 24,25, 33,34,35]
k_scrolly = 0# scrolling in keybind menu for smaller screens

#items & blocks
move = t.perf_counter()
move_animation = [1,1,1,1,1]#conveyor,cross conveyor,split_conveyor,sorting conveyor,highway conveyor
move_speed = [1.0,1.0,1.0,1.0,2.0,0]

items_list = []

placeable = False

storage = [100000,10,10,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#item0, item1, etc.

#recipes
unlocked_recipes = []
creater_unlocked_recipes = {} 
#example of creater_unlocked_recipes:
# {13: [1, 2, 3], 14: [4, 5], 15: []}
creater_menu_collidepoints = [] # creater menu collidepoints go in here

# spawning
cargo_spawn_list = [] #only one spawn time

cargo_spawn_perf = -1 # cargo cooldown spawn time, when not a lot of items
spawn_cooldown = -1

item_spawn_time = {'12':1,'13':2,'14':3,'16':5,'33':1,'34':2,'35':3}

locations = [[],[]] #list of locations (x,y) of spawnable blocks
crafting_locations = [[],[]]
cargo_locations = [[],[]]
cargo_spawn_locations = [[],[]]

# player data
start_play_perf = -1

#debug
angle = 0
print_timing = False

#final variables
clock = pg.time.Clock()
deltaTime = 0.0
render_distance = 1
max_scale = 2

not_enough_picture,rect_keybinds,data_display,data_arrow,rect_info,rect_ui,research_button_clicked,research_button_unclicked,research_display,info_ui = render_images(screen,True)

pg.event.set_allowed([pg.MOUSEMOTION,pg.MOUSEBUTTONDOWN,pg.MOUSEBUTTONUP,pg.QUIT,pg.VIDEORESIZE,pg.KEYUP,pg.KEYDOWN, pg.MOUSEWHEEL])

percent_vals = loading_screen(screen,percent_vals,90,load_font,"Loading world list")

#game menu
in_menu = True
selected_world = None
backg_surf, backg_img = create_backg_surf(screen_w, screen_h)


world_list = [] #world folders get added in here
rootdir = 'Data/Saves'
for file in os.listdir(rootdir):
    d = os.path.join(rootdir, file)
    if os.path.isdir(d):
        world_list.append(d[11:]) #cut out the "Data/Saves/" part

world_btn_list = [] # world btns
for i, world in enumerate(world_list):
    if world != "~menu_world":
        world_btn_list.append(WorldSelect(i, world))


btn_list = []
input_box_list = []
button_collidepoints = []
switch_menu_trigger = True
menu_screen = "world_select"
keypresses = None
mouse_down = False # when mouse down
clicked = False # when mouse is released
ignore_click = False

world_menu_top, world_menu_bottom = update_pictures(screen)
world_select_scrolly = -world_menu_top.get_height() + 45

grid,grid_rotation,grid_cables,grid_data,unlocked_blocks,conveyor_speed,move_speed,storage,keybinds,research_progress,research_grid, grid_generation, grid_features_generation,unlocked_recipes,creater_unlocked_recipes = read_world('~menu_world', spawn_items) # load background for title screen

percent_vals = loading_screen(screen,percent_vals,100,load_font,"Starting game loop")

autosave_perf = 1
autosave_interval = 10
autosave_active = False
autosave_stage = 0 # goes up 1 every time it is active. When it reaches certain num, autosave is deactivated

autoload = True
autoload_world = "new testing world"

if autoload: # temporary for quicker testing
    selected_world = autoload_world
    scroll_keys_hold = [False, False, False, False]
    grid,grid_rotation,grid_cables,grid_data,unlocked_blocks,conveyor_speed,move_speed,storage,keybinds,research_progress,research_grid, grid_generation, grid_features_generation,unlocked_recipes,creater_unlocked_recipes = read_world(autoload_world, spawn_items)
    locations, crafting_locations, cargo_locations, cargo_spawn_locations = update_locations(grid, spawn_items)
    append_per_spawn = generate_append_per_spawn(grid, grid_data, spawn_time, spawn_items, locations, blocks_index,creater_unlocked_recipes)
    in_menu = False
    start_play_perf = t.perf_counter() + 1
    ignore_click = True

###########
#Game loop#
###########

while playing and __name__ == "__main__":
    if in_menu:
        keypresses = pg.key.get_pressed()
        events = pg.event.get()
        mx,my = pg.mouse.get_pos()
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 4:
                    if world_select_scrolly > -world_menu_top.get_height() + 45:
                        world_select_scrolly -= 80
                elif e.button == 5:
                    if world_select_scrolly < len(world_list) * 260 - world_menu_top.get_height() - 300:
                        world_select_scrolly += 80
                else: # no scrollwheel stuff
                    mouse_down = True

            if e.type == pg.MOUSEBUTTONUP:
                if e.button < 4:
                    mouse_down = False
                    clicked = True

            if e.type == pg.VIDEORESIZE:
                screen_info = pg.display.Info()
                screen_size = pg.display.get_surface().get_size()
                screen_w, screen_h = screen_size
                not_enough_picture,rect_keybinds,data_display,data_arrow,rect_info,rect_ui,research_button_clicked,research_button_unclicked,research_display,info_ui = render_images(screen,True)
                r_screen_transparent = update_r_screen_func(screen, rect_ui)
                if k_scrolly < rect_keybinds.get_height()-screen_size[1]:
                    k_scrolly = 0
                switch_menu_trigger = True
                backg_surf, backg_img = create_backg_surf(screen_w, screen_h)
                world_menu_top, world_menu_bottom = update_pictures(screen)

            if e.type == pg.QUIT:
                playing = False

            if input_box_list != []:
                for inputbox in input_box_list:
                    inputbox.handle_events(e, screen)

        if switch_menu_trigger:
            btn_list, input_box_list = [], []
            if menu_screen == "title":
                btn_list = draw_title_menu(screen, backg_surf, update_btn_list=True)
            elif menu_screen == "world_select":
                btn_list = draw_world_select_menu(screen, backg_surf, world_list, world_menu_top, world_menu_bottom, update_btn_list=True)
            elif menu_screen == "create":
                btn_list, input_box_list = draw_create_menu(screen, backg_img, update_btn_list=True)

            backg_surf, backg_img = create_backg_surf(screen_w, screen_h, menu_screen)
            switch_menu_trigger = False

        if t.perf_counter() > move+0.025:
            move = t.perf_counter()
            for i in range(len(move_animation)):
                move_animation[i] += move_speed[i]
                move_animation[i] = move_animation[i] % 25

        if menu_screen in ["title", "world_select", "create"]:
            grid_cables = teken_grid(screen, grid, grid_rotation, selected_x, selected_y, move_animation, scrollx, scrolly, screen_size,render_distance,storage,scale,scaled_pictures,blocks_index, grid_cables, brush, angle, grid_data)
        
        if menu_screen == "title":
            draw_title_menu(screen, backg_surf)

        elif menu_screen == "world_select":
            screen.blit(backg_surf,(0,0))

            for worldbtn in world_btn_list:
                worldbtn.draw(screen, world_select_scrolly)

            draw_world_select_menu(screen, backg_surf, world_list, world_menu_top, world_menu_bottom)

        elif menu_screen == "create":
            draw_create_menu(screen, backg_img)

        for inputbox in input_box_list:
            inputbox.draw(screen, keypresses)

        for btn in btn_list:            
            btn.update_hover(mx,my)
            btn.update_click(clicked)
            if btn.clicked:
                if btn.id == "world_select":
                    menu_screen = "world_select"
                    switch_menu_trigger = True

                elif btn.id == "quit":
                    playing = False
                
                elif btn.id == "to_title":
                    menu_screen = "title"
                    switch_menu_trigger = True

                elif btn.id == "to_world_select":
                    menu_screen = "world_select"
                    switch_menu_trigger = True

                elif btn.id == "create_world":
                    menu_screen = "create"
                    switch_menu_trigger = True

                elif btn.id == "play_world":
                    backg_surf = pg.Surface(screen.get_size())
                    grid_cables = teken_grid(screen, grid, grid_rotation, selected_x, selected_y, move_animation, scrollx, scrolly, screen_size,render_distance,storage,scale,scaled_pictures,blocks_index, grid_cables, brush, angle, grid_data)
                    loading_surf = setup_loading_screen(screen, backg_img)

                    draw_loading_screen_create_world(screen, clock, loading_surf, 10, 0, "Reading world...")

                    scroll_keys_hold = [False, False, False, False]
                    grid,grid_rotation,grid_cables,grid_data,unlocked_blocks,conveyor_speed,move_speed,storage,keybinds,research_progress,research_grid, grid_generation, grid_features_generation,unlocked_recipes,creater_unlocked_recipes = read_world(selected_world, spawn_items)

                    locations, crafting_locations, cargo_locations, cargo_spawn_locations = update_locations(grid, spawn_items)
                    append_per_spawn = generate_append_per_spawn(grid, grid_data, spawn_time, spawn_items, locations, blocks_index,creater_unlocked_recipes)

                    draw_loading_screen_create_world(screen, clock, loading_surf, 90, 10, "Setting variables...")

                    locations, crafting_locations, cargo_locations, cargo_spawn_locations = update_locations(grid, spawn_items)
                    in_menu = False
                    start_play_perf = t.perf_counter() + 1
                    ignore_click = True
                    tile_mode = "place"
                    update_r_screen = True

                    draw_loading_screen_create_world(screen, clock, loading_surf, 100, 90, "Rendering...")

                elif btn.id == "confirm_create_world":
                    world_options = {}
                    world_seed = ""
                    world_name = ""
                    for btn in btn_list:
                        if btn.__class__.__name__ == "SettingsBtn":
                            world_options = btn.get_setting(world_options)
                    for inputbox in input_box_list:
                        if inputbox.id == "world_name":
                            world_name = inputbox.text
                        elif inputbox.id == "world_seed":
                            world_seed = inputbox.text

                    if world_name == "":
                        continue

                    backg_surf = pg.Surface(screen.get_size())
                    grid_cables = teken_grid(screen, grid, grid_rotation, selected_x, selected_y, move_animation, scrollx, scrolly, screen_size,render_distance,storage,scale,scaled_pictures,blocks_index, grid_cables, brush, angle, grid_data)
                    loading_surf = setup_loading_screen(screen, backg_img)
                    
                    create_world(screen, loading_surf, clock, world_name, world_seed, world_options, version)
                    
                    world_list.append(world_name)
                    world_btn_list = [] # regenerate worldbtn list
                    for i, world in enumerate(world_list):
                        if world != "~menu_world":
                            world_btn_list.append(WorldSelect(i, world))

                    #load world after creation
                    backg_surf = pg.Surface(screen.get_size())
                    grid_cables = teken_grid(screen, grid, grid_rotation, selected_x, selected_y, move_animation, scrollx, scrolly, screen_size,render_distance,storage,scale,scaled_pictures,blocks_index, grid_cables, brush, angle, grid_data)
                    loading_surf = setup_loading_screen(screen, backg_img)

                    draw_loading_screen_create_world(screen, clock, loading_surf, 10, 0, "Reading world files...")


                    selected_world = world_name
                    scroll_keys_hold = [False, False, False, False]
                    grid,grid_rotation,grid_cables,grid_data,unlocked_blocks,conveyor_speed,move_speed,storage,keybinds,research_progress,research_grid, grid_generation, grid_features_generation,unlocked_recipes,creater_unlocked_recipes = read_world(selected_world, spawn_items)
                    
                    locations, crafting_locations, cargo_locations, cargo_spawn_locations = update_locations(grid, spawn_items)
                    append_per_spawn = generate_append_per_spawn(grid, grid_data, spawn_time, spawn_items, locations, blocks_index,creater_unlocked_recipes)
                    
                    draw_loading_screen_create_world(screen, clock, loading_surf, 100, 10, "Finishing up...")

                    in_menu = False
                    start_play_perf = t.perf_counter() + 1
                    ignore_click = True
                    tile_mode = "place"
                    update_r_screen = True

            btn.draw(screen)

        if not ignore_click and menu_screen == "world_select" and clicked:
            for worldbtn in world_btn_list:
                if worldbtn.update_selected(mx, my, clicked, selected_world):
                    selected_world = worldbtn.world_folder
                    worldbtn.selected = True
                    break
            else:
                selected_world = None
                for worldbtn in world_btn_list:
                    worldbtn.update_selected(-5, -5, False, None)

            for worldbtn in world_btn_list:
                if worldbtn.world_folder != selected_world:
                    worldbtn.update_selected(-5, -5, False, None)
                
        for btn in btn_list:
            if btn.id in ["play_world", "edit_world", "delete_world"]:
                btn.disabled = True if selected_world is None else False
                btn.update_disabled(btn.disabled)
                
        clicked = False
        ignore_click = False
        fps = clock.get_fps()
        screen.blit(i_title_font.render(str(int(fps)), True, (0,0,0)),(10,10))
        pg.display.flip()
        deltaTime = clock.tick(60)

    else: #in game
        #events
        mx,my = pg.mouse.get_pos()
        events = pg.event.get()

        t_event = t.perf_counter()

        for e in events:
            if e.type == pg.MOUSEMOTION:
                if my > screen_size[1] - bar_height: #in menu bar
                    if mx < int(button_distance) and menu_scrollx > 0: #left
                        menu_scrollx -= menu_scrollspeed
                    elif mx >  screen_size[0] - int(button_distance) < 1000: #right
                        menu_scrollx += menu_scrollspeed

                elif edit_tile_menu_open:
                    if rect_edit_menu.collidepoint(mx,my): # in the edit menu
                        update_edit_menu = True
                        mouse_down = False
                        for btn_obj in crafter_btn_collidepoints:
                            btn = btn_obj[0]
                            if btn.collidepoint(mx, my):
                                hover_recipe = btn_obj[1]
                                
            if e.type == pg.MOUSEBUTTONDOWN:
                if mousebutton_pressed == False:
                    stop_mouse_placement = False
                    if e.button == 1:#left mouse button
                        if not research_menu and not keybind_menu:#normal menu
                            if my < screen_size[1] - bar_height:#dont draw tiles under the menu
                                mouse_down = True
                            else:
                                stop_mouse_placement = True
                            open_menu = False
                            for icon in range(len(icon_click_list)):
                                if mx > icon_click_list[icon][0] and my > icon_click_list[icon][1]:
                                    if mx < icon_click_list[icon][0]+icon_width and my < icon_click_list[icon][1]+icon_width:
                                        stop_mouse_placement = True
                                        mouse_down = False
                                        if clicked_icon == icon:
                                            clicked_icon = -1
                                            open_menu = False
                                        else:
                                            clicked_icon = icon
                                            open_menu = True
                                            clicked_button = -1
                                            tile_mode = "place"

                            if my > screen.get_size()[1] - bar_height:
                                open_menu = True
                                tile_mode = "place"
                            if not open_menu:
                                clicked_icon = -1
                            if clicked_icon == 5: # research
                                open_menu = False
                                research_menu = True
                                clicked_icon = -1
                                tile_mode = "place"

                            for button in range(len(button_click_list)):
                                if mx > button_click_list[button][0] and my > button_click_list[button][1]:
                                    if mx < button_click_list[button][0]+button_width and my < button_click_list[button][1]+button_width:
                                        stop_mouse_placement = True
                                        if clicked_button == button:
                                            clicked_button = -1
                                        else:
                                            if clicked_icon == 0:
                                                if research_progress[clicked_icon][conveyor_research_progress_dict[button+1]] > -1:#researched
                                                    clicked_button = button
                                                    brush = menu_pictures[clicked_icon][clicked_button]
                                                else:
                                                    clicked_button = -1
                                            elif clicked_icon in [1,2,3]: #researched creaters
                                                if menu_pictures[clicked_icon][button] in unlocked_blocks:
                                                    clicked_button = button
                                                    brush = menu_pictures[clicked_icon][clicked_button]


                                            else: #exception
                                                clicked_button = button
                                                if not (clicked_icon >= len(menu_pictures)):
                                                    if not (button >= len(menu_pictures[clicked_icon])):
                                                        brush = menu_pictures[clicked_icon][button]

                            if edit_tile_menu_rect.collidepoint(mx, my): # changing tile mode (mouse click was in the tile mode menu top right)
                                stop_mouse_placement = True
                                mouse_down = False
                                edit_tile_menu_open = False
                                for btn in tile_mode_btns:
                                    if btn[0].collidepoint(mx, my):
                                        tile_mode = btn[1]

                            if tile_mode == "info":
                                stop_mouse_placement = True
                                if (not (mx < rect_info.get_size()[0] and my > screen_size[1]-rect_info.get_size()[1])) and selected_x == mrx and selected_y == mry:
                                    stop_mouse_placement = True
                                    selected_x, selected_y = -1, -1
                                elif (mx < rect_info.get_size()[0] and my > screen_size[1]-rect_info.get_size()[1]):
                                    mouse_down = False
                                else:
                                    mouse_down = False#no more tile placement
                                    mrx, mry = bereken_muis_pos(mx,my,scrollx,scrolly,scale)
                                    selected_x = mrx
                                    selected_y = mry

                            elif tile_mode == "edit":
                                stop_mouse_placement = True
                                if (not (rect_edit_menu.collidepoint(mx,my))) and selected_x == mrx and selected_y == mry:
                                    stop_mouse_placement = True
                                    selected_x, selected_y = -1, -1
                                    edit_tile_menu_open = False
                                elif rect_edit_menu.collidepoint(mx,my): # click in the edit menu
                                    mouse_down = False
                                    if line_1 < my < line_2:
                                        for btn_obj in crafter_btn_collidepoints:
                                            btn = btn_obj[0]
                                            if btn.collidepoint(mx, my):
                                                hover_recipe = btn_obj[1]
                                                update_edit_menu = True
                                                grid_data = update_recipe(grid,grid_data,hover_recipe,selected_x,selected_y, blocks_index, creater_type, update=tile_menu_type)
                                                selected_x, selected_y = -1, -1
                                                edit_tile_menu_open = False
                                                if tile_menu_type == "creater":
                                                    locations, crafting_locations, cargo_locations, cargo_spawn_locations = update_locations(grid, spawn_items)
                                                    append_per_spawn = generate_append_per_spawn(grid, grid_data, spawn_time, spawn_items, locations, blocks_index, creater_unlocked_recipes)


                                else:
                                    if grid[mry, mrx] == 15 or grid[mry, mrx] == -15: 
                                        mouse_down = False # no more tile placement
                                        mrx, mry = bereken_muis_pos(mx,my,scrollx,scrolly,scale)
                                        selected_x = mrx
                                        selected_y = mry
                                        tile_menu_type = "crafter"
                                        edit_tile_menu_open = True
                                    elif -grid[mry, mrx] in can_spawn_items or grid[mry, mrx] in can_spawn_items:
                                        mouse_down = False # no more tile placement
                                        mrx, mry = bereken_muis_pos(mx,my,scrollx,scrolly,scale)
                                        selected_x = mrx
                                        selected_y = mry
                                        tile_menu_type = "creater"
                                        creater_type = abs(grid[mry, mrx])
                                        edit_tile_menu_open = True

                            elif not tile_mode == "edit":
                                edit_tile_menu_open = False

                            if up_button.collidepoint(mx,my):
                                stop_mouse_placement = True
                                if tile_info_mode == "splitter" and grid_data[selected_y,selected_x]["split_count"] < 100:
                                    grid_data[selected_y,selected_x]["split_count"] += 1
                                elif tile_info_mode == "sorter" and grid_data[selected_y,selected_x]["sort_item"] < len(storage)-1:
                                    grid_data[selected_y,selected_x]["sort_item"] += 1
                            elif down_button.collidepoint(mx,my):
                                stop_mouse_placement = True
                                if tile_info_mode == "splitter" and grid_data[selected_y,selected_x]["split_count"] > 1:
                                    grid_data[selected_y,selected_x]["split_count"] -= 1
                                elif tile_info_mode == "sorter" and grid_data[selected_y,selected_x]["sort_item"] > 0:
                                    grid_data[selected_y,selected_x]["sort_item"] -= 1

                        elif keybind_menu == True:
                            for k_index in keybinds.keys():
                                if keyb_up_buttons[k_index].collidepoint(mx,my):
                                    stop_mouse_placement = True
                                    if keybinds[k_index] < unlocked_blocks[-1]:
                                        unlocked_blocks_where = np.array(unlocked_blocks)
                                        unlocked_block_find = np.where(unlocked_blocks_where==keybinds[k_index])
                                        if unlocked_block_find[0].shape[0] == 0:
                                            unlocked_block_find = np.where(unlocked_blocks_where>=keybinds[k_index])
                                            keybinds[k_index] = unlocked_blocks[unlocked_block_find[0][0]]

                                        else:
                                            keybinds[k_index] = unlocked_blocks[unlocked_block_find[0][0]+1]

                                elif keyb_down_buttons[k_index].collidepoint(mx,my):
                                    stop_mouse_placement = True
                                    if keybinds[k_index] > 0:
                                        unlocked_blocks_where = np.array(unlocked_blocks)
                                        unlocked_block_find = np.where(unlocked_blocks_where == keybinds[k_index])
                                        if unlocked_block_find[0].shape[0] == 0:
                                            unlocked_block_find = np.where(unlocked_blocks_where<=keybinds[k_index])
                                            keybinds[k_index] = unlocked_blocks[unlocked_block_find[0][-1]]
                                        else:
                                            keybinds[k_index] = unlocked_blocks[unlocked_block_find[0][0] - 1]

                        elif research_menu:#research menu open
                            stop_mouse_placement = True
                            shortage_timer,shortage_item,storage[0],r_clicked_row,r_clicked_button,research_grid,update_r_screen,unlocked_recipes,creater_unlocked_recipes,creater_clicked_btn,unlocked_blocks = research_mouse_check(shortage_timer,shortage_item,storage[0],r_prices,r_scrollx[r_screen_page],r_scrolly[r_screen_page],mx,my,research_progress,r_scrollx[r_screen_page],r_scrolly[r_screen_page],research_button_clicked, r_screen_page, research_grid, r_crafter_grid, unlocked_recipes,creater_menu_collidepoints,creater_unlocked_recipes,unlocked_blocks)
                            if r_screen_page == 0: #conveyor/transport research screen
                                if r_clicked_row != -1 and r_clicked_button != -1:
                                    unlocked_blocks,conveyor_speed,move_speed = research_clicked_item(unlocked_blocks,r_clicked_row,r_clicked_button,research_progress,conveyor_speed,move_speed)
                                    r_particles = generate_r_particles_square(r_particles,r_clicked_button*250-r_scrollx[r_screen_page],r_clicked_row*125-r_scrolly[r_screen_page],r_clicked_button*250+200-r_scrollx[r_screen_page],r_clicked_row*125+100-r_scrolly[r_screen_page],(10,50))
                            elif r_screen_page in [1,2,3]: #creater research screen
                                if creater_clicked_btn is not None:
                                    x, y, w, h = creater_clicked_btn[0]
                                    x -= r_scrollx[r_screen_page]
                                    y -= r_scrolly[r_screen_page]
                                    unlocked_creater = creater_clicked_btn[1] == "creater"
                                    if unlocked_creater:
                                        r_particles = generate_r_particles_square(r_particles, x, y, x+w, y+h, (30,80),spawn_rate=10)
                                    else: # unlocked an item
                                        r_particles = generate_r_particles_square(r_particles, x, y, x+w, y+h, (10,50))



                            if mx > exit_corner[0] and mx < exit_corner[0]+50 and my > exit_corner[1] and my < exit_corner[1]+50:#exit button
                                research_menu = False
                                stop_mouse_placement = True

                            for icon in range(len(r_icons_click_list)):
                                if mx > r_icons_click_list[icon][0] and my > r_icons_click_list[icon][1]:
                                    if mx < r_icons_click_list[icon][0]+icon_width and my < r_icons_click_list[icon][1]+icon_width:
                                        mouse_down = False
                                        r_screen_page = icon
                                        update_r_screen = True

                        if brush in draggable_brushes and e.button == 1 and not stop_mouse_placement:
                            mouse_drag_brush = True #mouse held down for brushes

                    mousebutton_pressed = True

            if e.type == pg.MOUSEBUTTONUP:
                if e.button == 1:
                    mousebutton_pressed = False
                    mouse_drag_brush = False

                if keybind_menu:
                    if e.button == 4:#scroll up
                        if k_scrolly < rect_keybinds.get_height()-screen_size[1]:
                            k_scrolly += 25
                    if e.button == 5:#scroll down
                        if k_scrolly >= 25:
                            k_scrolly -= 25

                elif edit_tile_menu_open and tile_mode == "edit":
                    if e.button == 4:#scroll up
                        craft_scrolly[tile_menu_type] -= 5 * deltaTime
                        if tile_menu_type == "crafter":
                            craft_scrolly[tile_menu_type] = max(-len(unlocked_recipes) * 130 + 200, craft_scrolly[tile_menu_type])
                        elif tile_menu_type == "creater":
                            craft_scrolly[tile_menu_type] = max(-len(creater_unlocked_recipes[creater_type]) * 130 + 200, craft_scrolly[tile_menu_type])
                            
                    if e.button == 5:#scroll down
                        craft_scrolly[tile_menu_type] += 5 * deltaTime
                        craft_scrolly[tile_menu_type] = min(15, craft_scrolly[tile_menu_type])
                    update_edit_menu = True

                else: # scrolling in level -> zooming
                    mouse_down = False
                    if e.button == 4 and not research_menu:#scroll up
                        old_scale = scale
                        scale += 0.11
                        scale = int(scale*10)/10
                        if scale > max_scale:
                            scale = max_scale
                        scrollx = int(round(scrollx*scale/old_scale - mx*(1-old_scale/scale),0))
                        if scrollx > 0:
                            scrollx = 0
                        if scrollx < -round((grid.shape[1])*50*scale-screen_size[0], 3):
                            scrollx = int(round((grid.shape[1])*50*scale-screen_size[0], 3))
                        scrolly = int(round(scrolly*scale/old_scale - my*(1-old_scale/scale),0))
                        if scrolly > 0:
                            scrolly = 0
                        if scrolly < -round((grid.shape[0])*50*scale-screen_size[1], 3):
                            scrolly = int(round((grid.shape[0])*50*scale-screen_size[1], 3))
                        scaled_pictures = scale_pictures(scale)
                        render_distance = int(1/scale+1)
                    if e.button == 5 and not research_menu:#scroll down
                        old_scale = scale
                        scale -= 0.1
                        scale = int(scale*10)/10
                        if scale <= 0.5:
                            scale = 0.5
                        scrollx = int(round(scrollx*scale/old_scale - mx*(1-old_scale/scale),0))
                        if scrollx > 0:
                            scrollx = 0
                        if scrollx < -round((grid.shape[1])*50*scale-screen_size[0], 3):
                            scrollx = int(round((grid.shape[1])*50*scale-screen_size[0], 3))
                        scrolly = int(round(scrolly*scale/old_scale - my*(1-old_scale/scale),0))
                        if scrolly > 0:
                            scrolly = 0
                        if scrolly < -round((grid.shape[0])*50*scale-screen_size[1], 3):
                            scrolly = int(round((grid.shape[0])*50*scale-screen_size[1], 3))
                        scaled_pictures = scale_pictures(scale)
                        render_distance = int(1/scale+1)

            if e.type == pg.QUIT:
                playing = False

            if e.type == pg.VIDEORESIZE:
                screen_info = pg.display.Info()
                screen_size = pg.display.get_surface().get_size()
                screen_w, screen_h = screen_size
                not_enough_picture,rect_keybinds,data_display,data_arrow,rect_info,rect_ui,research_button_clicked,research_button_unclicked,research_display,info_ui = render_images(screen,True)
                r_screen_transparent = update_r_screen_func(screen, rect_ui)

                if k_scrolly < rect_keybinds.get_height()-screen_size[1]:
                    k_scrolly = 0

                backg_surf, backg_img = create_backg_surf(screen_w, screen_h)
                world_menu_top, world_menu_bottom = update_pictures(screen)

            if e.type == pg.KEYUP:
                if e.key == pg.K_w or e.key == pg.K_UP:
                    scroll_keys_hold[0] = False
                elif e.key == pg.K_s or e.key == pg.K_DOWN:
                    scroll_keys_hold[2] = False
                if e.key == pg.K_a or e.key == pg.K_LEFT:
                    scroll_keys_hold[1] = False
                elif e.key == pg.K_d or e.key == pg.K_RIGHT:
                    scroll_keys_hold[3] = False

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_w or e.key == pg.K_UP:
                    scroll_keys_hold[0] = True
                elif e.key == pg.K_s or e.key == pg.K_DOWN:
                    scroll_keys_hold[2] = True
                if e.key == pg.K_a or e.key == pg.K_LEFT:
                    scroll_keys_hold[1] = True
                elif e.key == pg.K_d or e.key == pg.K_RIGHT:
                    scroll_keys_hold[3] = True

                if e.key == pg.K_ESCAPE:
                    backg_surf = pg.Surface(screen.get_size())
                    grid_cables = teken_grid(screen, grid, grid_rotation, selected_x, selected_y, move_animation, scrollx, scrolly, screen_size,render_distance,storage,scale,scaled_pictures,blocks_index, grid_cables, brush, angle, grid_data)
                    loading_surf = setup_loading_screen(screen, backg_img)

                    draw_loading_screen_create_world(screen, clock, loading_surf, 10, 0, "Saving world...")

                    save_world(selected_world,grid,grid_rotation,grid_data,grid_cables,research_progress,storage,keybinds,research_grid,unlocked_recipes,creater_unlocked_recipes)

                    draw_loading_screen_create_world(screen, clock, loading_surf, 80, 10, "Saving player data...")

                    save_player_data(selected_world, start_play_perf)
                    in_menu = True
                    switch_menu_trigger = True

                    draw_loading_screen_create_world(screen, clock, loading_surf, 100, 80, "Returning to menu screen...")

                if e.key == pg.K_r:
                    mrr = (mrr - 1) % 4

                if e.key in [pg.K_0,pg.K_1,pg.K_2,pg.K_3,pg.K_4,pg.K_5,pg.K_6,pg.K_7,pg.K_8,pg.K_9]:
                    brush = keybinds[e.key-48]

                #debug keys
                if e.key == pg.K_k:
                    keybind_menu = not keybind_menu

                if e.key == pg.K_m:
                    scale = 1
                    scaled_pictures = scale_pictures(scale)

                if e.key == pg.K_p:
                    research_menu = not research_menu
                
                if e.key == pg.K_o:
                    print_timing = not print_timing
                
                if e.key in [pg.K_F1, pg.K_F2, pg.K_F3, pg.K_F4]:
                    open_menu = False
                    clicked_button = -1
                    clicked_icon = -1
                    selected_x, selected_y = -1, -1
                    edit_tile_menu_open = False
                    if e.key == pg.K_F1:
                        tile_mode = "place"
                    elif e.key == pg.K_F2:
                        tile_mode = "edit"
                    elif e.key == pg.K_F3:
                        tile_mode = "info" 
                    elif e.key == pg.K_F4:
                        tile_mode = "view"

                if e.key == pg.K_q:
                    if selected_world is not None:
                        in_menu = not in_menu

        if not research_menu:#normal scrolling in level
            if scroll_keys_hold[3] and abs(scrollx-scroll_speed) <= round((grid.shape[1])*50*scale-screen_size[0], 3):
                scrollx += -scroll_speed * deltaTime
            if scroll_keys_hold[1] and -(scrollx+scroll_speed) >= 0:
                scrollx += scroll_speed * deltaTime
            if scroll_keys_hold[2] and abs(scrolly-scroll_speed) <= round((grid.shape[0])*50*scale-screen_size[1], 3):
                scrolly += -scroll_speed * deltaTime
            if scroll_keys_hold[0] and -(scrolly+scroll_speed) >= 0:
                scrolly += scroll_speed * deltaTime
            
            scrollx = round(min(0,scrollx))
            scrolly = round(min(0,scrolly))

        elif research_menu:#scrolling in research menu
            if scroll_keys_hold[3]:
                r_scrollx[r_screen_page] += scroll_speed * deltaTime
            if scroll_keys_hold[1] and r_scrollx[r_screen_page] > -5:
                r_scrollx[r_screen_page] += -scroll_speed * deltaTime
            if scroll_keys_hold[2]:
                r_scrolly[r_screen_page] += scroll_speed * deltaTime
            if scroll_keys_hold[0] and r_scrolly[r_screen_page] > -5:
                r_scrolly[r_screen_page] += -scroll_speed * deltaTime
            
            if r_scrollx[r_screen_page] + screen_w > r_width[r_screen_page]:
                r_scrollx[r_screen_page] = r_width[r_screen_page] - screen_w
            if r_scrolly[r_screen_page] + screen_h > r_height[r_screen_page]:
                r_scrolly[r_screen_page] = r_height[r_screen_page] - screen_h

            if max(scroll_keys_hold): #if one of these is true, update scroll
                update_r_scroll = True

        if (-scrollx)+screen_size[0] > grid.shape[1]*50*scale:
            scrollx = -grid.shape[1]*50*scale+screen_size[0]

        if (-scrolly)+screen_size[1] > grid.shape[0]*50*scale:
            scrolly = -grid.shape[0]*50*scale+screen_size[1]

        t_mouse_and_locations = t.perf_counter()
        #add to grid
        mrx, mry = bereken_muis_pos(mx,my,scrollx,scrolly,scale)
        if (mouse_down or mouse_drag_brush) and mrx < grid.shape[1] and mry < grid.shape[0] and not (research_menu or tile_mode in ["edit", "info", "view"]):#click
            grid, grid_rotation, grid_data, storage, place_status = add_to_grid(mrx,mry,mrr,grid,grid_rotation,grid_data,brush,blocks_index[brush],blocks_index,storage,item_names,b_prices, grid_cables, big_tiles, placed_on_only,cannot_place_on, ground_blocks, grid_generation, grid_features_generation, strict_placement_tiles)
            locations, crafting_locations, cargo_locations, cargo_spawn_locations = update_locations(grid, spawn_items)
            # craft_data, item_spawn_dict, item_perf_time,cargo_spawn_list = update_item_spawn(grid,grid_rotation,item_spawn_dict,item_spawn_time,item_perf_time,locations,craft_data,cargo_spawn_list)
            append_per_spawn = generate_append_per_spawn(grid, grid_data, spawn_time, spawn_items, locations, blocks_index,creater_unlocked_recipes)

            mouse_down = False
        
        #teken grid
        if t.perf_counter() > move+0.025:
            move = t.perf_counter()
            for i in range(len(move_animation)):
                move_animation[i] += move_speed[i]
                move_animation[i] = move_animation[i] % 25

            #sync move_animation when not upgrading at the same time
            for x in range(len(move_animation)):
                for y in range(len(move_animation)):
                    if not x == y:
                        if move_speed[x] == move_speed[y] and move_animation[x] != move_animation[y]:
                            move_animation[y] = move_animation[x]  

        t_teken = t.perf_counter()

        grid_cables = teken_grid(screen, grid, grid_rotation, selected_x, selected_y,move_animation, scrollx, scrolly, screen_size,render_distance,storage,scale,scaled_pictures,blocks_index, grid_cables, brush, angle, grid_data)

        if not (research_menu or tile_mode in ["edit", "info", "view"]):
            placeable = check_placeable(mrx, mry, mrr, grid, grid_rotation, brush, blocks_index[brush], blocks_index, storage, b_prices, grid_cables, big_tiles, placed_on_only, cannot_place_on, ground_blocks, strict_placement_tiles, item_names)
            draw_preview_box(screen,tile_mode == "info",mrx,mry,mrr,brush,scrollx,scrolly,scale,scaled_pictures,blocks_index[brush], placeable, tile_mode == "edit")
        elif tile_mode in ["info", "edit"]:
            draw_preview_box(screen,tile_mode == "info",mrx,mry,mrr,brush,scrollx,scrolly,scale,scaled_pictures,blocks_index[brush], placeable, tile_mode == "edit")

        t_items_cargo = t.perf_counter()

        #items
        items_list, cargo_data, spawn_cooldown = spawn_cargo(cargo_locations,grid,cargo_data,items_list, spawn_cooldown)

        t_items = t.perf_counter()

        # craft_data, items_list = spawn_items(grid, grid_data, items_list, item_perf_time, craft_data, item_spawn_dict, cargo_spawn_list)
        items_list, craft_data, cargo_spawn_perf = spawn_pregenerated_items(items_list, craft_data, append_per_spawn, spawn_perf_counters, cargo_locations, cargo_spawn_locations, spawn_time, cargo_spawn_perf)

        t_research = t.perf_counter()

        craft_data,items_list = craft_items(crafting_locations, craft_data, grid, grid_rotation, grid_data, items_list)

        t_pop_items = t.perf_counter()

        pop_index = []
        for index, item in enumerate(items_list):
            if not item.kapot:
                storage,craft_data,grid_data,cargo_data = item.bepaal_richting(grid,grid_rotation,grid_data,storage,craft_data,conveyor_speed,deltaTime,grid_cables,cargo_data)
                item.beweeg(deltaTime)
                item.teken(screen,scale,scaled_pictures,scrollx,scrolly)
            else:
                pop_index.append(index)
        for index in list(sorted(pop_index))[::-1]:
            items_list.pop(index)

        t_teken_menu = t.perf_counter()

        #teken menu
        if selected_x > -1 and selected_y > -1:
            if tile_mode == "info":
                tile_info_mode, up_button, down_button = draw_tile_menu(screen,data_display,data_arrow,item_names,tile_names,tile_des,rect_info,grid,selected_x,selected_y,grid_data,craft_data)
            elif tile_mode == "edit":
                if update_edit_menu:
                    edit_menu_surf, crafter_btn_collidepoints, line_1, line_2 = draw_edit_menu(tile_menu_type, unlocked_recipes, craft_scrolly[tile_menu_type], item_names,creater_unlocked_recipes, creater_type, hover_recipe=hover_recipe)
                    update_edit_menu = False
                    rect_edit_menu, crafter_btn_collidepoints, line_1, line_2 = blit_tile_edit_menu(screen, edit_menu_surf, crafter_btn_collidepoints, line_1, line_2)
                else:
                    rect_edit_menu, crafter_btn_collidepoints = blit_tile_edit_menu(screen, edit_menu_surf, crafter_btn_collidepoints, line_1, line_2, False)

            else: 
                selected_x = -1
                selected_y = -1
        else:
            rect_edit_menu = pg.Rect((0,0),(0,0))

        if research_menu and update_r_screen: #update r_screen once (for 1 frame)
            r_screen = pg.Surface((r_width[r_screen_page], r_height[r_screen_page]),pg.SRCALPHA)
            r_screen, creater_menu_collidepoints = draw_research(screen,storage[0],r_screen,rect_ui,0,0,research_display,research_button_clicked,research_button_unclicked,research_progress,research_text,r_tile_text,research_subtext,r_prices,r_screen_page, research_grid,creater_unlocked_recipes)
            update_r_screen = False

        if not tile_mode == "view":
            if research_menu: #research menu is open
                screen.blit(r_screen_transparent,(0,0))
                if r_width[r_screen_page] < screen.get_width(): # total width of research screen is smaller than monitor width, so center research screen
                    r_scrollx[r_screen_page] = -int((screen.get_width() - r_width[r_screen_page]) / 2)
                if r_height[r_screen_page] < screen.get_height(): # same but with y/height
                    r_scrolly[r_screen_page] = -int((screen.get_height() - r_height[r_screen_page]) / 2)
                screen.blit(r_screen,(-r_scrollx[r_screen_page],-r_scrolly[r_screen_page]))
                exit_corner, r_icons_click_list = draw_research_fixed(screen, screen, research_display, storage[0], r_screen_page, mx,my,r_scrollx, r_scrolly)
                
                #TODO: add particles 
                r_particles = research_particles(screen,r_particles, deltaTime)
            else: #r menu closed
                icon_click_list,bar_width,bar_height,button_distance,button_click_list,button_width = teken_menu(screen,conveyor_research_progress_dict,research_progress,menu_pictures,open_menu,clicked_icon,clicked_button,menu_scrollx,scaled_pictures,b_prices,creater_unlocked_recipes)

            if keybind_menu:
                keyb_up_buttons,keyb_down_buttons = draw_keybind_menu(screen,k_scrolly,unlocked_blocks,data_display,data_arrow,rect_keybinds,keybinds)

            if my > screen_size[1] - bar_height and open_menu: #mouse in menu bar
                for button in range(len(button_click_list)):
                    if mx > button_click_list[button][0] and my > button_click_list[button][1]:
                        if mx < button_click_list[button][0]+button_width and my < button_click_list[button][1]+button_width:
                            draw_info_popup(screen,mx,my,menu_pictures,clicked_icon,button,tile_names,b_prices,info_ui,item_names,tile_des)

            if shortage_timer + 2.5 > t.perf_counter():
                draw_shortage_notification(screen,not_enough_picture,shortage_item)

        if not research_menu and not keybind_menu:
            tile_mode_btns, edit_tile_menu_rect = draw_tile_mode_menu(screen, tile_mode)


        if t.perf_counter() > autosave_perf + autosave_interval and autosave_active == False:
            autosave_active = True
            autosave_state = 0
            print("starting autosave")

        if autosave_active:
            autosave_state += 1
            autosave_part(selected_world,grid,grid_rotation,grid_data,grid_cables,research_progress,storage,keybinds,research_grid,unlocked_recipes,creater_unlocked_recipes, autosave_state)
            if autosave_state > 16:
                autosave_active = False
                autosave_perf = t.perf_counter()
                print("finished autosave")
        
        fps = clock.get_fps()
        screen.blit(i_title_font.render(str(int(fps)), True, (0,0,0)),(10,10))
        pg.display.flip()
        deltaTime = clock.tick(150)
        deltaTime = min(deltaTime, 100)
        angle += 1

        t_final = t.perf_counter()

        if print_timing:
            print(f"Timing: {t_mouse_and_locations - t_event} {t_teken-t_mouse_and_locations} {t_items_cargo - t_teken} {t_items - t_items_cargo} {t_research - t_items} {t_pop_items - t_research} {t_teken_menu - t_pop_items} {t_final - t_teken_menu}")

pg.display.quit()
pg.font.quit()
pg.quit()
sys.exit()