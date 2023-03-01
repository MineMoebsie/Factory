import random as r
import time as t
import numpy as np
import pygame as pg
import os
import sys
import pdb

pg.init()
pg.font.init()

def loading_screen(screen,percent_vals,percent_in,load_font,process,only_show_text=False):
    percent_vals.append(percent_in)
    screen_w, screen_h = screen.get_size()
    screen.fill((0,0,0))
    
    bar_w = int(screen_w/2)
    bar_h = int(screen_w/10)

    x_bar = int((screen_w - bar_w) / 2)
    y_bar = int((screen_h - bar_h) / 2)

    text_blit = load_font.render(str(process),True,(255,255,255))
    text_w,text_h = text_blit.get_size()

    loop_amount = (percent_vals[-1] - percent_vals[-2]) * 0

    screen.blit(text_blit,((screen_w-text_w)/2,y_bar+bar_h+text_h/5))
    if not only_show_text:
        for x in range(loop_amount):
            percent = x * (percent_vals[-1] - percent_vals[-2]) / loop_amount + percent_vals[-2]
            pg.draw.rect(screen,(0,0,0),((x_bar,y_bar),((bar_w*(percent/100)),bar_h)))
            
            pg.draw.rect(screen,(255,255,255),((x_bar,y_bar),(bar_w,bar_h)),width=3,border_radius=5)
            pg.draw.rect(screen,(255,255,255),((x_bar,y_bar),((bar_w*(percent/100)),bar_h)),border_radius=5)
            pg.display.flip()
            pg.event.pump()

        return percent_vals

if __name__ == '__main__':
    pg.font.quit()
    pg.quit()