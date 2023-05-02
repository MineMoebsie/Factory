import time as t
import pygame as pg
import numpy as np
import random as r
import pdb
import datetime
import json
import easing_functions
import os
from perlin_noise import PerlinNoise
import copy

from Files.factory_functions import *
from Files.item_spawn import *

with open("Data/ver.txt") as f:
    version = f.read()

pg.init()
pg.font.init()

menu_font = pg.font.Font('Fonts/Lato.ttf',30)
title_font = pg.font.Font('Fonts/Roboto.ttf',70)
ver_font = pg.font.Font('Fonts/Roboto-Light.ttf',15)

btn_font = pg.font.Font('Fonts/Roboto.ttf',40)
btn_wide_font = pg.font.Font('Fonts/Roboto.ttf',25)

btn_wide_disabled_font = pg.font.Font('Fonts/Roboto-Italic.ttf',25)
btn_wide_font_create = pg.font.Font('Fonts/Roboto-Bold.ttf',25)

world_title_font = pg.font.Font('Fonts/Lato.ttf', 52)
world_btn_font = pg.font.Font('Fonts/Roboto.ttf', 25)

textbox_font = pg.font.Font('Fonts/DMM-Mono.ttf', 30)
textbox_placeholder_font = pg.font.Font('Fonts/DMM-Mono-Italic.ttf', 30)


load_font = pg.font.Font('Fonts/Roboto-Light.ttf', 25)

btn_w, btn_h = (260,130)
menu_button = import_foto("UI/menu_button.png", btn_w, btn_h)
menu_button_hover = import_foto("UI/menu_button_hover.png", btn_w, btn_h)

btn_w_wide, btn_h_wide = (260,65)
menu_button_wide = import_foto("UI/menu_button_wide.png", btn_w_wide, btn_h_wide)
menu_button_wide_hover = import_foto("UI/menu_button_wide_hover.png", btn_w_wide, btn_h_wide)

btn_w_widexl, btn_h_widexl = (540,65)
menu_button_widexl = import_foto("UI/menu_button_widexl.png", btn_w_widexl, btn_h_widexl)
menu_button_widexl_hover = import_foto("UI/menu_button_widexl_hover.png", btn_w_widexl, btn_h_widexl)


btn_world_w, btn_world_h = (1000, 250)
world_select_button = import_foto("UI/world_select_button.png", btn_world_w, btn_world_h)
world_select_button_selected = import_foto("UI/world_select_button_selected.png", btn_world_w, btn_world_h)

world_menu_top_w, world_menu_top_h = (2500, 175)
# world_menu_top = import_foto("world_menu_top.png", world_menu_top_w, world_menu_top_h)

backg_pic_1 = import_foto("Blocks/10.png", 50, 50, convert=True)
backg_pic_2 = import_foto("Blocks/11.png", 50, 50, convert=True)

def debug_point(screen, point):
    pg.draw.circle(screen, (255,0,0), point, 5)

class Button:
    def __init__(self, screen, x, y, horizontal_align=False, text="Button", font=btn_font, id=None, disabled=False, color=(255,255,255), btn_type=""):
        self.horizontal_align = horizontal_align
        self.text = text
        self.font = font
        self.hover = False
        self.id = id
        self.type = "button"
        self.disabled = disabled
        self.color = color
    
        self.btn_type = btn_type
        if self.btn_type != "":
            self.btn_type = "_" + self.btn_type
            self.rect = pg.Rect(x, y, eval(f"btn_w{self.btn_type}"), eval(f"btn_h{self.btn_type}"))
        else:
            self.rect = pg.Rect(x, y, btn_w, btn_h)

        self.pic = eval(f"menu_button{self.btn_type}")
        self.pic_hover = eval(f"menu_button{self.btn_type}_hover")

        if self.horizontal_align:
            self.rect.x = int((screen.get_width() - self.rect.w) / 2)

        if self.disabled:
            self.textimg = self.font.render(self.text, True, (255, 0, 0))
        else:
            self.textimg = self.font.render(self.text, True, self.color)

    def update_disabled(self, disabled):
        self.disabled = disabled
        self.textimg = None # reset textimg
        if self.disabled:
            self.textimg = self.font.render(self.text, True, (100, 100, 100))
        else:
            self.textimg = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        if self.hover:
            screen.blit(self.pic_hover ,(self.rect.x, self.rect.y))
        else:
            screen.blit(self.pic ,(self.rect.x, self.rect.y))

        screen.blit(self.textimg, (int(self.rect.x + self.rect.w / 2 - self.textimg.get_width() / 2),
                                   int(self.rect.y + self.rect.h / 2 - self.textimg.get_height() / 2)))

    def update_hover(self, mx, my):
        self.hover = True if self.rect.collidepoint(mx, my) else False

    def update_click(self, clicked):
        self.clicked = True if (self.hover and clicked and not self.disabled) else False
        return self.clicked

class SettingsBtn(Button):
    def __init__(self, screen, x, y, horizontal_align=False, text="Button", font=btn_font, id=None, disabled=False, color=(255,255,255), btn_type="", setting="Setting", options=["Option 1", "Option 2", "Option 3"]):
        super().__init__(screen, x, y, horizontal_align, text, font, id, disabled, color, btn_type)
        self.setting = setting
        self.options = options
        self.current_setting = 0 # index of self.options
        self.text = f"{self.setting}: {self.options[self.current_setting]}"
        if self.setting == "Comming soon...":
            self.text = f"{self.setting}"
            self.disabled = True
            self.font = btn_wide_disabled_font
        self.update_disabled(self.disabled)
        # self.textimg = self.font.render(self.text, True, self.color)

    def update_click(self, clicked):
        self.clicked = True if (self.hover and clicked) else False
        if self.clicked and not self.disabled:
            self.current_setting = (self.current_setting + 1) % len(self.options)
            self.text = f"{self.setting}: {self.options[self.current_setting]}"
            self.update_disabled(self.disabled)
        return self.clicked

    def get_setting(self, world_options):
        if self.setting != "Comming soon...":
            world_options[self.setting] = self.options[self.current_setting] 
        return world_options


class WorldSelect:
    def __init__(self, pos, world_folder):
        self.pos = pos # pos in 1, 2, 3 ( * world_select_btn_h + some margin val)
        self.world_folder = world_folder
        self.selected = False
        self.margin_world_select = 10
        self.x, self.y = (-1000,-1000)
        self.img = None
        self.data_dict = {}
        self.update_data_dict()
        self.update_img()


    def update_data_dict(self):
        with open(f"Data/Saves/{self.world_folder}/player_data.txt") as f:
            self.data_dict = eval(f.read())

    def update_img(self):
        self.img = pg.Surface((btn_world_w, btn_world_h), pg.SRCALPHA)
        if not self.selected:
            self.img.blit(world_select_button, (0, 0))
        else:
            self.img.blit(world_select_button_selected, (0, 0))

        title_color = (255,255,255)
        details_color = (200,200,200)

        worldimg = world_title_font.render(f"{self.world_folder.replace('_', ' ')}", True, title_color) # f string in case of int/float?
        self.img.blit(worldimg, (50, 30))
        title_y = 30 + worldimg.get_height()
        margin_title_to_text = 5
        line_height = 40

        lastplayedimg = world_btn_font.render(f"Last played: {self.data_dict['last_played']}", True, details_color)
        self.img.blit(lastplayedimg, (50, title_y + margin_title_to_text))
        createdimg = world_btn_font.render(f"Created: {self.data_dict['created']}", True, details_color)
        self.img.blit(createdimg, (50, title_y + margin_title_to_text + line_height))
        createdimg = world_btn_font.render(f"Total playtime: {self.data_dict['playtime']}", True, details_color)
        self.img.blit(createdimg, (50, title_y + margin_title_to_text + line_height * 2))

        w_blit = int(btn_world_w / 2 + 25)

        lastplayedimg = world_btn_font.render(f"World mode: -", True, details_color)
        self.img.blit(lastplayedimg, (w_blit, title_y + margin_title_to_text))
        createdimg = world_btn_font.render(f"World type: -", True, details_color)
        self.img.blit(createdimg, (w_blit, title_y + margin_title_to_text + line_height))
        createdimg = world_btn_font.render(f"Version: {self.data_dict['version']}", True, details_color)
        self.img.blit(createdimg, (w_blit, title_y + margin_title_to_text + line_height * 2))



    def draw(self, screen, world_select_scrolly):
        self.x = round((screen.get_width() - btn_world_w) / 2)
        self.y = self.pos * btn_world_h + self.pos * self.margin_world_select - world_select_scrolly
        # if self.selected:
        #     screen.blit(world_select_button_selected, (self.x, self.y))
        # else:
        #     screen.blit(world_select_button, (self.x, self.y))

        if self.y + self.img.get_height() - 50 > 0 and self.y - 5 < screen.get_height(): 
            screen.blit(self.img, (self.x, self.y))

    def update_selected(self, mx, my, clicked, selected_world):
        if pg.Rect((self.x, self.y),(btn_world_w, btn_world_h)).collidepoint(mx,my) and clicked:
            self.selected = not self.selected
            self.update_img()
            return True
        elif selected_world != self.world_folder:
            self.selected = False
            self.update_img()
        return False

class Inputbox:
    def __init__(self, screen, x, y, width, maxwidth, height, placeholder="Type here...", center="middle", border_radius=10, border_width=10, max_chars=25,id_=""):
        scr_w, scr_h = screen.get_size()
        self.center = center # can be "", "right", "left"
        self.width = width
        self.maxwidth = maxwidth
        self.minwidth = width # current width as minwidth
        
        match self.center:
            case "middle":
                self.x = int((scr_w - self.width) / 2)
            case "left":
                self.x = int((scr_w / 2 - self.width) / 2)
            case "right":
                self.x = int((scr_w / 2 - self.width) / 2 + scr_w / 2)
            case other:
                self.x = x

        self.y = y
        self.height = height
        self.placeholder = placeholder
        self.active = False
        self.text = ""
        self.id = id_
        self.border_radius = border_radius
        self.border_width = border_width
        self.active_color = (40,140,144)
        self.inactive_color = (25, 85, 88)
        self.delete_cooldown = -1
        self.max_chars = max_chars

        self.render_text(screen)

    def draw(self, screen, keypresses):
        if self.active and keypresses[pg.K_BACKSPACE] and t.perf_counter() > self.delete_cooldown + 0.1:
            self.text = self.text[:-1]
            self.render_text(screen)
            self.delete_cooldown = t.perf_counter()

        width = min(self.width, self.maxwidth)
        pg.draw.rect(screen, (100,100,100), ((self.x, self.y), (width, self.height)), border_radius=self.border_radius)

        screen.blit(self.textimg, (self.x + int((self.width - self.textimg.get_width()) / 2), self.y + int((self.height - self.textimg.get_height()) / 2)))

        pg.draw.rect(screen, self.active_color if self.active else self.inactive_color, ((self.x, self.y), (width, self.height)), width=5, border_radius=self.border_radius)

    def render_text(self, screen):
        scr_w, scr_h = screen.get_size()

        if self.text == "":
            self.textimg = textbox_placeholder_font.render(self.placeholder, True, (200,200,200))
        else:
            self.textimg = textbox_font.render(self.text, True, (255,255,255))
   
        textimgw = self.textimg.get_width()
        if self.width < textimgw + 50:
            self.width = textimgw + 50
        elif self.width + 50 > textimgw:
            self.width = textimgw + 50
        self.width = min(max(self.width, self.minwidth), self.maxwidth)

        match self.center:
            case "middle":
                self.x = int((scr_w - self.width) / 2)
            case "left":
                self.x = int((scr_w / 2 - self.width) / 2)
            case "right":
                self.x = int((scr_w / 2 - self.width) / 2 + scr_w / 2)
            case other:
                self.x = x


    def handle_events(self, event, screen):
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.Rect((self.x, self.y), (min(self.width, self.maxwidth), self.height)).collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        
        if self.active:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.text = ''
                    self.active = False
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.max_chars >= len(self.text):
                        self.text += event.unicode
                self.render_text(screen)



def create_backg_surf(screen_w, screen_h, menu_screen="title"):
    backg_surf = pg.Surface((screen_w, screen_h), pg.SRCALPHA)
    backg_surf.fill((20,20,20))
    alpha_set = {"title": 50, "world_select": 130,"create": 200}
    backg_surf.set_alpha(alpha_set[menu_screen])

    backg_img = pg.Surface((screen_w, screen_h), pg.SRCALPHA)
    backg_img.blit(import_foto("UI/backg_ui.png", screen_w, screen_h), (0,0))
    backg_img.set_alpha(alpha_set[menu_screen])
    return backg_surf, backg_img

def blit_horizontally_centered(screen, img, y):
    screen.blit(img,(int((screen.get_width() - img.get_width()) / 2), int(y)))
    return int((screen.get_width() - img.get_width()) / 2), int(y) # returns optional x and y of blit destination

def draw_title_menu(screen, backg_surf, update_btn_list=False):
    btn_list = []
    screen.blit(backg_surf,(0,0))

    titleimg = title_font.render('''"Factory"''', True, (255,255,255))
    title_w, title_h = titleimg.get_size()
    blit_horizontally_centered(screen, titleimg, 15)

    verimg = ver_font.render(version, True, (255,255,255))
    screen.blit(verimg, (3, screen.get_height() - verimg.get_height() - 3))

    margin_title_to_btn = 20
    margin_between_btn = 20

    if update_btn_list: # text is for user only, id is what is actually used in code
        btn_list.append(Button(screen, 0, title_h + margin_title_to_btn + (btn_h + margin_between_btn) * 0, horizontal_align=True,text="Play",id="world_select"))
        btn_list.append(Button(screen, 0, title_h + margin_title_to_btn + (btn_h + margin_between_btn) * 1, horizontal_align=True,text="Settings",id="general_settings"))
        btn_list.append(Button(screen, 0, title_h + margin_title_to_btn + (btn_h + margin_between_btn) * 2, horizontal_align=True,text="Credits",id="credits"))
        btn_list.append(Button(screen, 0, title_h + margin_title_to_btn + (btn_h + margin_between_btn) * 3, horizontal_align=True,text="Quit",id="quit"))

    return btn_list

def draw_world_select_menu(screen, backg_surf, world_list, world_menu_top, world_menu_bottom, update_btn_list=False):
    screen_w, screen_h = screen.get_size()
    btn_list = []
    # screen.blit(backg_surf,(0,0))
    screen.blit(world_menu_top, (0,-25))
    # screen.blit(world_menu_bottom, (0,screen_h - world_menu_bottom.get_height()))
    # pg.draw.rect(screen, (41,70,71), ((0,0),(screen_w, title_h + 30)))

    # screen.blit(world_menu_top, (0,0))
    
    if update_btn_list:
        margin_title_to_btn = 20
        margin_between_btn = 10
        margin_button_vertical = 10

        btn_list.append(Button(screen, 0, screen_h - 3*btn_h_wide - 3*margin_button_vertical,text="Play selected world",btn_type="widexl",font=btn_wide_font,id="play_world", horizontal_align=True))
        btn_list.append(Button(screen, int(screen_w / 2 - btn_w_wide - margin_between_btn), screen_h - btn_h_wide - margin_button_vertical,text="Back",btn_type="wide",font=btn_wide_font,id="to_title"))
        btn_list.append(Button(screen, int(screen_w / 2 - btn_w_wide - margin_between_btn), screen_h - 2*btn_h_wide - 2*margin_button_vertical,text="Edit",btn_type="wide",font=btn_wide_font, id="edit_world"))
        btn_list.append(Button(screen, int(screen_w / 2 + margin_between_btn), screen_h - 2*btn_h_wide - 2*margin_button_vertical,text="Delete",btn_type="wide",font=btn_wide_font, id="delete_world"))
        btn_list.append(Button(screen, int(screen_w / 2 + margin_between_btn), screen_h - btn_h_wide - margin_button_vertical,text="Create",btn_type="wide",font=btn_wide_font,id="create_world"))

    return btn_list
    
def draw_create_menu(screen, backg_img, update_btn_list=False):
    screen.blit(backg_img, (0,0))
    titleimg = title_font.render('''Create a new world''', True, (255,255,255))
    title_w, title_h = titleimg.get_size()
    blit_horizontally_centered(screen, titleimg, 15)
    screen_w, screen_h = screen.get_size()

    if update_btn_list:
        btn_list = []
        input_box_list = []

        input_box_list.append(Inputbox(screen, 0, 120, 400, 500, 75, "World name...", id_="world_name"))
        input_box_list.append(Inputbox(screen, 0, 220, 400, 500, 75, "World seed...", id_="world_seed"))

        margin_from_centre = 10
        half_scr_w = screen_w/2

        btn_list.append(SettingsBtn(screen, half_scr_w - margin_from_centre - btn_w_widexl, 325, False, setting="World mode", font=btn_wide_font, btn_type="widexl", options=["Default", "Sandbox"]))

        btn_list.append(SettingsBtn(screen, half_scr_w + margin_from_centre, 325, False, setting="Comming soon...", font=btn_wide_font, btn_type="widexl", options=["Default", "Sandbox"]))

        btn_list.append(SettingsBtn(screen, half_scr_w - margin_from_centre - btn_w_widexl, 400, False, setting="Comming soon...", font=btn_wide_font, btn_type="widexl", options=["Default", "Sandbox"]))

        btn_list.append(SettingsBtn(screen, half_scr_w + margin_from_centre, 400, False, setting="Comming soon...", font=btn_wide_font, btn_type="widexl", options=["Default", "Sandbox"]))

        btn_list.append(Button(screen, half_scr_w - margin_from_centre - btn_w_wide, screen.get_height() - menu_button_wide.get_height() - 25, False, "Create world", font=btn_wide_font_create, btn_type="wide", id="confirm_create_world"))

        btn_list.append(Button(screen, half_scr_w + margin_from_centre, screen.get_height() - menu_button_wide.get_height() - 25, False, "Cancel", id="to_world_select", btn_type="wide", font=btn_wide_font))

        return btn_list, input_box_list


def update_pictures(screen):
    scr_w, scr_h = screen.get_size()
    world_menu_top = pg.image.load("Assets/UI/world_menu_top.png")
    world_menu_top = pg.transform.scale(world_menu_top, (scr_w, world_menu_top_h))
    titleimg = title_font.render('''Select a world''', True, (255,255,255))
    title_w, title_h = titleimg.get_size()
    blit_horizontally_centered(world_menu_top, titleimg, 38)
    
    world_menu_bottom = pg.image.load("Assets/UI/world_menu_bottom.png")
    pg.transform.scale(world_menu_bottom, (scr_w, world_menu_bottom.get_height()))

    return world_menu_top, world_menu_bottom

def read_world(world_folder, spawn_items):
    breedte, hoogte = 500,500
    unlocked_blocks = [0,1,12,13,14,15,20,23, 24, 25,33,34,35,36,37]
    conveyor_speed = [25.0,25.0,25.0,25.0,12.5,5]
    
    move_speed = [1.0,1.0,1.0,1.0,2.0]

    grid = np.loadtxt('Data/Saves/'+world_folder+'/grid.txt').reshape(breedte, hoogte)
    grid = grid.astype(int)
    grid_rotation = np.loadtxt('Data/Saves/'+world_folder+'/grid_rotation.txt').reshape(breedte, hoogte)
    grid_rotation = grid_rotation.astype(int)

    grid_generation = np.loadtxt('Data/Saves/'+world_folder+'/grid_generation.txt').reshape(breedte, hoogte)
    grid_generation = grid_generation.astype(float)
    grid_features_generation = np.loadtxt('Data/Saves/'+world_folder+'/grid_generation_features.txt').reshape(breedte, hoogte)
    grid_features_generation = grid_features_generation.astype(float)

    grid_cables = np.loadtxt('Data/Saves/'+world_folder+'/grid_cables.txt').reshape(breedte, hoogte)
    grid_cables = grid_cables.astype(int)

    grid_data_load = json.loads(open(f'Data/Saves/{world_folder}/grid_data.json').read())    
    grid_data = np.array(grid_data_load["data"]).reshape(grid_data_load["shape"])

    with open('Data/Saves/'+world_folder+'/unlocked_recipes.txt') as f:
        unlocked_recipes = eval(f.read())

    with open('Data/Saves/'+world_folder+'/creater_unlocked_recipes.json') as f:
        creater_unlocked_recipes = json.load(f)

    f = open('Data/Saves/'+world_folder+'/research_data.txt')
    research_progress_ = eval(f.read())
    f.close()

    move_speed = [1.0,1.0,1.0,1.0,2.0,0]

    for i in range(len(research_progress_[0])):
        if research_progress_[0][i] > -1:
            if i == 0 and research_progress_[0][i] == 0:
                continue
            for j in range(0, research_progress_[0][i] + 1):
                unlocked_blocks, conveyor_speed, move_speed = research_clicked_item(unlocked_blocks,i,j,research_progress_,conveyor_speed,move_speed)

    duplicate_blocks = []
    for x in unlocked_blocks:
        if not (x in duplicate_blocks):
            duplicate_blocks.append(x)
    unlocked_blocks = duplicate_blocks

    storage = {}
    for i in range(1000):
        storage[i] = 0

    f = open('Data/Saves/'+world_folder+'/storage.txt')
    storage_load = eval(f.read())
    f.close()

    for key in storage_load:
        storage[key] = storage_load[key]

    f = open('Data/Saves/'+world_folder+'/keybinds.txt')
    keybinds = eval(f.read())
    f.close()

    f = open('Data/Saves/'+world_folder+'/research_data.txt')
    research_progress = eval(f.read())
    f.close()

    f = open('Data/Saves/'+world_folder+'/research_grid.txt')
    research_grid = eval(f.read())
    f.close()

    return grid,grid_rotation,grid_cables,grid_data,unlocked_blocks,conveyor_speed,move_speed,storage,keybinds,research_progress,research_grid, grid_generation, grid_features_generation, unlocked_recipes, creater_unlocked_recipes

def save_world(world_folder,grid,grid_rotation,grid_data,grid_cables,research_progress,storage,keybinds,research_grid,unlocked_recipes,creater_unlocked_recipes):
    f = open('Data/Saves/'+world_folder+'/grid.txt','w')
    np.savetxt(f,grid.astype(int), fmt="%i")
    f.close()

    f = open('Data/Saves/'+world_folder+'/grid_rotation.txt','w')
    np.savetxt(f,grid_rotation.astype(int), fmt="%i")
    f.close()

    json_obj = {"shape": grid_data.shape, "data": grid_data.flatten().tolist()}
    with open('Data/Saves/'+world_folder+'/grid_data.json', "w") as f:
        json.dump(json_obj, f)

    f = open('Data/Saves/'+world_folder+'/grid_cables.txt','w')
    np.savetxt(f, grid_cables.reshape((1,-1)), fmt="%s")
    f.close()

    f = open('Data/Saves/'+world_folder+'/research_data.txt','w')
    f.write("{}".format(research_progress))
    f.close()

    f = open('Data/Saves/'+world_folder+'/storage.txt','w')
    f.write("{}".format(storage))
    f.close()

    f = open('Data/Saves/'+world_folder+'/keybinds.txt','w')
    f.write("{}".format(keybinds))
    f.close()

    f = open('Data/Saves/'+world_folder+'/research_grid.txt','w')
    f.write("{}".format(research_grid))
    f.close()

    with open('Data/Saves/'+world_folder+'/unlocked_recipes.txt','w') as f:
        f.write(str(unlocked_recipes))

    with open('Data/Saves/'+world_folder+'/creater_unlocked_recipes.json','w') as f:
        json.dump(creater_unlocked_recipes, f)


def save_player_data(world_folder, start_play_perf):
    with open('Data/Saves/'+world_folder+'/player_data.txt','r') as f:
        player_data_r = eval(f.read())

    with open('Data/Saves/'+world_folder+'/player_data.txt','w') as f:
        player_data = {}

        in_string = player_data_r['playtime']
        day_count = ""
        for char in in_string:
            try:
                if int(char) > -1:
                    day_count += char
            except ValueError:
                break
        day_count = int(day_count)

        time_part = in_string[-8:]
        x = t.strptime(time_part,'%H:%M:%S')
        sec = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
        sec += day_count * 86400

        player_data["playtime"] = str(datetime.timedelta(seconds=int(t.perf_counter() - start_play_perf + sec)))
        
        today = datetime.date.today()
        player_data["last_played"] = today.strftime("%b %d, %Y") # formats into Jan 2, 1918

        player_data["version"] = version

        player_data["created"] = player_data_r['created']

        player_data["seed"] = player_data_r['seed']

        player_data["mode"] = player_data_r['mode']
    
        f.write(str(player_data))

def setup_loading_screen(screen, backg_img):
    loading_screen = pg.Surface(screen.get_size())
    loading_screen.blit(screen, (0,0))
    loading_screen.blit(backg_img, (0,0))
    return loading_screen

def draw_loading_screen_create_world(screen, clock, loading_surf, percent, prev_percent, process):
    screen.blit(loading_surf, (0,0))
    screen_w, screen_h = screen.get_size()

    bar_w = int(screen_w/2)
    bar_h = int(screen_w/10)

    x_bar = int((screen_w - bar_w) / 2)
    y_bar = int((screen_h - bar_h) / 2)

    text_blit = load_font.render(str(process),True,(255,255,255))
    text_w,text_h = text_blit.get_size()

    loop_amount = 25
    ease_f = easing_functions.CubicEaseInOut(prev_percent, percent, loop_amount)
    for x in range(loop_amount):
        screen.blit(loading_surf, (0,0))

        percent = ease_f.ease(x)


        screen.blit(text_blit,((screen_w-text_w)/2,y_bar+bar_h+text_h/5))
        
        # pg.draw.rect(screen,(0,0,0),((x_bar,y_bar),((bar_w*(percent/100)),bar_h)))
        
        pg.draw.rect(screen,(255,255,255),((x_bar,y_bar),(bar_w,bar_h)),width=5,border_radius=15)
        if percent > 5:
            pg.draw.rect(screen,(255,255,255),((x_bar,y_bar),((bar_w*(percent/100)),bar_h)),border_radius=15)
        pg.event.pump()
        pg.display.flip()
        clock.tick(60)

def create_world(screen, loading_surf, clock, world_name, world_seed, world_options, version):#, world_name, world_seed, world_mode):
    height_grid, width_grid = (500,500)

    world_path = f'./Data/Saves/{world_name}' 
    if not os.path.exists(world_path) and world_name != "":
        draw_loading_screen_create_world(screen, clock, loading_surf, 10, 0, "Preparing world creation...")

        os.makedirs(world_path)

        #grid & rotation
        grid = np.zeros((height_grid,width_grid),dtype='int')
        grid_rotation = np.zeros((height_grid,width_grid),dtype='int') # 0 up, 1 right, 2 down, 3 left
        if world_seed == "": # generate random seed
            length = r.randint(5,50)
            for i in range(length):
                world_seed += str(r.randint(0, 9))
            world_seed = int(world_seed)
        elif type(world_seed) is str:
            new_seed = ""
            for i in range(len(world_seed)):
                if world_seed[i].isalpha() and world_seed[i].islower():
                    num = str(ord(world_seed[i])-96)
                    new_seed = new_seed + num
                elif world_seed[i].isalpha() and world_seed[i].isupper():
                    num = str(ord(world_seed[i])-38)
                    new_seed = new_seed + num
                elif world_seed[i]==' ':
                    new_seed = new_seed
                else:
                    new_seed = new_seed + world_seed[i]
            world_seed = int(new_seed)

        draw_loading_screen_create_world(screen, clock, loading_surf, 30, 10, "Generating noise...")

        grid_noise = PerlinNoise(octaves=15, seed=world_seed)
        grid_features_noise = PerlinNoise(octaves=15, seed=world_seed+100)
        
        draw_loading_screen_create_world(screen, clock, loading_surf, 40, 30, "Reading noise...")

        grid_generation = [[grid_noise([i/width_grid, j/height_grid]) for j in range(width_grid)] for i in range(height_grid)]
        pg.event.pump() # takes long time so update events
        grid_generation_features = [[grid_features_noise([i/width_grid, j/height_grid]) for j in range(width_grid)] for i in range(height_grid)]

        draw_loading_screen_create_world(screen, clock, loading_surf, 50, 40, "Creating grid...")

        for x in range(width_grid):
            for y in range(height_grid):
                generate_block(x, y, grid, grid_rotation, grid_generation, grid_generation_features)

        # TEMP 
        # import matplotlib.pyplot as plt
        # plt.imshow(grid_generation_features)
        # plt.imshow(grid)
        # plt.imshow(grid_generation)

        # plt.figure(1)
        # plt.pcolormesh(grid)
        # plt.colorbar()

        # plt.figure(2)
        # plt.pcolormesh(grid_generation_features)
        # plt.colorbar()

        # plt.figure(3)
        # plt.pcolormesh(grid_generation)
        # plt.colorbar()

        # plt.show()
        # TEMP

        with open(world_path+"/grid.txt","w") as f:
            np.savetxt(f, grid, fmt="%i")

        with open(world_path+"/grid_rotation.txt","w") as f:
            np.savetxt(f, grid_rotation, fmt="%i")    

        with open(world_path+"/grid_generation.txt","w") as f:
            np.savetxt(f, grid_generation, fmt="%f")

        with open(world_path+"/grid_generation_features.txt","w") as f:
            np.savetxt(f, grid_generation_features, fmt="%f")    

        draw_loading_screen_create_world(screen, clock, loading_surf, 65, 50, "Creating grid data...")

        #grid_data
        array_side = []
        for i in range(width_grid):
            array_side.append({}) 

        grid_data = []
        for i in range(height_grid):
            grid_data.append(copy.deepcopy(array_side))
        grid_data = np.array(grid_data)

        json_obj = {"shape": grid_data.shape, "data": grid_data.flatten().tolist()}

        with open(world_path+"/grid_data.json", "w") as f:
            json.dump(json_obj, f)

        draw_loading_screen_create_world(screen, clock, loading_surf, 70, 65, "Creating cables...")

        #grid_cables
        grid_cables = np.zeros((height_grid, width_grid), dtype="int")

        with open(world_path+"/grid_cables.txt", "w") as f:
            np.savetxt(f, grid_cables.reshape((1,-1)), fmt="%s")

        draw_loading_screen_create_world(screen, clock, loading_surf, 75, 70, "Making player keybinds...")

        #keybinds
        keybinds = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

        with open(world_path+"/keybinds.txt", "w") as f:
            f.write(str(keybinds))

        draw_loading_screen_create_world(screen, clock, loading_surf, 80, 75, "Creating research data...")

        #research_data
        research_data = [[0, -1, -1, -1, -1, -1]]
        with open(world_path+"/research_data.txt", "w") as f:
            f.write(str(research_data))

        #research_grid
        r_grid_size = 15
        research_grid = []
        for row in range(r_grid_size):
            row_line = []
            for index in range(r_grid_size):
                if row == int(r_grid_size / 2) and index == int(r_grid_size / 2):
                    row_line.append([True, False])
                else:
                    row_line.append([False, False])
                    
            research_grid.append(row_line[:])

        with open(world_path+"/research_grid.txt", "w") as f:
            f.write(str(research_grid))

        draw_loading_screen_create_world(screen, clock, loading_surf, 90, 80, "Clearing storage...")

        #storage
        storage = {}
        for x in range(26):
            storage[x] = 0
        storage[0] = 100
        with open(world_path+"/storage.txt", "w") as f:
            f.write(str(storage))

        draw_loading_screen_create_world(screen, clock, loading_surf, 95, 90, "Storing player data...")

        #unlocked recipes
        with open(world_path+"/unlocked_recipes.txt", "w") as f:
            f.write(str("[]"))

        with open(world_path+"/creater_unlocked_recipes.json", "w") as f:
            json.dump({}, f)

        #player_data
        player_data = {'playtime': '0:00:00', 'last_played': datetime.date.today().strftime("%b %d, %Y"), 'version': version, 'created': datetime.date.today().strftime("%b %d, %Y"), 'seed': world_seed, 'mode': world_options["World mode"]}

        with open(world_path+"/player_data.txt", "w") as f:
            f.write(str(player_data))

        draw_loading_screen_create_world(screen, clock, loading_surf, 100, 95, "Loading world...")

if __name__ == '__main__':
    pg.font.quit()
    pg.quit()