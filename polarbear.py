import os
import pygame
import sys
import draw
import pygame.locals as pg
from numpy import arange, linspace
import geometry, bear

#os.environ['SDL_VIDEO_WINDOW_POS'] = "3000,200"

FPS = 40

HEXDEPTH = 4

BLUE          = (63, 63, 255)
RED           = (255, 0, 63)
LIGHTRED      = (255,159,191)
INVLIGHTRED   = (0,-96,-64)

def add_trail(arctic,ia,bear):
    ja = list(ia)
    for (k,hex_id) in enumerate(bear.trail):
        ja[arctic.center[hex_id]] = LIGHTRED
    
    return ja

def animate(draw_api,arctic,player_bear,list_of_bears,fpsClock,cr=0,co=0):
    for astep in linspace(0,1,20):
        draw_api.clear()
        for hex_id in arctic.matrix:
            draw_api.draw_hexagon(hex_id,color=arctic.color(hex_id),off=(0,co*astep),rot=cr*astep)
        player_bear.draw(draw_api)
        for b in list_of_bears:
            b.draw(draw_api,off=(0,co*astep),rot=cr*astep,astep=astep)
        pygame.display.update()
        fpsClock.tick(FPS)
    
    draw_api.clear()
    
def redraw(draw_api,arctic,player_bear,list_of_bears):
    for hex_id in arctic.matrix:
        draw_api.draw_hexagon(hex_id,color=arctic.color(hex_id))
                                
    player_bear.draw(draw_api)
    for b in list_of_bears:
        b.draw(draw_api)

def main():
    #random.seed(0)
    
    draw_api = draw.init()
    
    arctic = geometry.Arctic(HEXDEPTH)
    
    player_bear = bear.Bear((0,0),0,BLUE,BLUE)
    another_bear = bear.Bear((1,3),2,RED,INVLIGHTRED)
    another_bear.put_trail(arctic)
    list_of_bears = [another_bear]

    fpsClock = pygame.time.Clock()
            
    for hex_id in arctic.matrix:
        draw_api.draw_hexagon(hex_id,color=arctic.color(hex_id))
    
    player_bear.draw(draw_api)
    another_bear.draw(draw_api)    
    
    while True:
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_UP):
                    co = -1
                    animate(draw_api,arctic,player_bear,list_of_bears,fpsClock,co=co)
                    
                    arctic.move_forward()

                    for b in list_of_bears:
                        b.shift_forward()
                        b.move()
                        b.put_trail(arctic)
                    
                    redraw(draw_api,arctic,player_bear,list_of_bears)
                                       
                if (event.key == pg.K_RIGHT):
                    cr = 1
                    animate(draw_api,arctic,player_bear,list_of_bears,fpsClock,cr=cr)
                                        
                    arctic.turn_right()

                    for b in list_of_bears:
                        b.turn_left()
                        b.rotate_right()
                        b.move()
                        b.put_trail(arctic)
                    
                    redraw(draw_api,arctic,player_bear,list_of_bears)

                    for hex_id in arctic.matrix:
                        draw_api.draw_hexagon(hex_id,color=arctic.color(hex_id))
                            
                    player_bear.draw(draw_api)
                    for b in list_of_bears:
                        b.draw(draw_api)
                     
                if (event.key == pg.K_LEFT):
                    cr = -1
                    animate(draw_api,arctic,player_bear,list_of_bears,fpsClock,cr=cr)

                    arctic.turn_left()
                    
                    for b in list_of_bears:
                        b.turn_right()
                        b.rotate_left()
                        b.move()
                        b.put_trail(arctic)
                    
                    redraw(draw_api,arctic,player_bear,list_of_bears)

                if (event.key == pg.K_DOWN):
                    animate(draw_api,arctic,player_bear,list_of_bears,fpsClock)
                    
                    arctic.remain()
                    
                    for b in list_of_bears:
                        b.move()
                        b.put_trail(arctic)
                    
                    redraw(draw_api,arctic,player_bear,list_of_bears)
                    
                if (event.key == pg.K_ESCAPE):
                    print(sys.getsizeof(draw_api.get_h_lookup))
        
        pygame.display.update()

main()