import time as t
import pygame as pg
import numpy as np
import random as r
import pdb
import json
import easing_functions
import os

class storageMenu:
    def __init__(self, storage):
        self.storage = storage
        
        self.pics = {}
        load_imgs = [["UI/storage_display.png", 500, 63, "storage_display"]]

        for load_img in load_imgs:
            self.pics[load_img[3]] = pg.transform.scale(pg.image.load(f"Assets/{load_img[0]}"), (load_img[1], load_img[2])).convert_alpha()

        self.item_pics = {}
        load_item_pics = list(range(1, 42))
        load_item_pics.append('r')

        self.item_size = 50

        for load_item in load_item_pics:
            self.item_pics[load_item] = pg.transform.scale(pg.image.load(f"Assets/Items/item{load_item}.png"), (self.item_size, self.item_size))
        
        print(self.pics, self.item_pics)

    def draw_storage_menu(self, screen):
        screen.blit(self.pics["storage_display"], (0, 0))

    def update_storage(self, storage):
        self.storage = storage
