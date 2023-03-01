
if __name__ == "factory_functions_copy":
    import multiprocessing
    import random as r
    import time as t
    import numpy as np
    import pygame as pg
    import pdb
    from factory_mp import *

    pg.init()
    pg.font.init()

    scherm = pg.display.set_mode((1000, 600), pg.RESIZABLE)


    def import_foto(name, sizex=50, sizey=50, convert=False):
        foto_rauw = pg.image.load('Assets/' + str(name))
        if convert:  # convert = faster, but no transparency
            foto_af = pg.transform.scale(foto_rauw, (sizex, sizey)).convert()
        else:
            foto_af = pg.transform.scale(foto_rauw, (sizex, sizey)).convert_alpha()
        return foto_af


    grid_size = 50
    item_size = 15
    side_size = int(grid_size / 5)

    conveyor_connect_list = [1, 2, 3, 4, 5, 6, 7, 15, -15, -16, 16, -17, 17]
    extra_conveyor_list = [12, 13, 14, 33, 34, 35]

    item_font = pg.font.Font('Fonts/Lato.ttf', 20)
    r_display_font = pg.font.Font('Fonts/Roboto-Light.ttf', 30)
    r_title_font = pg.font.Font('Fonts/Roboto-Bold.ttf', 19)
    r_subtitle_font = pg.font.Font('Fonts/Roboto-Light.ttf', 16)
    r_font = pg.font.Font('Fonts/Roboto.ttf', 15)

    i_title_font = pg.font.Font('Fonts/Roboto-Bold.ttf', 25)
    i_text_font = pg.font.Font('Fonts/Roboto.ttf', 16)
    i_des_font = pg.font.Font('Fonts/Roboto-Light.ttf', 17)

    picture_arrow = import_foto('arrow-single.png', grid_size, grid_size)
    picture_arrow_cross = import_foto('arrow-cross.png', grid_size, grid_size)
    picture_arrow_split_r = import_foto('arrow-split-right.png', grid_size, grid_size)
    picture_arrow_split_l = import_foto('arrow-split-left.png', grid_size, grid_size)
    picture_arrow_sort_r = import_foto('arrow-sorting-right.png', grid_size, grid_size)
    picture_arrow_sort_l = import_foto('arrow-sorting-left.png', grid_size, grid_size)
    picture_arrow_highway = import_foto('arrow-highway.png', grid_size, grid_size)

    picture_arrow_cable = import_foto('arrow-cable.png', grid_size, grid_size)

    r_particle_picture = import_foto('itemr.png', item_size * 3, item_size * 3)
    r_icon_picture = import_foto('itemr.png', 29, 29)
    r_display_picture = import_foto('itemr.png', 44, 44)
    # menu stuff
    menu_bar_picture = import_foto('menu_bar.png', 1000, 200)
    icon_clicked_picture = import_foto('menu_icon_clicked.png', 50, 50)
    icon_unclicked_picture = import_foto('menu_icon_unclicked.png', 50, 50)

    button_clicked_picture = import_foto('menu_button_clicked.png', 125, 125)
    button_unclicked_picture = import_foto('menu_button_unclicked.png', 125, 125)

    research_button_clicked = import_foto('research_button_clicked.png', 1000, 500)
    research_button_unclicked = import_foto('research_button.png', 1000, 500)
    research_display = import_foto('research_display.png', 1000, 500)

    info_ui = import_foto('info_ui.png',600,400)

    lock_picture = import_foto('lock.png', 50, 50)

    rect_ui = import_foto('rect_ui.png', 2500, 2500, True)
    rect_info = import_foto('info_rect.png', 750, 1000)
    rect_keybinds = import_foto('keybind_rect.png', 750, 2000)

    data_display = import_foto('data_display.png', 250, 165)
    data_arrow = import_foto('data_arrow.png', 250, 215)

    not_enough_picture = import_foto('not_enough.png', 2000, 500)

    icon_1 = import_foto('menu_icon_1.png', 50, 50)
    icon_2 = import_foto('menu_icon_2.png', 50, 50)
    icon_3 = import_foto('menu_icon_3.png', 50, 50)
    icon_4 = import_foto('menu_icon_4.png', 50, 50)
    icon_5 = import_foto('menu_icon_5.png', 50, 50)
    icon_6 = import_foto('menu_icon_6.png', 50, 50)
    icon_cross = import_foto('menu_icon_cross.png', 50, 50)

    # blocks
    picture_0 = import_foto('0.png', grid_size, grid_size)
    picture_1 = import_foto('01.png', grid_size, grid_size, True)  # conveyor
    picture_2 = import_foto('01.png', grid_size, grid_size, True)  # cross-conveyor
    picture_3 = import_foto('01.png', grid_size, grid_size, True)  # split-conveyor-r
    picture_4 = import_foto('01.png', grid_size, grid_size, True)  # split-conveyor-l
    picture_5 = import_foto('01.png', grid_size, grid_size, True)  # sort-conveyor-r
    picture_6 = import_foto('01.png', grid_size, grid_size, True)  # sort-conveyor-l
    picture_7 = import_foto('01.png', grid_size, grid_size, True)  # highway-conveyor

    picture_8 = import_foto('8.png', grid_size, grid_size)
    picture_9 = import_foto('9.png', grid_size, grid_size)

    picture_10 = import_foto('10.png', grid_size, grid_size, True)
    picture_11 = import_foto('11.png', grid_size, grid_size, True)
    picture_12 = import_foto('12.png', grid_size * 3, grid_size * 3)
    picture_13 = import_foto('13.png', grid_size * 4, grid_size * 4)
    picture_14 = import_foto('14.png', grid_size * 5, grid_size * 5)
    picture_15 = import_foto('15.png', grid_size * 3, grid_size * 3, True)
    picture_16 = import_foto('16.png', grid_size * 3, grid_size * 3, True)
    picture_17 = import_foto('17.png', grid_size * 3, grid_size * 3, True)
    picture_18 = import_foto('18.png', grid_size, grid_size)
    #picture_19 = import_foto('19.png', grid_size, grid_size, True)
    picture_20 = import_foto('20.png', grid_size * 3, grid_size * 3, True)# storage temp

    picture_21 = import_foto('21.png', grid_size, grid_size, True)
    picture_22 = import_foto('22.png', grid_size, grid_size, True)

    picture_23 = import_foto('23.png', grid_size, grid_size, True)
    picture_24 = import_foto('24.png', grid_size, grid_size, True)

    picture_25 = import_foto('25_base.png', grid_size, grid_size, True)
    picture_26 = import_foto('25_arm.png', grid_size * 3, grid_size * 3)

    picture_33 = import_foto('33.png', grid_size * 3, grid_size * 3, True)
    picture_34 = import_foto('34.png', grid_size * 4, grid_size * 4, True)
    picture_35 = import_foto('35.png', grid_size * 5, grid_size * 5, True)
    picture_list = [0, 1, 2, 3, 4, 5, 6, 7, 8,9,10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 33, 34, 35]
    # items
    lst = []

    for x in range(22):
        lst.append(import_foto('item{}.png'.format(x if x != 0 else 'r'), item_size, item_size))
    item_0_picture, item_1_picture, item_2_picture, item_3_picture, item_4_picture, item_5_picture, item_6_picture, \
    item_7_picture, item_8_picture, item_9_picture, item_10_picture, item_11_picture, item_12_picture, item_13_picture, \
    item_14_picture, item_15_picture, item_16_picture, item_17_picture, item_18_picture, item_19_picture, item_20_picture, \
    item_21_picture = lst

    item_c_picture = import_foto('itemc.png', item_size, item_size) 

    items_pictures = list(range(0, 22))  # list of all the items (0,1,2 etc)
    items_pictures.append('c')

    # add to scale lists
    scaled_pictures = {}
    pictures_scales = {}
    for i in range(len(picture_list)):
        scaled_pictures[str('picture_' + str(picture_list[i]))] = [pg.transform.rotate(
            eval('picture_' + str(picture_list[i])), -angle) for angle in range(0, 360, 90)]
        pictures_scales[str('picture_' + str(picture_list[i]))] = [round(
            float(eval('picture_' + str(picture_list[i])).get_size()[0] / grid_size)) for angle in range(0, 360, 90)]
    for i in range(len(items_pictures)):
        scaled_pictures[str('item_' + str(items_pictures[i]) + '_picture')] = [pg.transform.rotate(eval(
            'item_' + str(items_pictures[i]) + '_picture'), -angle) for angle in range(0, 360, 90)]
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
        conveyor_frames['picture_1_' + str(i + 1)] = [import_foto("01-" + str(i + 1) + ".png", grid_size, grid_size) for angle in range(0, 360, 90)]
        scaled_pictures['picture_1_' + str(i + 1)] = [pg.transform.rotate(import_foto("01-" + str(i + 1) + ".png", grid_size, grid_size), -angle) for angle in range(0, 360, 90)]
        pictures_scales['picture_1_' + str(i + 1)] = [1 for angle in range(0, 360, 90)]

    # research frames (25)
    research_frames = {}


    def generate_random_background(tile1,tile2,size):
        picture = pg.Surface((grid_size * size, grid_size * size))
        for x in range(3):
            for y in range(3):
                picture.blit(pg.transform.rotate(eval('picture_'+str(r.choice([tile1,tile2]))),r.randint(0,3)*90),(x*grid_size,y*grid_size))
        return picture

    #for x in range(3):
    #    for y in range(3):
    #        picture_random.blit(pg.transform.rotate(eval('picture_'+str(r.randint(10,11))),r.randint(0,3)*90),(x*grid_size,y*grid_size))

    picture_random = generate_random_background(10,11,3)

    for i in range(0,25):
        picture = pg.Surface((grid_size * 3, grid_size * 3))
        picture.blit(picture_random,(0,0))
        picture.blit(import_foto("15-" + str(i + 1) + ".png", grid_size * 3, grid_size * 3),(0,0))
        picture = pg.transform.rotate(picture, 180) #image is upside down
        research_frames['picture_15_' + str(i + 1)] = [picture for angle in range(0, 360, 90)]
        scaled_pictures['picture_15_' + str(i + 1)] = [pg.transform.rotate(picture, -angle) for angle in range(0, 360, 90)]
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

    crafter_frames = {}
    crafter_colors = ["black","dark_blue","dark_green","dark_red","gray","light_blue","light_green","orange","pink","purple","red","yellow"]
    crafter_picture_colors = {}
    for i in crafter_colors:
        crafter_picture_colors[i] = [pg.transform.rotate(import_foto("base_research_"+str(i)+".png",150,150), -angle) for angle in range(0, 360, 90)]

    crafter_craftables = {'r':"dark_blue"}

    for color in crafter_colors:
        crafter_frames[str(color)] = {}
        picture_random = generate_random_background(10,11,3)
        for i in range(25):
            final_picture = pg.Surface((150,150))
            final_picture.blit(picture_random,(0,0))
            final_picture.blit(research_frames["picture_15_"+str(i + 1)][0],(0,0))
            final_picture.blit(crafter_picture_colors[color][0],(0,0))

            if color == "dark_blue":
                pictjure = final_picture

            crafter_frames[str(color)][i+1] = [pg.transform.rotate(final_picture, -angle) for angle in range(0, 360, 90)]
            pictures_scales['picture_15_' + str(i + 1)] = [3 for angle in range(0, 360, 90)]

    for craftable in crafter_craftables.keys():
        crafter_frames[craftable] = {}
        picture_random = generate_random_background(10,11,3)
        for i in range(25):
            color = crafter_craftables[craftable]
            final_picture = pg.Surface((150,150))
            final_picture.blit(picture_random,(0,0))
            final_picture.blit(research_frames["picture_15_"+str(i + 1)][0],(0,0))
            final_picture.blit(crafter_picture_colors[color][0],(0,0))

            item_blit_size = 50
            item_blit_picture = import_foto("item"+str(craftable)+".png")
            item_blit_picture = pg.transform.scale(item_blit_picture,(item_blit_size,item_blit_size))

            final_picture.blit(item_blit_picture,(int((150-item_blit_size)/2),int((150-item_blit_size)/2)))

            crafter_frames[craftable][i+1] = [pg.transform.rotate(final_picture, -angle) for angle in range(0, 360, 90)]
            pictures_scales['picture_15_' + str(i + 1)] = [3 for angle in range(0, 360, 90)]



    #print("crafter_frames!!!")
    #print(crafter_frames)



    def scale_pictures(scale, grid_size=grid_size, item_size=item_size, scaled_pictures=scaled_pictures):
        for key in scaled_pictures.keys():
            if 'item' in key:  # item
                scaled_pictures[key] =[pg.transform.rotate(pg.transform.scale(eval(key), (
                    int(np.ceil(pictures_scales[key][int(angle/90)] * scale * item_size)),
                    int(np.ceil(pictures_scales[key][int(angle/90)] * scale * item_size)))), -angle) for angle in range(0, 360, 90)]
            elif 'picture_1_' in key:  # animated conveyor
                scaled_pictures[key] = [pg.transform.rotate(pg.transform.scale(conveyor_frames[key][int(angle/90)], (
                    int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
                    int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))), -angle) for angle in range(0, 360, 90)]
            elif 'picture_15_' in key:
                scaled_pictures[key] = [pg.transform.rotate(pg.transform.scale(research_frames[key][int(angle/90)], (
                    int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
                    int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))), -angle) for angle in range(0, 360, 90)]   
            else:
                scaled_pictures[key] = [pg.transform.rotate(pg.transform.scale(eval(key), (
                    int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)),
                    int(np.ceil(pictures_scales[key][int(angle/90)] * scale * grid_size)))), -angle) for angle in range(0, 360, 90)]
        return scaled_pictures


    def _grid_function_old(coords):
        x, y, g_grid, g_grid_rotation, g_scale, g_scrollx, g_scrolly, g_grid_size = coords
        built = g_grid[y, x]
        orientation = g_grid_rotation[y, x]
        x_grid_scale = round(x * g_grid_size * g_scale) + g_scrollx
        y_grid_scale = round(y * g_grid_size * g_scale) + g_scrolly
        if built in [10, 11, 21, 22]:  # ground
            image = ["picture_" + str(built), orientation]
            loc = [(x_grid_scale, y_grid_scale)]
        else:
            image = []
            loc = []
        return [image, loc]



    def teken_grid_mp(scherm, grid, grid_rotation, selected_x, selected_y, move, scrollx, scrolly, screen_size, 
                    render_distance, storage, scale, scaled_pictures, blocks_index, grid_cables, brush, angle,grid_data, 
                    conveyor_connect_list=conveyor_connect_list):

        res = teken_grid_mp_core(scherm, grid, grid_rotation, selected_x, selected_y, move, scrollx, scrolly, screen_size, 
                render_distance, storage, scale, scaled_pictures, blocks_index, grid_cables, brush, angle,grid_data, grid_size 
                )
        for block in res:
            if block[0] != []: 
                scherm.blit(scaled_pictures[block[0][0]][block[0][1]], block[1][0])



    def teken_grid(scherm, grid, grid_rotation, selected_x, selected_y, move, scrollx, scrolly, screen_size,
                render_distance, storage, scale, scaled_pictures, blocks_index, grid_cables, brush, angle,grid_data, queue=None,
                conveyor_connect_list=conveyor_connect_list):
        scherm = scherm
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

                

                if built in [10, 11, 21, 22]:  # ground
                    scherm.blit(scaled_pictures["picture_" + str(built)][orientation],
                                    (x_grid_scale, y_grid_scale))

                elif built in [1, 2, 3, 4, 5, 6, 7]:  # conveyors
                    scherm.blit(scaled_pictures["picture_1_" + str(int(move[move_dict[built]] + 1))][orientation], (x_grid_scale, y_grid_scale))

                    if built == 1:  # conveyor
                        scherm.blit(scaled_pictures["picture_arrow"][orientation],
                                        (x_grid_scale, y_grid_scale))
                    elif built == 2:  # cross-conveyor
                        scherm.blit(scaled_pictures["picture_arrow_cross"][orientation],
                                        (x_grid_scale, y_grid_scale))
                    elif built == 3:  # split-conveyor-r
                        scherm.blit(scaled_pictures["picture_arrow_split_r"][orientation],
                                        (x_grid_scale, y_grid_scale))
                    elif built == 4:  # split-conveyor-l
                        scherm.blit(scaled_pictures["picture_arrow_split_l"][orientation],
                                        (x_grid_scale, y_grid_scale))
                    elif built == 5:  # sort-conveyor-r
                        scherm.blit(scaled_pictures["picture_arrow_sort_r"][orientation],
                                        (x_grid_scale, y_grid_scale))
                    elif built == 6:  # sort-conveyor-l
                        scherm.blit(scaled_pictures["picture_arrow_sort_l"][orientation],
                                        (x_grid_scale, y_grid_scale))
                    elif built == 7:  # highway-conveyor
                        scherm.blit(scaled_pictures["picture_arrow_highway"][orientation],
                                        (x_grid_scale, y_grid_scale))

                    pg.draw.rect(scherm, (82, 82, 82), (
                    (x_grid_scale, y_grid_scale), (round(side_size * scale), round(side_size * scale))))  # linksboven
                    pg.draw.rect(scherm, (82, 82, 82), (
                    (round((x * grid_size + grid_size - side_size) * scale + scrollx), round(y * grid_size * scale) + scrolly),
                    (round(side_size * scale), round(side_size * scale))))  # rechtsboven
                    pg.draw.rect(scherm, (82, 82, 82), (
                    (round(x * grid_size * scale)+ scrollx, round((y * grid_size + grid_size - side_size) * scale)+ scrolly),
                    (round(side_size * scale), round(side_size * scale))))  # linksonder
                    pg.draw.rect(scherm, (82, 82, 82), ((round((x * grid_size + grid_size - side_size) * scale)+ scrollx,
                                                            round((y * grid_size + grid_size - side_size) * scale)+ scrolly), (
                                                            round(side_size * scale),
                                                            round(side_size * scale))))  # rechtsonder

                    side_scale = round(side_size * scale)

                    if y > 0:
                        if not grid[y - 1, x] in conveyor_connect_list:
                            pg.draw.rect(scherm, (82, 82, 82),
                                        ((x_grid_scale, y_grid_scale), (round(grid_size * scale), side_scale)))
                    else:
                        pg.draw.rect(scherm, (82, 82, 82),
                                    ((x_grid_scale, y_grid_scale), (round(grid_size * scale), side_scale)))

                    if x > 0:
                        if not grid[y, x - 1] in conveyor_connect_list:
                            pg.draw.rect(scherm, (82, 82, 82),
                                        ((x_grid_scale, y_grid_scale), (side_scale, round(grid_size * scale))))
                    else:
                        pg.draw.rect(scherm, (82, 82, 82),
                                    ((x_grid_scale, y_grid_scale), (side_scale, round(grid_size * scale))))

                    if x < grid.shape[0] - 1:
                        if y + 1 == grid.shape[0]:
                            pg.draw.rect(scherm, (82, 82, 82), (
                            (x_grid_scale, round((y * grid_size + grid_size - side_size) * scale)+ scrolly),
                            (round(grid_size * scale), side_scale)))
                        elif not grid[y + 1, x] in conveyor_connect_list:
                            pg.draw.rect(scherm, (82, 82, 82), (
                            (x_grid_scale, round((y * grid_size + grid_size - side_size) * scale)+ scrolly),
                            (round(grid_size * scale), side_scale)))
                    else:
                        pg.draw.rect(scherm, (82, 82, 82), (
                        (x_grid_scale, round((y * grid_size + grid_size - side_size) * scale)+ scrolly),
                        (round(grid_size * scale), side_scale)))

                    if y < grid.shape[1] - 1:
                        if x + 1 == grid.shape[1]:
                            pg.draw.rect(scherm, (82, 82, 82), (
                            (round((x * grid_size + grid_size - side_size) * scale)+ scrollx, y_grid_scale),
                            (side_scale, round(grid_size * scale))))
                        elif not grid[y, x + 1] in conveyor_connect_list:
                            pg.draw.rect(scherm, (82, 82, 82), (
                            (round((x * grid_size + grid_size - side_size) * scale)+ scrollx, y_grid_scale),
                            (side_scale, round(grid_size * scale))))
                    else:
                        pg.draw.rect(scherm, (82, 82, 82), (
                        (round((x * grid_size + grid_size - side_size) * scale)+ scrollx, y_grid_scale),
                        (side_scale, round(grid_size * scale))))
                #elif built == 15: #animated research thing
                    #scherm, drawn_xy = render_building(built,x,y,orientation,drawn_xy,scherm,scale,grid,grid_rotation,grid_cables,blocks_index,scaled_pictures,scrollx,scrolly,move)

                    #scherm.blit(scaled_pictures["picture_15_" + str(int(move[move_dict[built]] + 1))][orientation], (x_grid_scale, y_grid_scale))

                elif built == 25:
                    scherm.blit(scaled_pictures["picture_25"][orientation], (x_grid_scale, y_grid_scale))
                    draw_last_list.append([orientation, (round((x - 1) * grid_size * scale) + scrollx, round((y - 1) * grid_size * scale) + scrolly)])
                    #scherm.blit(scaled_pictures["picture_26"][orientation], )

                else:
                    scherm, drawn_xy, grid_cables = render_building(built,x,y,orientation,drawn_xy,scherm,scale,grid,grid_rotation,grid_cables,blocks_index,scaled_pictures,scrollx,scrolly,move,grid_data)
            #elif built == 20:
                #    if [x, y] not in drawn_xy:
                #        drawn_xy.append([x, y])
                #        scherm.blit(pg.transform.rotate(scaled_pictures["picture_20"], -orientation * 90),
                #                         (x_grid_scale, y_grid_scale))
                #        for item in range(len(storage)):
                #            if storage[item] != 0 and item != 0:
                #                scherm.blit(eval("item_" + str(item) + "_picture"), (
                #                round((x * grid_size * scale + int(item / 7) * grid_size * scale * 3 / 4)),
                #                round((y * grid_size + (item % 7) * (item_size + 5)) * scale)))
                #                scherm.blit(item_font.render(str(storage[item]), (255, 255, 255), True), (
                #                round((x * grid_size + item_size + 2) * scale + int(item / 7) * grid_size * scale * 3 / 4),
                #                round((y * grid_size + (item % 7) * (item_size + 5)) * scale)))
                #
                #elif built == -20:
                #    x_, y_ = outside_screen_render(x, y, grid, grid_rotation, blocks_index, 20)
                #    if [x_, y_] not in drawn_xy:
                #        drawn_xy.append([x_, y_])
                #        scherm.blit(pg.transform.rotate(scaled_pictures["picture_16"], -grid_rotation[y_, x_] * 90),
                #                         (round(x_ * grid_size * scale), round(y_ * grid_size * scale)))
                #        for item in range(len(storage)):
                #            if storage[item] != 0 and item != 0:
                #                scherm.blit(eval("item_" + str(item) + "_picture"), (
                #                round((x_ * grid_size * scale + int(item / 7) * grid_size * scale * 3 / 4)),
                #                round((y_ * grid_size + (item % 7) * (item_size + 5)) * scale)))
                #                scherm.blit(item_font.render(str(storage[item]), (255, 255, 255), True), (
                #                    round((x_ * grid_size + item_size + 2) * scale + int(item / 7) * grid_size * scale * 3 / 4),
                #                    round((y_ * grid_size + (item % 7) * (item_size + 5)) * scale)))
                #
                

                #temp stuff
                if grid_cables[y,x] > 0:
                    if brush in [16,17,18,19]:
                        scherm.blit(scaled_pictures["picture_arrow_cable"][grid_cables[y,x]-1],
                                        (x_grid_scale, y_grid_scale))

        for i in draw_last_list:
        # angle = 45
            rotated_scaled = pg.transform.rotate(scaled_pictures["picture_26"][i[0]], angle)
            new_rect = rotated_scaled.get_rect(center = scaled_pictures["picture_26"][i[0]].get_rect(topleft =  i[1]).center)

            scherm.blit(rotated_scaled, new_rect.topleft)
            #scherm.blit(pg.transform.rotate(scaled_pictures["picture_26"][i[0]], angle), i[1])            
        pg.draw.rect(scherm, (0, 0, 255), (
        (round(selected_x * grid_size * scale) + scrollx, round(selected_y * grid_size * scale) +scrolly),
        (round(grid_size * scale), round(grid_size * scale))), width=2)
        
        if queue is not None: #do multiprocessing
            t_grid_output = queue.get()
            t_grid_output['grid_cables'] = grid_cables
            queue.put()
        else:
            return grid_cables

    def render_building(built,x,y,orientation,drawn_xy,main_scherm,scale,grid,grid_rotation,grid_cables,blocks_index,scaled_pictures,scrollx, scrolly,move,grid_data,grid_size=grid_size,crafter_frames=crafter_frames,research_frames=research_frames,pictjure=pictjure):
        x_grid_scale = round(x * grid_size * scale)+scrollx
        y_grid_scale = round(y * grid_size * scale)+scrolly
        
        if built in [16, 17, 18]:
            if [x, y] not in drawn_xy:
                drawn_xy.append([x, y])
                main_scherm, grid_cables = draw_cables(x,y,main_scherm,built,orientation,grid,grid_rotation, grid_cables, scale, scaled_pictures,scrollx, scrolly)
        elif -built in [16,17,18]:
            x_, y_ = outside_screen_render(x, y, grid, grid_rotation, blocks_index, abs(built))
            if [x_, y_] not in drawn_xy:
                drawn_xy.append([x_, y_])
                main_scherm,grid_cables = draw_cables(x_,y_,main_scherm,abs(built),orientation,grid,grid_rotation, grid_cables, scale, scaled_pictures,scrollx, scrolly)

        elif built == abs(built):#positive render
            #main_scherm.blit(scaled_pictures["picture_15_" + str(int(move[move_dict[built]] + 1))][orientation], (x_grid_scale, y_grid_scale))

            if [x, y] not in drawn_xy:
                drawn_xy.append([x, y])
                if built == 15:
                    if grid_data[y,x][5] == -1:
                        main_scherm.blit(crafter_frames['r'][int(move[0]+1)][0],
                                    (x_grid_scale, y_grid_scale))

                    else:
                        main_scherm.blit(scaled_pictures["picture_15_" + str(int(move[0]+1))][orientation],
                                    (x_grid_scale, y_grid_scale))
                else:
                    main_scherm.blit(scaled_pictures["picture_"+str(abs(built))][orientation],
                                    (x_grid_scale, y_grid_scale))

        else:#negative render
            x_, y_ = outside_screen_render(x, y, grid, grid_rotation, blocks_index, abs(built))
            if [x_, y_] not in drawn_xy:
                drawn_xy.append([x_, y_])
                if built == -15:
                    if grid_data[y,x][5] == -1:
                        main_scherm.blit(crafter_frames['r'][int(move[0]+1)][0],
                                    (round(x_ * grid_size * scale)+scrollx, round(y_ * grid_size * scale)+scrolly))

                    else:
                        main_scherm.blit(scaled_pictures["picture_15_" + str(int(move[0]+1))][orientation],
                                    (round(x_ * grid_size * scale)+scrollx, round(y_ * grid_size * scale)+scrolly))
                else:
                    main_scherm.blit(scaled_pictures["picture_"+str(abs(built))][grid_rotation[y_, x_]],
                                    (round(x_ * grid_size * scale)+scrollx, round(y_ * grid_size * scale)+scrolly))

            
        return main_scherm, drawn_xy, grid_cables

    def draw_cables(x_in, y_in, main_scherm, built, orientation, grid, grid_rotation, grid_cables, scale, scaled_pictures,scrollx, scrolly):
        height_grid, width_grid = grid.shape
        x = x_in
        y = y_in

        x_grid_scale = round(x * grid_size * scale)+scrollx
        y_grid_scale = round(y * grid_size * scale)+scrolly
        
        if built in [16,17]:
            main_scherm.blit(scaled_pictures['picture_'+str(built)][0],(x_grid_scale,y_grid_scale))
            #main_scherm.blit(scaled_pictures['picture_cable_in'][0],(x_grid_scale,y_grid_scale))
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

            if built == 16:
                blit_picture = 'picture_cable_out' #dict key of scaled_pictures
            elif built == 17:
                blit_picture = 'picture_cable_in'

            blit_16 = False #outgoing cable tile can only have 1 output (other can have multiple inputs)
            if blit_up:
                main_scherm.blit(scaled_pictures[blit_picture][0],(x_grid_scale,y_grid_scale))
                if built_16:
                    blit_16 = True
                    grid_cables[y,x+1] = 1
                    grid_cables[y+1,x+1] = 1
                else:
                    grid_cables[y,x+1] = 3
            else:
                grid_cables[y,x+1] = 0

            if blit_down and not blit_16:
                main_scherm.blit(scaled_pictures[blit_picture][2],(x_grid_scale,y_grid_scale))
                if built_16:
                    blit_16 = True
                    grid_cables[y+1,x+1] = 3
                    grid_cables[y+2,x+1] = 3
                else:
                    grid_cables[y+2,x+1] = 1
            else:
                grid_cables[y+2,x+1] = 0

            if blit_left and not blit_16:
                main_scherm.blit(scaled_pictures[blit_picture][3],(x_grid_scale,y_grid_scale))
                if built_16:
                    blit_16 = True
                    grid_cables[y+1,x] = 4
                    grid_cables[y+1,x+1] = 4
                else:
                    grid_cables[y+1,x] = 2
            else:
                grid_cables[y+1,x] = 0

            if blit_right and not blit_16:
                main_scherm.blit(scaled_pictures[blit_picture][1],(x_grid_scale,y_grid_scale))
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
            main_scherm.blit(scaled_pictures["picture_10"][2],
                                            (x_grid_scale, y_grid_scale))
            if orientation in [0,2] and not cable_left and not cable_right:
                main_scherm.blit(scaled_pictures["picture_18"][orientation],(x_grid_scale,y_grid_scale))
            elif orientation in [1,3] and not cable_up and not cable_down:
                main_scherm.blit(scaled_pictures["picture_18"][orientation],(x_grid_scale,y_grid_scale))
            else: #draw shorter cable thingy
                if cable_up:
                    if grid_cables[y-1, x] == 1 or own_rotation == 1:
                        main_scherm.blit(scaled_pictures["picture_9"][0],
                                            (x_grid_scale, y_grid_scale))
                    elif grid_cables[y-1, x] == 3:
                        main_scherm.blit(scaled_pictures["picture_8"][0],
                                            (x_grid_scale, y_grid_scale))

                if cable_down:
                    if grid_cables[y+1,x] == 1:
                        main_scherm.blit(scaled_pictures["picture_8"][2],
                                            (x_grid_scale, y_grid_scale))
                    elif grid_cables[y+1,x] == 3 or own_rotation == 3:
                        main_scherm.blit(scaled_pictures["picture_9"][2],
                                            (x_grid_scale, y_grid_scale))
    
                if cable_right:
                    if grid_cables[y,x+1] == 2 or own_rotation == 2:
                        main_scherm.blit(scaled_pictures["picture_9"][1],
                                            (x_grid_scale, y_grid_scale))
                    elif grid_cables[y,x+1] == 4:
                        main_scherm.blit(scaled_pictures["picture_8"][1],
                                            (x_grid_scale, y_grid_scale))

                if cable_left:
                    if grid_cables[y,x-1] == 2:
                        main_scherm.blit(scaled_pictures["picture_8"][3],
                                            (x_grid_scale, y_grid_scale))
                    elif grid_cables[y,x-1] == 4 or own_rotation == 4:
                        main_scherm.blit(scaled_pictures["picture_9"][3],
                                            (x_grid_scale, y_grid_scale))

        return main_scherm, grid_cables
        

    def outside_screen_render(x, y, grid, grid_rotation, blocks_index, blocks_type):
        if x > blocks_index[blocks_type][0] and y > blocks_index[blocks_type][0]:
            cut = grid[y - blocks_index[blocks_type][0] + 1:y + 1, x - blocks_index[blocks_type][0] + 1:x + 1]
            dx = x - blocks_index[blocks_type][0] + 1
            dy = y - blocks_index[blocks_type][0] + 1
        elif x >= blocks_index[blocks_type][0] and y >= blocks_index[blocks_type][0]:
            cut = grid[y - blocks_index[blocks_type][0] + 1:y + 1, x - blocks_index[blocks_type][0] + 1:x + 1]
            dx = x - blocks_index[blocks_type][0] + 1
            dy = y - blocks_index[blocks_type][0] + 1
        else:  # on edge of grid
            if not x >= blocks_index[blocks_type][0] and (y >= blocks_index[blocks_type][0]):
                cut = grid[y - blocks_index[blocks_type][0] + 1:y + 1, 0:x + 1]
                dx = 0
                dy = y - blocks_index[blocks_type][0] + 1
            elif (x >= blocks_index[blocks_type][0]) and not y >= blocks_index[blocks_type][0]:
                cut = grid[0:y + 1, x - blocks_index[blocks_type][0] + 1:x + 1]
                dx = x - blocks_index[blocks_type][0] + 1
                dy = 0
            else:  # cornered
                cut = grid[0:y + 1, 0:x + 1]
                dx = 0
                dy = 0

        # print(cut)
        # print(x,y)
        linksboven = np.where(cut == blocks_type)
        # import pdb; pdb.set_trace()
        x_ = dx + linksboven[1][0]
        y_ = dy + linksboven[0][0]
        #x_ += scrollx
        #y_ += scrolly
        return x_, y_


    def bereken_muis_pos(mx, my, scrollx, scrolly, scale, grid_size=grid_size):
        mrx = round((mx - scrollx - grid_size / 2) / scale / grid_size)
        mry = round((my - scrolly - grid_size / 2) / scale / grid_size)

        #mrx = round((mx - scrollx - grid_size/scale) / 2 / grid_size)
        #mry = round((my - scrolly - grid_size/scale) / 2 / grid_size)
        return mrx, mry


    def draw_preview_box(scherm, selecting_tile, mrx, mry, mrr, brush, scrollx, scrolly, scale, scaled_pictures, size,
                        grid_size=grid_size):
        if not brush in [10, 11]:
            if not selecting_tile:
                scherm.blit(scaled_pictures["picture_" + str(brush)][mrr],
                            (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
                if brush == 1:
                    scherm.blit(scaled_pictures["picture_arrow"][mrr],
                                (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
                elif brush == 2:
                    scherm.blit(scaled_pictures["picture_arrow_cross"][mrr],
                                (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
                elif brush == 3:
                    scherm.blit(scaled_pictures["picture_arrow_split_r"][mrr],
                                (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
                elif brush == 4:
                    scherm.blit(scaled_pictures["picture_arrow_split_l"][mrr],
                                (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
                elif brush == 5:
                    scherm.blit(scaled_pictures["picture_arrow_sort_r"][mrr],
                                (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
                elif brush == 6:
                    scherm.blit(scaled_pictures["picture_arrow_sort_l"][mrr],
                                (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
                elif brush == 7:
                    scherm.blit(scaled_pictures["picture_arrow_highway"][mrr],
                                (mrx * grid_size * scale + scrollx, mry * grid_size * scale + scrolly))
            else:
                size = 1
            pg.draw.rect(scherm, (0, 0, 255), (
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
            free=False, spawn=False,crafter=0):
        if draw_brush is None:
            draw_brush = brush
        free = True
        if check_build_prices(b_prices, brush, storage, item_names) or free:
            grid[ry, rx] = draw_brush
            grid_rotation[ry, rx] = rr
            if not spawn:
                grid_data[ry, rx] = [-1, -1, 0, 2, 0,crafter]
            else:
                grid_data[ry, rx] = [brush, t.perf_counter(), 0, 2, 0, crafter]
            if not free:
                for item in b_prices[brush].keys():
                    storage[item_names[0].index(item)] -= b_prices[brush][item]
        else:
            print("not enough resources!")
        return grid, grid_rotation, grid_data, storage


    def add_to_grid(rx, ry, rr, grid, grid_rotation, grid_data, brush, size, blocks_index, storage, item_names, b_prices,grid_cables,
                    extra_conveyor_list=extra_conveyor_list):
        empty_grid_data_list = [-1, -1, 0, 2, 0, 0]
        cable_delete = False #default value
        grid_h, grid_w = grid.shape
        grid_h -= 1
        grid_w -= 1
        if brush != 0 and not (grid[ry, rx] == brush and grid_rotation[ry, rx] == rr):
            if size == 1:  # brush = [1 2 3 4 5 6 7]
                if brush in [1, 2, 3, 4, 5, 6, 7]:
                    check_list = [10, 11, 21, 22, 1, 2, 3, 4, 5, 6, 7]
                else:
                    check_list = [10, 11, 21, 22, brush]
                if grid[ry, rx] not in check_list:
                    print("Cannot build!")
                elif not (grid[ry, rx] in [10, 11, 21, 22] and grid[ry, rx] == brush):
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
                build_spot = True
                for x in range(rx, rx + size):
                    for y in range(ry, ry + size):
                        if not grid[y, x] in [10, 11, 21, 22]:
                            build_spot = False

                #if brush in [18,19] and grid[ry,rx] in [18,19]:
                #    build_spot = True

                if build_spot:
                    if check_build_prices(b_prices, brush, storage, item_names) or True:
                        free_build = False
                        '''
                        if brush == 19: #cargo cable
                            cable_delete = True
                            cur_grid = grid[ry,rx]
                            make_pole = False#make pole on facing location
                            r_addx = 0
                            r_addy = 0
                            if rr == 0:
                                r_addy = 3
                            elif rr == 1:
                                r_addx = -3
                            elif rr == 2:
                                r_addy = -3
                            elif rr == 3:
                                r_addx = 3

                            if grid[ry+r_addy,rx+r_addx] == 19 and rr != grid_rotation[ry+r_addy,rx+r_addx]:#dir going into is 19
                                make_pole = True

                            elif grid[ry-r_addy,rx-r_addx] == 19 and rr != grid_rotation[ry-r_addy,rx-r_addx]:
                                r_addx = -r_addx#place behind
                                r_addy = -r_addy
                                make_pole = True
            
                            if make_pole:
                                rr = 0#rotation doesnt matter when placed
                                rx += r_addx
                                ry += r_addy
                                free_build = True
                                brush = 18

                            else:#no pole placed: update grid_cables
                                if rr == 0:
                                    for c in range(0,6):
                                        grid_cables[ry+c-1,rx+1] = rr + 1
                                if rr == 1:
                                    for c in range(0,6):
                                        grid_cables[ry+1,rx+c-2] = rr + 1
                                if rr == 2:
                                    for c in range(0,6):
                                        grid_cables[ry+c-2,rx+1] = rr + 1
                                if rr == 3:
                                    for c in range(0,6):
                                        grid_cables[ry+1,rx+c-1] = rr + 1
                        '''
                        for x in range(rx, rx + size):
                            for y in range(ry, ry + size):
                                grid, grid_rotation, grid_data, storage = build(x, y, rr, grid, grid_rotation, grid_data,
                                                                                brush, size,
                                                                                b_prices, storage, item_names,
                                                                                draw_brush=-brush, free=True)
                                
                        grid, grid_rotation, grid_data, storage = build(rx, ry, rr, grid, grid_rotation, grid_data, brush,
                                                                        size,
                                                                        b_prices, storage, item_names, draw_brush=brush, free=free_build)

                        if brush == 16: #spawn cargo items
                            grid_data[ry, rx] = [brush, t.perf_counter(), 0, 2, 0, 0]

                        if brush == 15:
                            grid_data[ry, rx][5] = -1
                            print(ry,rx)
                            
                        if brush in extra_conveyor_list:  # extra conveyor
                            if rr == 0:
                                grid, grid_rotation, grid_data, storage = build(rx + int(0.5 * size - 0.5),
                                                                                ry + int(size - 1), 2, grid, grid_rotation,
                                                                                grid_data, brush,
                                                                                size, b_prices, storage, item_names,
                                                                                draw_brush=1, free=True, spawn=True)
                            elif rr == 1:
                                grid, grid_rotation, grid_data, storage = build(rx, ry + int(0.5 * size - 0.5), 3,
                                                                                grid, grid_rotation, grid_data, brush,
                                                                                size, b_prices, storage, item_names,
                                                                                draw_brush=1,
                                                                                free=True, spawn=True)

                            elif rr == 2:
                                grid, grid_rotation, grid_data, storage = build(rx + int(0.5 * size - 0.5), ry, 0,
                                                                                grid, grid_rotation, grid_data, brush,
                                                                                size, b_prices, storage, item_names,
                                                                                draw_brush=1,
                                                                                free=True, spawn=True)
                            elif rr == 3:
                                grid, grid_rotation, grid_data, storage = build(rx + int(size - 1),
                                                                                ry + int(0.5 * size - 0.5), 1,
                                                                                grid, grid_rotation, grid_data, brush,
                                                                                size, b_prices, storage, item_names,
                                                                                draw_brush=1,
                                                                                free=True, spawn=True)
                    else:
                        print("not enough resources!")

        elif brush == 0:
            if not grid[ry, rx] in [10, 11, 21, 22]:
                cable_delete = False
                
                if abs(grid[ry,rx]) in [16, 17, 18, 19]:
                    cable_delete = True
                    
                if grid[ry, rx] in [12, 13, 14, 15, 16, 17, 18, 19, 20, 33, 34, 35]:
                    if abs(grid[ry,rx]) == 18 and grid_cables[ry,rx] > 0:
                        grid_cables[ry,rx] = 0
                    else:
                        index = grid[ry, rx]
                        for y_ in range(blocks_index[index][0]):
                            for x_ in range(blocks_index[index][0]):
                                grid[ry + y_, rx + x_] = r.randint(10, 11)
                                grid_rotation[ry + y_, rx + x_] = r.randint(0, 3)
                                grid_data[ry + y_, rx + x_] = empty_grid_data_list

                elif -grid[ry, rx] in [12, 13, 14, 15, 16, 17, 18, 19, 20, 33, 34, 35]:
                    if abs(grid[ry,rx]) == 18 and grid_cables[ry,rx] > 0:
                        grid_cables[ry,rx] = empty_grid_data_list
                    else:
                        index = -1 * grid[ry, rx]
                        xlinksboven, ylinksboven = outside_screen_render(rx, ry, grid, grid_rotation, blocks_index,
                                                                        -1 * grid[ry, rx])
                        for y_ in range(ylinksboven, ylinksboven + blocks_index[index][0]):
                            for x_ in range(xlinksboven, xlinksboven + blocks_index[index][0]):
                                grid[y_, x_] = r.randint(10, 11)
                                grid_rotation[y_, x_] = r.randint(0, 3)
                                grid_data[y_, x_] = empty_grid_data_list

                else:
                    grid[ry, rx] = r.randint(10, 11)
                    grid_rotation[ry, rx] = r.randint(0, 3)
                    grid_data[ry, rx] = empty_grid_data_list

        if cable_delete:
                    #for i in range(len(cable_index[0])):
                    #    if not (abs(grid[cable_index[0][i],cable_index[1][i]]) in [16, 17, 18, 19]):
                    #        grid_cables[cable_index[0][i],cable_index[1][i]] = 0
                    
            cable_locations = np.where(grid_cables > 0) #delete 'floating' cables

            for x in cable_locations[1]:
                for y in cable_locations[0]:
                    if not abs(grid[y,x]) in [16,17,18,19]: # not on cable blocks
                        grid_cables[y,x] = 0


                            

        return grid, grid_rotation, grid_data, storage

    def update_locations(grid_data,grid):
        locations = np.array([])
        loc_grid = grid
        loc12 = np.where(loc_grid == 12, 13, loc_grid)  # transform all 13 into 14
        loc13 = np.where(loc12 == 13, 14, loc_grid)  # transform all 14 (and 13) into 15
        loc14 = np.where(loc13 == 14, 16, loc_grid)
        loc16 = np.where(loc14 == 16, 33, loc_grid)
        loc33 = np.where(loc16 == 33, 34, loc_grid)
        loc34 = np.where(loc33 == 34, 35, loc_grid)
        locations = np.where(loc34 == 35)

        crafting_locations = np.where(grid == 15)

        cargo_locations = np.where(grid == 17)
        return locations,crafting_locations,cargo_locations


        

    def spawn_items(grid, grid_data, items_list, item_perf_time, craft_data, item_spawn_dict, cargo_spawn_list, grid_size=grid_size):
        # grid data: type, perf_counter
        for x in item_spawn_dict.keys():
            if item_perf_time[x] + int(x) < t.perf_counter(): #if True, spawn extend list with items
                if item_spawn_dict[x] is not None:
                    
                    for item in item_spawn_dict[x]:
                        #print(item)
                        items_list.append(
                            Item(item[0] * grid_size + int(grid_size / 2), item[1] * grid_size + int(grid_size / 2), r.randint(item[2],item[3])))
                        
                    item_perf_time[x] = t.perf_counter()
                    #print(f"spawned items {x}")

        if item_perf_time['cargo'] + 10 < t.perf_counter() and cargo_spawn_list != []:
            item_perf_time['cargo'] = t.perf_counter()
            for cargo in cargo_spawn_list:
                items_dict = {}#dict for items inside of cargo item
                items_dict = craft_data[cargo[1], cargo[0]]
                #print(craft_data[cargo[1], cargo[0]],str([cargo[1], cargo[0]]))
                craft_data[cargo[1], cargo[0]] = {}
                
                items_list.append(
                    Cargo((cargo[0]+1) * grid_size + int(grid_size / 2), (cargo[1]+1) * grid_size + int(grid_size / 2), items_dict))
        
        return craft_data,items_list
                
    def update_item_spawn(grid,grid_rotation,item_spawn_dict,item_spawn_time,item_perf_time,locations,craft_data,cargo_spawn_list):
        item_spawn_dict = {1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
        #item_spawn_dict = {1:[[x,y,start randint, end randint],[x,y,start ...]],2:[],...}
        randint_range_dict = {12:[1,3],13:[4,6],14:[7,9],33:[10,12],34:[13,15],35:[16,21]}
        #print(locations)
        #print(item_spawn_dict[item_spawn_time[str(block)]])
        cargo_spawn_list = []
        for index in range(len(locations[0])):
            x = locations[1][index]
            y = locations[0][index]
        #for x in locations[1]:
            #for y in locations[0]:
                #print(f'GRID XY {grid[y,x]}')
            if grid[y,x] in list(randint_range_dict.keys()) and grid[y,x] != 16:
                block = grid[y,x] 
                add = []
                if grid_rotation[y,x] == 0:
                    add = [x+1,y+2]
                elif grid_rotation[y,x] == 1:
                    add = [x,y+1]
                elif grid_rotation[y,x] == 2:
                    add = [x+1,y]
                elif grid_rotation[y,x] == 3:
                    add = [x+2,y+1]

                    #print(f"block{block,add,block}")
                add.extend(randint_range_dict[block])
                item_spawn_dict[item_spawn_time[str(block)]].append(add)
                

            elif grid[y,x] == 16:#cargo
                        
                cargo_spawn_list.append([x,y])

                        #items_list.append(
                        #    Cargo((x+1) * grid_size + int(grid_size / 2), (y+1) * grid_size + int(grid_size / 2), items_dict))

        #print(item_spawn_dict,randint_range_dict.keys())
        return craft_data, item_spawn_dict, item_perf_time,cargo_spawn_list


    def research_items(crafting_locations, grid, grid_rotation, craft_data, items_list, grid_size=grid_size):
        locations = crafting_locations
        for ind in range(len(locations[1])):
            x = locations[1][ind]
            y = locations[0][ind]
            if True:
            #for y in locations[0]:
                if '1' in list(craft_data[y, x].keys()) and '2' in list(craft_data[y, x].keys()) and '3' in list(craft_data[y, x].keys()):
                    if craft_data[y, x]["1"] > 0 and craft_data[y, x]["2"] > 0 and craft_data[y, x]["3"] > 0:
                        # subtract data from craft_data
                        craft_data[y, x]["1"] -= 1
                        craft_data[y, x]["2"] -= 1
                        craft_data[y, x]["3"] -= 1

                        # spawn research item
                        spawnx = -1
                        spawny = -1
                        if grid_rotation[y, x] == 0:
                            spawnx = (x + int(0.5 * 3 - 0.5)) * grid_size + int(grid_size / 2)
                            spawny = (y + 3) * grid_size + int(grid_size / 10)
                        elif grid_rotation[y, x] == 1:
                            spawnx = x * grid_size - int(grid_size / 10)
                            spawny = (y + int(0.5 * 3 - 0.5)) * grid_size + int(grid_size / 2)
                        elif grid_rotation[y, x] == 2:
                            spawnx = (x + int(0.5 * 3 - 0.5)) * grid_size + int(grid_size / 2)
                            spawny = y * grid_size - int(grid_size / 10)
                        elif grid_rotation[y, x] == 3:
                            spawnx = (x + 3) * grid_size + int(grid_size / 10)
                            spawny = (y + int(0.5 * 3 - 0.5)) * grid_size + int(grid_size / 2)
                        items_list.append(Item(int(spawnx), int(spawny), 0))

        return craft_data, items_list


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
                        grid_data[ry, rx][2] = (grid_data[ry, rx][2] + 1) % grid_data[ry, rx][3]

                        if grid_data[ry, rx][2] == grid_data[ry, rx][3] - 1:  # to side
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
                    if grid_data[ry, rx][4] == self.item_type:  # go left/right (wanted item)
                        if volgend_blokje == 5:
                            orientatie_blokje += self.split_side
                        elif volgend_blokje == 6:
                            orientatie_blokje -= self.split_side
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
                        #print(max(0,ry - 2) + r_corner[0][0],max(0,rx - 2) + r_corner[1][0],craft_data[max(0,ry - 2) + r_corner[0][0]][max(0,rx - 2) + r_corner[1][0]])
                        #print(80,30,craft_data[80,30])
                    else:
                        storage[self.item_type] -= 1
                    self.vx = self.vy = 0
                    self.kapot = True

            return storage, craft_data, grid_data, cargo_data

        def teken(self, scherm, scale, scaled_pictures, scrollx, scrolly):
            item_margin = 10
            tekenx = int((self.x - int(self.breedte / 2)) * scale + scrollx)
            tekeny = int((self.y - int(self.lengte / 2)) * scale + scrolly)
            screen_x, screen_y = scherm.get_size()
            if not (tekenx + item_size + item_margin < 0 or tekeny + item_size + item_margin < 0) and not (
                    tekenx + item_size + item_margin > screen_x or tekeny + item_size + item_margin > screen_y):
                scherm.blit(scaled_pictures["item_" + str(self.item_type) + "_picture"][0], (
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
                

    def spawn_cargo(cargo_locations,grid,cargo_data,items_list, spawn_cooldown, grid_size=grid_size):
        loc_17 = cargo_locations
        set_spawn_cooldown = False
        for ind in range(len(loc_17[0])):
            x = loc_17[1][ind]
            y = loc_17[0][ind]
        #for x in loc_17[1]:
        #   for y in loc_17[0]:
            if True:
                if len(cargo_data[y, x]) > 0: # items to spawn
                    spawn_spots = [] #places to spawn
                    if grid[y-1,x+1] == 1:
                        spawn_spots.append([max(0,y-1),x+1])
                    if grid[y+1,x+3] == 1:
                        spawn_spots.append([y+1,x+3])
                    if grid[y+3,x+1] == 1:
                        spawn_spots.append([y+3,x+1])
                    if grid[y+1,x-1] == 1:
                        spawn_spots.append([y+1,max(0,x-1)])
                        
                    if len(spawn_spots) > 0: # no spawn spots, not spawning!
                        if (sum(cargo_data[y, x].values()) > 25) or (spawn_cooldown < t.perf_counter() - 0.5): #if a lot of items
                            set_spawn_cooldown = True
                            spawn_y, spawn_x = r.choice(spawn_spots)
                            dict_keys = list(cargo_data[y, x].keys())
                            spawn_type = r.choice(dict_keys)
                            spawn_type = int(spawn_type)
                            items_list.append(
                                Item(spawn_x * grid_size + int(grid_size / 2), spawn_y * grid_size + int(grid_size / 2), spawn_type))

                            spawn_type = str(spawn_type)
                            
                            if cargo_data[y, x][spawn_type] > 0:
                                cargo_data[y, x][spawn_type] -= 1
                            else:
                                del cargo_data[y,x][spawn_type]
                    else:
                        print("No spawn spots!")
        
        if set_spawn_cooldown:
            spawn_cooldown = t.perf_counter()

        return items_list, cargo_data, spawn_cooldown

    def draw_tile_menu(scherm, data_display, data_arrow, item_names, tile_names, tile_des, rect_info, grid, mrx, mry,
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
        width, height = scherm.get_size()
        scherm.blit(rect_info, (-2, height - rect_h))
        # i_title_font,i_text_font,i_des_font

        arrow_width = data_arrow.get_size()[0]
        arrow_height = data_arrow.get_size()[1]
        up_button = pg.Rect((150, height - rect_h + 133), (arrow_width, arrow_height))  # data editing x and y
        down_button = pg.Rect((151, height - rect_h + 170), (arrow_width, arrow_height))

        # title
        text = i_title_font.render("Edit Tile Data:", True, (0, 0, 0))
        scherm.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 33))
        tile_block = grid[mry, mrx]

        if tile_block in [3, 4, 5, 6]:  # splitters & sorters
            # text for splitters/sorters
            if tile_block in [3, 4]:
                tile_mode = "splitter"
                text1 = i_text_font.render("Edit tile data for splitter:", True, (0, 0, 0))
                text2 = i_des_font.render("Splits item for every " + str(grid_data[mry, mrx][3] - 1) + " item(s):", True,
                                        (0, 0, 0))
                text3 = i_title_font.render(str(grid_data[mry, mrx][3] - 1), True, (0, 0, 0))
            else:
                tile_mode = "sorter"
                text1 = i_text_font.render("Edit tile data for sorter:", True, (0, 0, 0))
                text2 = i_des_font.render("Sorts " + str(item_names[1][grid_data[mry, mrx][4]]) + ".", True, (0, 0, 0))
                text3 = None

            scherm.blit(text1, (int((rect_w - text1.get_size()[0]) / 2), height - rect_h + 65))
            scherm.blit(text2, (int((rect_w - text2.get_size()[0]) / 2), height - rect_h + 95))

            # display bit
            scherm.blit(data_display, (60, height - rect_h + 140))
            scherm.blit(data_arrow, (150, height - rect_h + 133))
            scherm.blit(pg.transform.rotate(data_arrow, 180), (151, height - rect_h + 170))

            if tile_block in [3, 4]:  # number for splitter
                scherm.blit(text3, (int((rect_w - text3.get_size()[0]) / 2) - 42, height - rect_h + 155))
            elif tile_block in [5, 6]:  # item for sorter
                if grid_data[mry, mrx][4] != 0:  # not research item
                    scherm.blit(pg.transform.scale(eval("item_" + str(grid_data[mry, mrx][4]) + "_picture"), (45, 45)),
                                (80, height - rect_h + 145))
                else:
                    scherm.blit(pg.transform.scale(r_icon_picture, (43, 43)), (80, height - rect_h + 146))
            # x,y
            text = i_des_font.render("Tile at x: " + str(mrx) + ", y: " + str(mry), True, (0, 0, 0))
            scherm.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 215))
            # type
            text = i_des_font.render("Item type: " + str(tile_names[abs(tile_block)]), True, (0, 0, 0))
            scherm.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 245))
            # descrition
            blit_text(scherm, rect_info, str(tile_des[abs(tile_block)]), (25, height - rect_h + 275), i_des_font)

        else:  # no info to edit, show defeault info
            tile_mode = ""  # no tile mode
            text = i_text_font.render("No information to edit.", True, (0, 0, 0))
            scherm.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 65))
            # x,y
            text = i_des_font.render("Tile at x: " + str(mrx) + ", y: " + str(mry), True, (0, 0, 0))
            scherm.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 95))
            # type
            text = i_des_font.render("Item type: " + str(tile_names[abs(tile_block)]), True, (0, 0, 0))
            scherm.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 125))
            # descrition
            blit_text(scherm, rect_info, str(tile_des[abs(tile_block)]), (25, height - rect_h + 155), i_des_font)

        return tile_mode, up_button, down_button  # buttons = pg.Rect of buttons (collidepoint)


    def draw_keybind_menu(scherm, k_scrolly, unlocked_blocks, data_display, data_arrow, rect_keybinds, keybinds):
        rect_w, rect_h = rect_keybinds.get_size()
        rect_w -= 10
        width, height = scherm.get_size()
        scherm.blit(rect_keybinds, (-2, height - rect_h + k_scrolly))
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
        scherm.blit(text, (int((rect_w - text.get_size()[0]) / 2), height - rect_h + 33 + k_scrolly))

        # list of keys with numbers and stuff
        key_distance = 73
        up_button = {}
        down_button = {}
        for k_index, k_item in enumerate(keybinds):
            # display bit
            scherm.blit(data_display, (90, height - rect_h + 70 + k_index * key_distance + k_scrolly))

            # pint("picture_"+str(keybinds[k_index]))
            scherm.blit(pg.transform.smoothscale(eval("picture_" + str(keybinds[k_index])), (50, 50)),
                        (107, height - rect_h + 73 + k_index * key_distance + k_scrolly))
            if str(keybinds[k_index]) in list(conveyor_arrow_dict.keys()):
                scherm.blit(pg.transform.scale(eval(conveyor_arrow_dict[str(keybinds[k_index])]), (50, 50)),
                            (107, height - rect_h + 73 + k_index * key_distance + k_scrolly))

            scherm.blit(data_arrow, (180, height - rect_h + 63 + k_index * key_distance + k_scrolly))
            scherm.blit(pg.transform.rotate(data_arrow, 180),
                        (181, height - rect_h + 100 + k_index * key_distance + k_scrolly))
            up_button[k_index] = pg.Rect((180, height - rect_h + 63 + k_index * key_distance + k_scrolly),
                                        (arrow_width, arrow_height))  # keybind editing x and y
            down_button[k_index] = pg.Rect((181, height - rect_h + 100 + k_index * key_distance + k_scrolly),
                                        (arrow_width, arrow_height))

            text = i_title_font.render(str(k_index) + ":", True, (0, 0, 0))
            scherm.blit(text, (55, height - rect_h + 90 + k_index * key_distance + k_scrolly))

        return up_button, down_button  # buttons = list of pg.Rect buttons (collidepoint)

    def draw_info_popup(scherm,mx,my,menu_pictures,clicked_icon,clicked_button,tile_names,b_prices,info_ui,item_names,tile_des):
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
        scr_w, scr_h = scherm.get_size()
        if mx + w > scr_w:
            blit_x = mx - w
        else:
            blit_x = mx
        blit_y =  my - h
        scherm.blit(info_ui,(blit_x,blit_y))
        tile_hover = tile_names[menu_pictures[clicked_icon][clicked_button]]
        
        #draw title
        scherm.blit(i_title_font.render(str(tile_hover),True,(0,0,0)),(blit_x + 15, blit_y + 5))

        #draw building price
        b_price_list = b_prices[menu_pictures[clicked_icon][clicked_button]]
        x_start = 15
        b_price_blit_y = blit_y + i_title_font.size("Test")[1] + 10
        for b_material in b_price_list.keys():
            item_type = item_names[0].index(b_material) # in numbers
            item_quantity = b_price_list[b_material]
            item_pic = eval("item_"+str(item_type)+"_picture")
            item_pic_size = item_pic.get_width() #width and height are the same
            scherm.blit(item_pic,(blit_x+x_start,b_price_blit_y))
            x_start += item_pic_size + 5
            scherm.blit(i_des_font.render(str(item_quantity),True,(0,0,0)),(blit_x+x_start,b_price_blit_y))
            width_text, height_text = i_des_font.size(str(item_quantity))
            x_start += width_text + 10
        
        #draw description
        #print(pg.Rect(blit_x,blit_y,w,h),(blit_x + 10, b_price_blit_y + height_text + 10),blit_y)
        blit_text(scherm,blit_x + w,tile_des[menu_pictures[clicked_icon][clicked_button]],(blit_x + 10, b_price_blit_y + height_text + 10),i_text_font,(0,0,0))
        




    def teken_menu(scherm, conveyor_research_progress_dict, research_progress, menu_pictures, open_menu, clicked_icon,
                clicked_button, menu_scrollx, scaled_pictures, b_prices):
        # bar
        width, height = scherm.get_size()
        if open_menu:
            ratio_menu = 1 / 6
            bar_height = int(height * ratio_menu)
            bar_width = width
            scherm.blit(pg.transform.scale(menu_bar_picture, (bar_width, bar_height)), (0, height - bar_height))
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
                    scherm.blit(pg.transform.scale(button_clicked_picture,
                                                (int(bar_height - button_margin), int(bar_height - button_margin))), (
                                button_distance * button + int(button_margin / 2) - menu_scrollx,
                                height - bar_height + int(button_margin / 2)))
                else:
                    scherm.blit(pg.transform.scale(button_unclicked_picture,
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

                scherm.blit(pg.transform.scale(scaled_pictures[scaled_picture][0], (
                    int(bar_height - button_margin - picture_margin), int(bar_height - button_margin - picture_margin))), (
                                button_distance * button + int(button_margin / 2) - menu_scrollx + int(picture_margin / 2),
                                height - bar_height + int(button_margin / 2) + int(picture_margin / 2)))
                if clicked_icon == 0:
                    if scaled_picture in conveyor_arrow_dict:
                        scherm.blit(pg.transform.scale(scaled_pictures[conveyor_arrow_dict[scaled_picture]][0], (
                        int(bar_height - button_margin - picture_margin), int(bar_height - button_margin - picture_margin))), (
                                    button_distance * button + int(button_margin / 2) - menu_scrollx + int(picture_margin / 2),
                                    height - bar_height + int(button_margin / 2) + int(picture_margin / 2)))

                    if research_progress[clicked_icon][conveyor_research_progress_dict[index_for_research_progress_dict[index]]] < 0:
                        scherm.blit(pg.transform.scale(lock_picture, (
                        int(bar_height - button_margin - picture_margin), int(bar_height - button_margin - picture_margin))), (
                                    button_distance * button + int(button_margin / 2) - menu_scrollx + int(picture_margin / 2),
                                    height - bar_height + int(button_margin / 2) + int(picture_margin / 2)))

                button += 1

        # tab buttons
        buttons = 6  # button count
        button_distance = 75
        icon_click_list = []  # pos icons
        for icon in range(buttons):
            icon_click_list.append([(icon * button_distance) + int((bar_width - (buttons * button_distance)) / 2),
                                    height - bar_height - button_distance])
            if clicked_icon == icon:
                scherm.blit(icon_clicked_picture, (
                (icon * button_distance) + int((bar_width - (buttons * button_distance)) / 2),
                height - bar_height - button_distance))
            else:
                scherm.blit(icon_unclicked_picture, (
                (icon * button_distance) + int((bar_width - (buttons * button_distance)) / 2),
                height - bar_height - button_distance))
            if icon in [0, 1, 2, 3, 4, 5]:
                scherm.blit(eval("icon_" + str(icon + 1)), (
                (icon * button_distance) + int((bar_width - (buttons * button_distance)) / 2),
                height - bar_height - button_distance))
        return icon_click_list, bar_width, bar_height, button_distance, button_click_list, button_width


    def render_images(scherm, new, not_enough_picture=not_enough_picture, rect_keybinds=rect_keybinds, data_display=data_display, data_arrow=data_arrow, rect_info=rect_info, rect_ui=rect_ui, research_button_clicked=research_button_clicked, research_button_unclicked=research_button_unclicked, research_display=research_display,info_ui=info_ui):
        width, height = scherm.get_size()
        rect_info = pg.transform.scale(rect_info, (300, 400))
        rect_info.set_alpha(235)
        rect_keybinds = pg.transform.scale(rect_keybinds, (300, 800))
        rect_keybinds.set_alpha(235)
        rect_ui = pg.transform.scale(rect_ui, (width, height))
        rect_ui.set_alpha(115)  # make slightly transparent
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


    def draw_research(scherm, r_points, r_scherm, rect_ui, r_scrollx, r_scrolly, research_display, research_button_clicked,
                    research_button_unclicked, research_progress, research_text, r_tile_text, research_subtext, r_prices):
        width, height = scherm.get_size()
        scherm.blit(rect_ui, (0, 0))  # background
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
                        pg.draw.line(r_scherm, (40, 140, 144),
                                    (int(button_size_x / 2) - r_scrollx, row * button_dist_y + button_size_y - r_scrolly),
                                    (int(button_size_x / 2) - r_scrollx, row * button_dist_y + button_dist_y - r_scrolly),
                                    width=5)
                    for button in range(research_progress[category][row] + 2):
                        if not button == research_progress[category][row] + 1:  # not last item, draw line
                            if not button == 5:  # not last item, max research
                                pg.draw.line(r_scherm, (40, 140, 144), (
                                button * button_dist_x + button_size_x - 5 - r_scrollx,
                                row * button_dist_y + int(button_size_y / 2) - r_scrolly), (
                                            button * button_dist_x + button_dist_x + 5 - r_scrollx,
                                            row * button_dist_y + int(button_size_y / 2) - r_scrolly), width=5)
                            r_scherm.blit(research_button_clicked,
                                        (button * button_dist_x - r_scrollx, row * button_dist_y - r_scrolly))
                        else:  # last item, unclicked
                            if not button > 5:  # not max research item
                                r_scherm.blit(research_button_unclicked,
                                            (button * button_dist_x - r_scrollx, row * button_dist_y - r_scrolly))
                        if not button > 5:  # text and icon thingies
                            r_scherm.blit(r_title_font.render(str(research_text[0][button]), True, (0, 0, 0)),
                                        (button * button_dist_x + 10 - r_scrollx, row * button_dist_y + 8 - r_scrolly))
                            r_scherm.blit(r_subtitle_font.render(str(r_tile_text[0][row]), True, (0, 0, 0)),
                                        (button * button_dist_x + 10 - r_scrollx, row * button_dist_y + 29 - r_scrolly))
                            r_scherm.blit(r_font.render(str(research_subtext[0][button]), True, (0, 0, 0)),
                                        (button * button_dist_x + 10 - r_scrollx, row * button_dist_y + 50 - r_scrolly))
                            r_scherm.blit(r_icon_picture, (
                            button * button_dist_x + button_size_x - 105 - r_scrollx, row * button_dist_y + 3 - r_scrolly))
                            r_scherm.blit(r_font.render(str(r_prices[row][button]), True, (0, 0, 0)), (
                            button * button_dist_x + button_size_x - 75 - r_scrollx, row * button_dist_y + 9 - r_scrolly))

        # research points count in left-bottom corner
        r_scherm.blit(research_display, (0, height - 53))
        r_scherm.blit(r_display_picture, (5, height - 45))
        r_scherm.blit(r_display_font.render(str(r_points), True, (0, 0, 0)), (50, height - 41))

        # cross icon in right-top corner
        cross_margin = 10
        r_scherm.blit(icon_unclicked_picture, (width - 50 - cross_margin, cross_margin))
        r_scherm.blit(icon_cross, (width - 50 - cross_margin, cross_margin))

        # scrollbar?
        if (max(research_progress[0]) + 2) * button_dist_x - button_space_x >= width:
            pass  # scrollbar x!
        for y in range(len(research_progress[category])):
            if research_progress[category][max(y - 1, 0)] < 0:
                pass
                # pint(y)
        if (max(research_progress[0]) + 2) * button_dist_x - button_space_x >= width:
            pass  # scrollbar x!

        return r_scherm, [width - 50 - cross_margin, cross_margin]


    def research_mouse_check(shortage_timer, shortage_item, r_points, r_prices, r_scrollx, r_scrolly, mx, my,
                            research_progress, research_scrollx, research_scrolly, research_button_clicked):
        button_space_x = 50
        button_space_y = 25
        button_size_x, button_size_y = research_button_clicked.get_size()
        button_dist_x = button_space_x + button_size_x
        button_dist_y = button_space_y + button_size_y
        clicked_button = -1
        clicked_row = -1
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

                                        else:  # not enough research points
                                            shortage_timer = t.perf_counter()
                                            shortage_item = 0

        return shortage_timer, shortage_item, r_points, clicked_row, clicked_button


    def draw_shortage_notification(scherm, not_enough_picture, shortage_item):
        width, height = scherm.get_size()
        width_rect, height_rect = not_enough_picture.get_size()
        scherm.blit(not_enough_picture, (int((width - width_rect) / 2), int(height / 75)))
        item_size = int(height_rect / 3 * 2)
        if shortage_item != 0:  # not research item
            scherm.blit(pg.transform.scale(eval("item_" + str(shortage_item) + "_picture"), (item_size, item_size)),
                        (int((width - width_rect) / 2), int((height / 75) + (height_rect - item_size) / 2)))
        elif shortage_item == 0:
            scherm.blit(pg.transform.scale(r_icon_picture, (item_size, item_size)), (
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


    def research_particles(scherm, r_particles):
        # index 0=x,1=y,2=size
        particles_pop = []
        img_transformed = -1
        for p in range(len(r_particles)):
            # draw
            img_transformed = pg.transform.scale(r_particle_picture, (int(r_particles[p][2]), int(r_particles[p][2])))
            scherm.blit(img_transformed,
                        (int(r_particles[p][0] - r_particles[p][2] / 2), int(r_particles[p][1] - r_particles[p][2] / 2)))
            # process
            r_particles[p][2] -= (r_particles[p][2] + 3) / 20
            if r_particles[p][2] < 1:  # size < ...
                particles_pop.append(p)

        for index in list(sorted(particles_pop))[::-1]:
            r_particles.pop(index)
        return r_particles


    def generate_r_particles_square(r_particles, x0, y0, x1, y1, size_range):
        spawn_rate = 25
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


    def generateGrid(grid, grid_rotation, breedte, hoogte, default = False, plot = False):
        run_idea = 5
        # 1 = default
        # 2 = referentie hoogte
        # 3 = random, dan smoothen
        # 4 = sinus
        if run_idea == 1:
            default = True
        else:
            default = False
        f = 3
        if default:
            for x in range(breedte):
                for y in range(hoogte):
                    grid[y, x] = r.choice([10, 11, 21, 22])
                    grid_rotation[y, x] = r.randint(0, 3)
        else:
            if run_idea == 2:
                sigma = 1  # m
                h0 = 0.4 * sigma
                grid_generation = np.zeros((breedte, hoogte))
                grid_generation[0, 0] = h0
                if grid_generation[0, 0] >= 0:
                    grid[0, 0] = r.choice([10, 11])
                else:
                    grid[0, 0] = r.choice([21, 22])
                for x in range(breedte):
                    for y in range(hoogte):
                        grid_rotation[y, x] = r.randint(0, 3)
                        if x == 0 and y == 0:
                            continue
                        if x == 0:
                            referentie_hoogte = grid_generation[y - 1, x] / f
                        elif y == 0:
                            referentie_hoogte = grid_generation[y, x - 1] / f

                        else:
                            referentie_hoogte = ((grid_generation[y, x - 1] + grid_generation[y - 1, x]) / 2 ) / f
                            
                        grid_generation[y, x] = r.normalvariate(referentie_hoogte, sigma)
                        if grid_generation[y, x] >= 0:
                            grid[y, x] = r.choice([10, 11])
                        else:
                            grid[y, x] = r.choice([21, 22])
            elif run_idea == 3:
                sigma = 1
                h0 = 0.4 * sigma
                grid_generation_v1 = np.zeros((breedte, hoogte))
                for x in range(breedte):
                    for y in range(hoogte):
                        grid_generation_v1[y, x] = r.normalvariate(h0, sigma)
                        grid_rotation[y, x] = r.randint(0, 3)


                grid_generation = np.zeros((breedte, hoogte))
                for x in range(breedte):
                    for y in range(hoogte):
                        h_total = grid_generation_v1[y, x]
                        n_total = 1
                        if x > 0:
                            h_total += grid_generation_v1[y, x-1]
                            n_total += 1
                        if x < breedte - 1:
                            h_total += grid_generation_v1[y, x + 1]
                            n_total += 1
                        if y > 0:
                            h_total += grid_generation_v1[y - 1, x]
                            n_total += 1
                        if y < hoogte - 1:
                            h_total += grid_generation_v1[y + 1, x]
                            n_total += 1

                        grid_generation[y, x] = h_total / n_total
                        
                
                        if grid_generation[y, x] >= 0:
                            grid[y, x] = r.choice([10, 11])
                        else:
                            grid[y, x] = r.choice([21, 22])
            elif run_idea == 4:
                from matplotlib import pyplot as plt
                a = []
                for x in range(100):
                    #a.append(r.randint(-5, 10))
                    a.append((100-x) * ((x % 3) - 1))
                #a = np.array([9, 2, -1, 4, -2, 6, -8, 2])
                a = np.array(a)
                f0 = breedte
                x = np.arange(0, breedte)
                pattern = np.zeros(x.shape)
                #plt.figure(1)
                for a_ in range(a.shape[0]):
                    pattern += a[a_] * np.sin(2*np.pi*(a_+1)*x/f0)
                    #plt.plot(x, pattern, label=str(a_+1))
                #plt.legend()
                #plt.show()
                grid_generation = np.zeros(grid.shape)
                for i in range(grid_generation.shape[1]):
                    grid_generation[:, i] += pattern
                f0 = hoogte
                x = np.arange(0, hoogte)
                pattern = np.zeros(x.shape)
                #plt.figure(1)
                for a_ in range(a.shape[0]):
                    pattern += a[a_] * np.sin(2*np.pi*(a_+1)*x/f0)
                    #plt.plot(x, pattern, label=str(a_+1))
                #plt.legend()
                #plt.show()
                for i in range(grid_generation.shape[0]):
                    grid_generation[i, :] += pattern
                for x in range(breedte):
                    for y in range(hoogte):
                        grid_rotation[y, x] = r.randint(0,3)
                        if grid_generation[y, x] >= 0:
                            grid[y, x] = r.choice([10, 11])
                        else:
                            grid[y, x] = r.choice([21, 22])
            elif run_idea == 5:
                import matplotlib.pyplot as plt
                from perlin_noise import PerlinNoise
                #import numpy as np
                #import random as r

                noise = PerlinNoise(octaves=15, seed=1)
                #import pdb;pdb.set_trace()
                pic = [[noise([i/breedte, j/hoogte]) for j in range(breedte)] for i in range(hoogte)]

                #plt.imshow(pic)
                
                grid_generation = grid
                for x in range(breedte):
                    for y in range(hoogte):
                        grid_rotation[y, x] = r.randint(0,3)
                        
                        if pic[y][x] > -0.075:
                            grid[y, x] = r.choice([10,11])
                        elif pic[y][x] > -0.15:
                            grid[y, x] = r.choice([23,24])
                        else:
                            grid[y,x] = r.choice([21,22])
                        #if pic[y][x] >= -0.13:
                        #    grid[y, x] = r.choice([10, 11])
                        #elif pic[y][x] >= -0.10:
                        #    grid[y, x] = r.choice([23,24])
                        #else:
                        #    grid[y, x] = r.choice([21, 22])

                

                
                
                        

            #for x in range(breedte):
            #    for y in range(hoogte):
            #        if x == 0 and y == 0:
            #            continue
            #        elif x == 0:
            #            referentie_hoogte = grid_generation[y + r.randint(-sigma, sigma), x]
            #        elif y == 0:
            #            referentie_hoogte = grid_generation[y, x + r.randint(-sigma, sigma)]
            #        else:
            #            if x < 198 or y < 198:
            #                referentie_hoogte = (grid_generation[y, x -1] + grid_generation[y, x -1]) / 2 + r.uniform(-sigma, sigma)
            #            else:
            #                referentie_hoogte = (grid_generation[y, x + r.randint(-sigma, sigma)] + grid_generation[y + r.randint(-sigma, sigma), x]) / 2 + r.uniform(-sigma, sigma)#

            #        grid_generation[y, x] = r.normalvariate(referentie_hoogte, sigma)
            #        if grid_generation[y, x] >= 0:
            #            grid[y, x] = r.choice([10, 11])
            #        else:
            #            grid[y, x] = r.choice([21, 22])



            if plot:
                from matplotlib import pyplot as plt
                
                #plt.figure(1)
                #plt.pcolormesh(grid_generation)
                #plt.colorbar()

                plt.figure(2)
                plt.pcolormesh(grid)
                plt.colorbar()
                
                #ax = plt.figure(3).add_subplot(projection='3d')
                #ax.plot_wireframe(np.array([np.arange(0, grid.shape[1]) for i in range(grid.shape[0])]),
                #             np.array([[i] * grid.shape[0] for i in range(grid.shape[1])]),
                #             grid_generation)

                plt.show()
                            
                    

        return grid, grid_rotation


    if __name__ == '__main__':
        pg.font.quit()
        pg.quit()
