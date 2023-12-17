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
storage_categories_title_font = pg.font.Font('Fonts/Lato.ttf', 28)
storage_categories_count_font = pg.font.Font('Fonts/Lato.ttf', 23)

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
        self.all_menu_display_items = {} # self.menu_display_items but not cut for categories

        self.categories_rect = []
        self.selected_category_index = -1
        self.selected_category = ""

        self.start_line_x = 185 # where the line approx. is with margin excluded!
        self.category_scroll = 0 # how much the categories list is scrolled. 0 is default, 1 means that you can't see the top element anymore

        self.max_categories_displayed = 18 # how many categories can be displayed max
        self.max_lines_displayed = 12 # how many lines in main storage menu can be displayed max
        self.len_menu_display_items = 1 # length of self.menu_display_items before it is cut by self.category_scroll

        self.columns_in_menu = 5 # amount of columns in main menu of storage 
        #example of main storage layout
        '''
        self.main_storage_layout = [
            ["foods"],
            [1, 2, 3],
            ["minerals"],
            [4, 5, 6],
            ["accessories"],
            [7, 8, 9, 10, 11],
            [12, 13, 14],
            ["foods1"],
            [1, 2, 3]
        ]
        '''
        self.main_storage_layout = []
        self.main_storage_scrolly = 0


    def draw_storage_menu(self, screen):
        # draw storage bar (topleft)
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

        # draw storage btn located in storage bar
        screen.blit(self.pics[f"storage_select_{self.display_order}"], (self.storage_bar_display_size[0] - 50, self.topleft_margin[1] + 9))
        self.sort_btn_rect.x = self.storage_bar_display_size[0] - 50
        self.sort_btn_rect.y = self.topleft_margin[1] + 9
        
        # draw main menu of storage if opened
        self.categories_rect = []
        if self.menu_open:
            screen.blit(self.pics["storage_menu"], (self.topleft_margin[0], self.topleft_margin[1] + self.storage_bar_display_size[1] + 5))
            categories_blit_y = self.topleft_margin[1] + self.storage_bar_display_size[1] + 20
            j = 0 # i but only when category in menu_display_items
            for i, category in enumerate(self.all_menu_display_items):
                if category in self.menu_display_items:
                    if j > self.max_categories_displayed:
                        break

                    if self.selected_category_index == i:
                        category_text = storage_categories_font.render(str(category), True, (180, 180, 180))
                    else:
                        category_text = storage_categories_font.render(str(category), True, (255, 255, 255))
                    screen.blit(category_text, (25, categories_blit_y))
                    self.categories_rect.append([pg.Rect((25, categories_blit_y), category_text.get_size()), i])
                    categories_blit_y += 30
                    j += 1
        
            blit_scrolly = self.main_storage_scrolly
            j = 0 # how many lines blit so far
            for i, line in enumerate(self.main_storage_layout):
                if blit_scrolly >= 0:
                    if j <= self.max_lines_displayed:
                        j += 1
                        if type(line) is str:
                            if str(line) == self.selected_category:            
                                category_title = storage_categories_title_font.render(str(line).capitalize(), True, (180, 180, 180))
                            else:
                                category_title = storage_categories_title_font.render(str(line).capitalize(), True, (255, 255, 255))

                            screen.blit(category_title, (210, blit_scrolly + self.topleft_margin[1] + self.storage_bar_display_size[1] + 18))
                        else:
                            blit_x = 0
                            for item in line:
                                item_id = item
                                screen.blit(self.item_pics[item_id if item_id != 0 else 'r'], (210 + blit_x, blit_scrolly + self.topleft_margin[1] + self.storage_bar_display_size[1] + 18))
                                blit_x += 45
                                num = self.storage[item]
                                if self.storage[item] > 9999:
                                    num = self.compact_number(qty)
                                count_text = storage_categories_count_font.render(str(num), True, (255, 255, 255))
                                screen.blit(count_text, (210 + blit_x, blit_scrolly + self.topleft_margin[1] + self.storage_bar_display_size[1] + 18))
                                blit_x += 88
                    else:
                        break # no reason to continue looping
                blit_scrolly += 45

    def compact_number(self, num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        if magnitude > 9:
            return '999 Oct.+'
        return '{} {}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'k', 'M', 'B', 'T', 'Qa.', 'Qu.', 'Se.', 'Sep.', 'Oct.'][magnitude])

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
        
        self.len_menu_display_items = len(list(self.menu_display_items.keys()))
        self.all_menu_display_items = copy.copy(self.menu_display_items)

        keys = list(self.menu_display_items.keys())
        for i in range(self.category_scroll):
            del self.menu_display_items[keys[i]]

        self.main_storage_layout = []
        for disp_i in self.all_menu_display_items:
            self.main_storage_layout.append(str(disp_i))
            item_batch = [] # adding items in batches of 5 to main_storage_layout (5 = self.columns_in_menu)
            for item in self.all_menu_display_items[disp_i]: 
                item_batch.append(item)
                if len(item_batch) >= self.columns_in_menu:
                    self.main_storage_layout.append(item_batch)
                    item_batch = []
            if len(item_batch) > 0:
                self.main_storage_layout.append(item_batch)

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
                for rect, i in self.categories_rect:
                    if rect.collidepoint(mx, my):
                        if self.selected_category_index == i:
                            self.selected_category_index = -1
                            self.selected_category = ""
                        else:    
                            self.selected_category_index = i
                            self.selected_category = list(self.all_menu_display_items.keys())[i]
                            if self.selected_category in self.main_storage_layout:
                                self.main_storage_scrolly = -self.main_storage_layout.index(self.selected_category) * 45

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

    def scroll_in_menu(self, scroll, mx, my, unlocked_recipes, creater_unlocked_recipes):
        scroll_dir = "up" if scroll == 4 else "down" 
        if mx > self.start_line_x: # scrolling in the main part of storage menu
            if scroll_dir == "up":
                self.main_storage_scrolly = min(self.main_storage_scrolly + 45, 0)
            else:
                self.main_storage_scrolly = max(self.main_storage_scrolly - 45, -(len(self.main_storage_layout)-7) * 45)

        else: # in side bar
            if scroll_dir == "up":
                self.category_scroll = min(max(self.len_menu_display_items - 10, 0), self.category_scroll - 1)
            else:
                self.category_scroll = max(0, self.category_scroll+1)

            self.update_display_items(unlocked_recipes, creater_unlocked_recipes)
