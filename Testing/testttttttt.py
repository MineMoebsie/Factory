import pygame
import os

os.environ["SDL_HINT_RENDER_SCALE_QUALITY"]="best"
pygame.init()


pygame.display.set_caption('Vsync toggle test')
vsync = 1
scaled= 1
flags=pygame.FULLSCREEN|pygame.SCALED
res=1280, 720
window_surface = pygame.display.set_mode(res, flags=flags, vsync=vsync)

font = pygame.font.Font(None, 48)
fps_render = font.render('0 FPS', True, pygame.Color('#FFFFFF'))


clock = pygame.time.Clock()
is_running = True

x = 0

while is_running:
    time_delta = clock.tick()/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            scaled = int(not scaled)
            if scaled:
                flags=pygame.FULLSCREEN|pygame.SCALED
                res=1280,720
            else:
                flags=pygame.FULLSCREEN
                res=0,0
            window_surface = pygame.display.set_mode(res, flags=flags, vsync=vsync)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            vsync= int(not vsync)
            window_surface = pygame.display.set_mode(res, flags=flags, vsync=vsync)

    fps_render = font.render(f"{clock.get_fps():.2f}" + " FPS", True, pygame.Color('#FFFFFF'))
    
    w, h = window_surface.get_size()
    x= (x+3)%w

    window_surface.fill(0)

    for i in range(10):
        x1=(x+10*i)%w
        pygame.draw.line(window_surface, (255,255,255), (x1,0), (x1,h), 3)
    
    for i in range(10):
        x1=(x+100+3*i)%w
        pygame.draw.line(window_surface, (255,255,255), (x1,0), (x1,h))


    window_surface.blit(fps_render, (50, 50))

    pygame.display.update()