import time as t
import pygame as pg
import numpy as np
import random as r
import pdb
import json
import easing_functions
import os

storage_font = pg.font.Font('Fonts/Roboto.ttf', 20)

class storageMenu:
    def __init__(self, storage):
        self.storage = storage
        
        self.pics = {}
        load_imgs = [["UI/storage_display.png", 625, 63, "storage_display"]]

        for load_img in load_imgs:
            self.pics[load_img[3]] = pg.transform.scale(pg.image.load(f"Assets/{load_img[0]}"), (load_img[1], load_img[2])).convert_alpha()

        self.item_pics = {}
        load_item_pics = list(range(1, 42))
        load_item_pics.append('r')

        self.item_size = 35

        for load_item in load_item_pics:
            self.item_pics[load_item] = pg.transform.scale(pg.image.load(f"Assets/Items/item{load_item}.png"), (self.item_size, self.item_size))
        
        self.topleft_margin = [5, 5]

        self.display_items = [1, 2, 3] # items that are displayed in order 0 is left 
        self.display_order = "most"
        self.pinned_items = [] # items that show up when display order is "pinned"
        '''
        Possible display orders:
        "most" - most to least
        "least" - least to most
        "fast" - most to least in produced parts per min
        "slow" - least to most in produced parts per min: only the things that are produced per min show up
        "pinned" - show pinned items
        '''

    def draw_storage_menu(self, screen):
        screen.blit(self.pics["storage_display"], self.topleft_margin)
        blit_x = 20
        blit_x_max = 600
        for item_id in self.display_items:
            qty = self.storage[item_id]
            if qty > 9999: # shorten from 9.999k to things like 150k, 3B etc.
                qty = self.compact_number(qty)
            #check if item wanted to blit fits in menu
            w_item = self.item_size + 3
            w_text = storage_font.size(str(qty))[0] + 7
            if blit_x + w_item + w_text <= blit_x_max:
                screen.blit(self.item_pics[item_id if item_id != 0 else 'r'], (blit_x, 14 + self.topleft_margin[1]))
                blit_x += self.item_size + 3

                storage_text = storage_font.render(str(qty), True, (0, 0, 0))
                screen.blit(storage_text, (blit_x, 23))
                blit_x += storage_text.get_width() + 7
            else:
                break

    def compact_number(self, num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


        return number

    def update_display_items(self):
        self.display_items = []
        if self.display_order == "most":
            storage_sorted = {k: v for k, v in sorted(self.storage.items(), reverse=True, key=lambda item: item[1])}
            for item in storage_sorted:
                self.display_items = list(storage_sorted.keys())[:50]
        elif self.display_order == "least":
            storage_sorted = {k: v for k, v in sorted(self.storage.items(), reverse=False, key=lambda item: item[1])}
            for item in storage_sorted:
                self.display_items = list(storage_sorted.keys())[:50]

        delete_indexes = []
        for i, item in enumerate(self.display_items):
            if item not in self.item_pics and item != 0:
                delete_indexes.append(i)
        for del_ind in reversed(delete_indexes):
            self.display_items.pop(del_ind)


    def update_storage(self, storage):
        self.storage = storage
        self.update_display_items()
