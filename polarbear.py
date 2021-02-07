import os
import pygame, sys
#import time
import random
import draw
import pygame.locals as pg
from numpy import arange, linspace
import geometry, bear

os.environ['SDL_VIDEO_WINDOW_POS'] = "3000,200"

FPS = 40

BLUE          = (63, 63, 255)
RED           = (255, 0, 63)
LIGHTRED      = (255,159,191)
    
def random_ice_color():    
    blue = random.randrange(16)
    gray = blue*2
    
    return (255-gray,255-gray,255-blue)
    
def ice_color_array(n):
    l = []
    for i in range(n):
        l.append(random_ice_color())
    return l

def add_trail(arctic,ia,bear):
    ja = list(ia)
    for (k,hex_id) in enumerate(bear.trail):
        ja[arctic.center[hex_id]] = LIGHTRED
    
    return ja

def main():
    random.seed(0)
    
    draw_api = draw.init()

    hex_depth = 20
    
    arctic = geometry.Arctic(hex_depth)
    
    pure_ice_color = ice_color_array(arctic.size)
    
    player_bear = bear.Bear((0,0),0,BLUE)
    another_bear = bear.Bear((1,0),0,RED)

    ice_color = add_trail(arctic,pure_ice_color,another_bear)

    fpsClock = pygame.time.Clock()
            
    for hex_id in arctic.matrix:
        draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color))
    
    player_bear.draw(draw_api)
    another_bear.draw(draw_api)    
    
    while True:
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_UP):
                    #steptime = [] 
                    for astep in linspace(0,1,20):
                        draw_api.clear()
                        #before = time.time()
                        for hex_id in arctic.matrix:
                            draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color),off=(0,-astep))
                        player_bear.draw(draw_api)
                        another_bear.draw(draw_api,off=(0,-astep),astep=astep)
                        #after = time.time()
                        #steptime.append(after-before)
                        pygame.display.update()
                        fpsClock.tick(FPS)
                    
                    draw_api.clear()
                    
                    pure_ice_color = arctic.move_forward(pure_ice_color,ice_color_array(2*arctic.depth+1))
                                        
                    ice_color = add_trail(arctic,pure_ice_color,another_bear)
                    
                    another_bear.shift_forward()
                    
                    for hex_id in arctic.matrix:
                        draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color))
                    
                    player_bear.draw(draw_api)
                    another_bear.move()
                    another_bear.draw(draw_api)
                    
                    #print(f"mean time: {sum(steptime)*1000/20}")
                    
                if (event.key == pg.K_RIGHT):
                    for astep in linspace(0,1,20):
                        draw_api.clear()
                        for hex_id in arctic.matrix:
                            draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color),rot=astep)
                        player_bear.draw(draw_api)
                        another_bear.draw(draw_api,rot=astep,astep=astep)
                        pygame.display.update()
                        fpsClock.tick(FPS)
                    
                    draw_api.clear()
                                        
                    another_bear.turn_left()
                    another_bear.rotate_right()
                    another_bear.move()
                    pure_ice_color = arctic.turn_right(pure_ice_color)
                    ice_color = add_trail(arctic,pure_ice_color,another_bear)

                    for hex_id in arctic.matrix:
                        draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color))
                            
                    player_bear.draw(draw_api)
                    another_bear.draw(draw_api)                
                     
                if (event.key == pg.K_LEFT):
                    for astep in linspace(0,1,20):
                        draw_api.clear()
                        for hex_id in arctic.matrix:
                            draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color),rot=-astep)
                        player_bear.draw(draw_api)
                        another_bear.draw(draw_api,rot=-astep,astep=astep)
                        pygame.display.update()
                        fpsClock.tick(FPS)
                    
                    draw_api.clear()

                    another_bear.turn_right()
                    another_bear.rotate_left()
                    another_bear.move()
                    pure_ice_color = arctic.turn_left(pure_ice_color)
                    ice_color = add_trail(arctic,pure_ice_color,another_bear)
                    
                    for hex_id in arctic.matrix:
                        draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color))
                                                
                    player_bear.draw(draw_api)
                    another_bear.draw(draw_api)

                if (event.key == pg.K_DOWN):
                    another_bear.set_destination()
                
                    for astep in linspace(0,1,20):
                        draw_api.clear()
                        for hex_id in arctic.matrix:
                            draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color))
                        player_bear.draw(draw_api)
                        another_bear.draw(draw_api,astep=astep)
                        pygame.display.update()
                        fpsClock.tick(FPS)
                    
                    draw_api.clear()
                    
                    another_bear.move()                    
                                                            
                    ice_color = add_trail(arctic,pure_ice_color,another_bear)
                                        
                    for hex_id in arctic.matrix:
                        draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color))
                                                
                    player_bear.draw(draw_api)
                    another_bear.draw(draw_api)
                    
                if (event.key == pg.K_ESCAPE):
                    print(sys.getsizeof(draw_api.get_h_lookup))
        
        pygame.display.update()

main()