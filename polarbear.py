import os
import pygame
import sys
import draw
import pygame.locals as pg
from numpy import arange, linspace
import geometry, bear

#os.environ['SDL_VIDEO_WINDOW_POS'] = "3000,200"

FPS = 40

HEXDEPTH = 10

BEAR_ATTRACTION = 5

BLUE          = (63, 63, 255)
RED           = (255, 0, 63)
LIGHTRED      = (255,159,191)
INVLIGHTRED   = (0,-12,-8)
INVLIGHTBLUE  = (-12,-12,-0)

def animate(draw_api,arctic,list_of_bears,fpsClock,cr=0,co=0):
    for astep in linspace(0,1,20):
        draw_api.clear()
        for hex_id in arctic.matrix:
            draw_api.draw_hexagon(hex_id,color=arctic.color(hex_id),off=(0,co*astep),rot=cr*astep)
        for b in reversed(list_of_bears):
            b.draw(draw_api,off=(0,co*astep),rot=cr*astep,astep=astep)
        pygame.display.update()
        fpsClock.tick(FPS)
    
    draw_api.clear()
    
def redraw(draw_api,arctic,list_of_bears):
    for hex_id in arctic.matrix:
        try:
            draw_api.draw_hexagon(hex_id,color=arctic.color(hex_id))
        except ValueError:
            print('Value Error', arctic.color(hex_id))
    
    for b in reversed(list_of_bears):
        b.draw(draw_api)
        
def move_bears(arctic,list_of_bears):
    for b in list_of_bears:
        b.move()
        b.put_trail(arctic)
        
        if not arctic.contains(b.position):
            list_of_bears.remove(b)
            print('Bear outside arctic!')

def evaluate_hex_on_bear_position(bear_position_1,bear_position_2):
    bear_distance = draw.get_hex_distance(bear_position_1,bear_position_2)
    return max(0,BEAR_ATTRACTION - bear_distance)


def set_purpose(arctic,list_of_bears):
    for b in list_of_bears[1:]:
        a = [0]*6   # adjacent hexes
        c = 0       # current position
        a[b.direction+2] = 1
        for o in list_of_bears:
            if o.identity != b.identity:
               for i in range(6):
                   a[i] += evaluate_hex_on_bear_position(geometry.adjacent(b.position,i%6-2),o.position)
               c += evaluate_hex_on_bear_position(b.position,o.position)
        amax = max(a)
        #print(b.intent)
        if amax > c:
            #print(a.index(amax)%6-2)
            b.intent = a.index(amax)%6-2
        else:
            b.intent = None
        b.purpose()
        #print(b.intent)
            
# def set_purpose(arctic,list_of_bears):
    # for b in list_of_bears[1:]:
        # for o in list_of_bears:
            # if o.identity != b.identity:
                # d = draw.get_hex_distance(b.position,o.position)
                # a = draw.get_hex_direction(b.position,o.position)
                # r = b.relative_direction(a)
                # #print(o.identity, 'discovered at distance', '{0:.2f}'.format(d), 'and direction', '{0:.2f}'.format(r))
        # b.purpose()

def main():
    #random.seed(0)
    
    draw_api = draw.init()
    
    arctic = geometry.Arctic(HEXDEPTH)
    
    list_of_bears = []
    
    player_bear = bear.Bear((0,0),0,BLUE,INVLIGHTBLUE,'M')
    player_bear.put_trail(arctic)
    player_bear.destination = (0,0)
    list_of_bears.append(player_bear)
    
    another_bear = bear.Bear((1,0),1,RED,INVLIGHTRED,'F')
    another_bear.put_trail(arctic)
    list_of_bears.append(another_bear)
    yet_another_bear = bear.Bear((-4,4),-1,RED,INVLIGHTRED,'F')
    yet_another_bear.put_trail(arctic)
    list_of_bears.append(yet_another_bear)

    #print(draw.get_hex_distance(player_bear.position,another_bear.position))
    #print('{0:.2f}'.format(draw.get_hex_angle(player_bear.position,another_bear.position))+'°')

    fpsClock = pygame.time.Clock()
    
    redraw(draw_api,arctic,list_of_bears)
    
    set_purpose(arctic,list_of_bears)
    
    while True:
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_UP):
                    co = -1
                    list_of_bears[0].destination = (0,1)
                    
                    animate(draw_api,arctic,list_of_bears,fpsClock,co=co)
                    
                    arctic.move_forward()

                    for b in list_of_bears:
                        b.shift_forward()
                    
                    move_bears(arctic,list_of_bears)
                    set_purpose(arctic,list_of_bears)
                    redraw(draw_api,arctic,list_of_bears)
                                       
                if (event.key == pg.K_RIGHT):
                    cr = 1
                    
                    list_of_bears[0].turn_right()
                    
                    animate(draw_api,arctic,list_of_bears,fpsClock,cr=cr)
                                        
                    arctic.turn_right()

                    for b in list_of_bears:
                        b.turn_left()
                        b.rotate_right()
                        
                    move_bears(arctic,list_of_bears)
                    set_purpose(arctic,list_of_bears)
                    redraw(draw_api,arctic,list_of_bears)
                     
                if (event.key == pg.K_LEFT):
                    cr = -1
                    
                    list_of_bears[0].turn_left()
                    
                    animate(draw_api,arctic,list_of_bears,fpsClock,cr=cr)

                    arctic.turn_left()
                    
                    for b in list_of_bears:
                        b.turn_right()
                        b.rotate_left()
                        
                    move_bears(arctic,list_of_bears)
                    set_purpose(arctic,list_of_bears)
                    redraw(draw_api,arctic,list_of_bears)

                if (event.key == pg.K_DOWN):
                    animate(draw_api,arctic,list_of_bears,fpsClock)
                    
                    arctic.remain()

                    move_bears(arctic,list_of_bears)
                    set_purpose(arctic,list_of_bears)
                    redraw(draw_api,arctic,list_of_bears)
                    
                if (event.key == pg.K_ESCAPE):
                    print(sys.getsizeof(draw_api.get_h_lookup))
        
        pygame.display.update()

main()