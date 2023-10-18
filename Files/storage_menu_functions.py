import time as t
import pygame as pg
import numpy as np
import random as r
import pdb
import json
import easing_functions
import os
import copy

storage_font = pg.font.Font('Fonts/Roboto.ttf', 20)
storage_categories_font = pg.font.Font('Fonts/Lato.ttf', 24)


class storageMenu:
    def __init__(self, storage):
        self.storage = storage

        self.prev_storage = storage # storage that will be updated every 10 seconds, then average will be calculated per item
        self.update_prev_storage_perf = -1
        self.avg_per_min_storage = {}

        self.storage_bar_display_size = (625, 63)

        self.pics = {}
        #order important for factory.py!!!
        self.load_imgs = [["UI/storage_display.png", self.storage_bar_display_size[0], self.storage_bar_display_size[1], "storage_display"],
                     ["UI/storage_select_most.png", 45, 45, "storage_select_most"],
                     ["UI/storage_select_least.png", 45, 45, "storage_select_least"],
                     ["UI/storage_select_fast.png", 45, 45, "storage_select_fast"],
                     ["UI/storage_select_slow.png", 45, 45, "storage_select_slow"],
                     ["UI/storage_menu.png", 900, 600, "storage_menu"]]

        for load_img in self.load_imgs:
            self.pics[load_img[3]] = pg.transform.scale(pg.image.load(f"Assets/{load_img[0]}"), (load_img[1], load_img[2])).convert_alpha()

        self.item_pics = {}
        load_item_pics = list(range(1, 42))
        load_item_pics.append('r')

        self.item_size = 35

        for load_item in load_item_pics:
            self.item_pics[load_item] = pg.transform.scale(pg.image.load(f"Assets/Items/item{load_item}.png"), (self.item_size, self.item_size))
        
        self.topleft_margin = [5, 5]

        self.display_items = [1, 2, 3] # items that are displayed in order 0 is left 
        self.amount_of_items_in_bar = 3
        self.display_order = "least"
        self.display_orders = ["most", "least", "fast", "slow"]
        self.start_view_items = 0 # start at index x view items (changed when scrolling)
        # self.pinned_items = [] # items that always show up 

        self.sort_btn_rect = pg.Rect((-1, -1), (self.pics["storage_select_most"].get_width(), self.pics["storage_select_most"].get_height()))

        '''
        Possible display orders:
        "most" - most to least
        "least" - least to most
        "fast" - most to least in produced parts per min
        "slow" - least to most in produced parts per min: only the things that are produced per min show up
        '''

        self.menu_open = True # bugger menu open or not

        self.unlocked_items = []

        with open("Data/storage_menu_layout.json") as f:
            self.storage_layout = json.load(f) # all items theoretically displayed
        self.menu_display_items = {} # all items displayed (only unlocked items)

        self.categories_rect = []
        self.selected_category_index = -1

        self.start_line_x = 150 # where the line approx. is with margin incl.

    def draw_storage_menu(self, screen):
        screen.blit(self.pics["storage_display"], self.topleft_margin)
        blit_x = 20
        blit_x_max = 550
        for item_id in self.display_items:
            if self.display_order in ["most", "least"]:
                qty = self.storage[item_id]
                if qty > 9999: # shorten from 9.999k to things like 150k, 3B etc.
                    qty = self.compact_number(qty)
            else: # display order "fast" or "slow"
                qty = str(round(self.avg_per_min_storage[item_id], 2))
                qty = qty + "/s"
            #check if item wanted to blit fits in menu
            w_item = self.item_size + 3
            w_text = storage_font.size(str(qty))[0] + 7
            if blit_x + w_item + w_text <= blit_x_max:
                screen.blit(self.item_pics[item_id if item_id != 0 else 'r'], (blit_x, 14 + self.topleft_margin[1]))
                blit_x += self.item_size + 3

                storage_text = storage_font.render(str(qty), True, (255, 255, 255))
                screen.blit(storage_text, (blit_x, 23))
                blit_x += storage_text.get_width() + 7
            else:
                break

        screen.blit(self.pics[f"storage_select_{self.display_order}"], (self.storage_bar_display_size[0] - 50, self.topleft_margin[1] + 9))
        self.sort_btn_rect.x = self.storage_bar_display_size[0] - 50
        self.sort_btn_rect.y = self.topleft_margin[1] + 9
        
        self.categories_rect = []
        if self.menu_open:
            screen.blit(self.pics["storage_menu"], (self.topleft_margin[0], self.topleft_margin[1] + self.storage_bar_display_size[1] + 5))
            categories_blit_y = self.topleft_margin[1] + self.storage_bar_display_size[1] + 20
            for i, category in enumerate(self.menu_display_items):
                if self.selected_category_index == i:
                    category_text = storage_categories_font.render(str(category), True, (180, 180, 180))
                else:
                    category_text = storage_categories_font.render(str(category), True, (255, 255, 255))
                screen.blit(category_text, (25, categories_blit_y))
                self.categories_rect.append(pg.Rect((25, categories_blit_y), category_text.get_size()))
                categories_blit_y += 30

    def compact_number(self, num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'k', 'M', 'B', 'T', 'Qa.', 'Qu.', 'Se.', 'Sep.', 'Oct.'][magnitude])

    def update_display_items(self, unlocked_recipes, creater_unlocked_recipes):
        self.display_items = []
        if self.display_order == "most":
            storage_sorted = {k: v for k, v in sorted(self.storage.items(), reverse=True, key=lambda item: item[1])}
            for item in storage_sorted:
                self.display_items = list(storage_sorted.keys())[:50]
        elif self.display_order == "least":
            storage_sorted = {k: v for k, v in sorted(self.storage.items(), reverse=False, key=lambda item: item[1])}
            for item in storage_sorted:
                self.display_items = list(storage_sorted.keys())[:50]
        elif self.display_order == "fast":
            avg_sorted = {k: v for k, v in sorted(self.avg_per_min_storage.items(), reverse=True, key=lambda item: item[1])}
            for avg_item in avg_sorted:
                if avg_sorted[avg_item] != 0.0:
                    self.display_items.append(avg_item)
        elif self.display_order == "slow":
            avg_sorted = {k: v for k, v in sorted(self.avg_per_min_storage.items(), reverse=False, key=lambda item: item[1])}
            for avg_item in avg_sorted:
                if avg_sorted[avg_item] != 0.0:
                    self.display_items.append(avg_item)


        delete_indexes = []
        for i, item in enumerate(self.display_items):
            if item not in self.item_pics and item != 0:
                delete_indexes.append(i)
        for del_ind in sorted(delete_indexes, reverse=True):
            self.display_items.pop(del_ind)

        self.amount_of_items_in_bar = len(self.display_items)

        for _ in range(self.start_view_items):
            self.display_items.pop(0)

        self.unlocked_items = copy.copy(unlocked_recipes)
        for creater_recipe in creater_unlocked_recipes:
            for item in creater_unlocked_recipes[creater_recipe]:
                self.unlocked_items.append(item)

        self.unlocked_items = list(dict.fromkeys(self.unlocked_items))

        self.menu_display_items = {}
        for category in self.storage_layout:
            self.menu_display_items[category] = []
            for item in self.storage_layout[category]:
                if item in self.unlocked_items:
                    self.menu_display_items[category].append(item)
            if self.menu_display_items[category] == []:
                del self.menu_display_items[category]
        
    def update_storage(self, storage, unlocked_recipes, creater_unlocked_recipes):
        self.storage = storage
        if self.update_prev_storage_perf + 10 <= t.perf_counter():
            for item in self.prev_storage.keys():
                self.avg_per_min_storage[item] = (self.storage[item] - self.prev_storage[item]) / 10 # 10 for the 10 seconds
            
            self.prev_storage = copy.copy(storage)
            self.update_prev_storage_perf = t.perf_counter()

        self.update_display_items(unlocked_recipes, creater_unlocked_recipes)

        return self.unlocked_items

    def mouse_interaction(self, mx, my, mouse_down):
        if mouse_down: # clicc
            if self.sort_btn_rect.collidepoint(mx, my):
                self.display_order = self.display_orders[(self.display_orders.index(self.display_order) + 1) % len(self.display_orders)]
                self.start_view_items = 0
            elif pg.Rect(self.topleft_margin, self.storage_bar_display_size).collidepoint(mx, my):
                self.menu_open = not self.menu_open
            elif self.menu_open:
                for i, rect in enumerate(self.categories_rect):
                    if rect.collidepoint(mx, my):
                        if self.selected_category_index == i:
                            self.selected_category_index = -1
                        else:    
                            self.selected_category_index = i

    def scroll_in_bar(self, scroll, unlocked_recipes, creater_unlocked_recipes):
        scroll_dir = "up" if scroll == 4 else "down" 
        if scroll_dir == "up":
            if self.display_order in ["most", "least"]:
                storage_len = min(50, self.amount_of_items_in_bar)
                self.start_view_items = min(storage_len-5, self.start_view_items+1)
            else:
                self.start_view_items = min(max(self.amount_of_items_in_bar, 5)-5, self.start_view_items+1)
        else:
            self.start_view_items = max(0, self.start_view_items-1)

        self.update_display_items(unlocked_recipes, creater_unlocked_recipes)
