import os
import pygame, sys
#import time
import random
from pygame.locals import *
from math import cos, sin, sqrt, pi
from numpy import arange, linspace
import geometry

os.environ['SDL_VIDEO_WINDOW_POS'] = "3000,200"

WINDOWSIZE = (500,400)
FPS = 40

HEXSIDE       = 50
WHITE         = (255,255,255)
HEXEDGECOLOR  = (127,127,127)
BLUE          = (63, 63, 255)
RED          = (255, 0, 63)
SQRT3 = sqrt(3)

class DrawAPI:
    def __init__(self,display):
        self.display = display
        self.get_h_lookup = {}

    def draw_hexagon(self,hex_id,color=WHITE,off=(0,0),rot=0):
        if (hex_id,off,rot) not in self.get_h_lookup:
            (i,j) = hex_id
            j = j - off[1]
            center = get_hex_center((i,j))
            h = []
            for k in range(6):
                corner = get_hex_corner(center,0.95,k)
                corner = add_rotation(corner,rot)
                corner = add_perspective(corner)
                corner = window_coordinates(corner)
                h.append(corner)
            if not any(check_if_point_in_window(p) for p in h):
                h = []
            self.get_h_lookup[(hex_id,off,rot)] = h
        
        h = self.get_h_lookup[(hex_id,off,rot)]
        
        if h:
            pygame.draw.polygon(self.display,color,h)
            pygame.draw.polygon(self.display,HEXEDGECOLOR,h,1)
        
    def highlight_hexagon(self,hex_id,color,off=(0,0),rot=0):
        (i,j) = hex_id
        j = j - off[1]
        center = get_hex_center((i,j))
        h = []
        for k in range(6):
            corner = get_hex_corner(center,0.95,k)
            corner = add_rotation(corner,rot)
            corner = add_perspective(corner)
            corner = window_coordinates(corner)
            h.append(corner)
            
        pygame.draw.polygon(self.display,color,h)

class Bear:
    def __init__(self,position,direction,color):
        self.position  = position
        self.direction = direction
        self.color = color
        
    def draw(self,draw_api,astep=0,rot=0):
        draw_api.highlight_hexagon(self.position,self.color,off=(0,astep),rot=rot)
        
    def shift_left(self):
        self.position = geometry.new_position_left(self.position)
        
    def shift_right(self):
        self.position = geometry.new_position_right(self.position)
        
    def shift_forward(self):
        self.position = geometry.new_position_forward(self.position)
        
    def destination(self):
        (i,j) = self.position
        d = {0:(i,j+1),1:(i-1,j+1),2:(i-1,j),3:(i,j-1),4:(i+1,j-1),5:(i+1,j)}
        return d.get(self.direction)
        

def add_perspective(p):
    (x,y) = p
    a = 2/3
    e = 2/3
    h = 1/20
 
    return (a*x/(h*y+1),e*y/(h*y+1))
    
def add_rotation(p,rotation_step):
    (x,y) = p
    theta = pi / 180 * (rotation_step * 60)
    
    return (x*cos(theta)-y*sin(theta),x*sin(theta)+y*cos(theta))

def get_hex_corner(center, size, i):
    (cx,cy) = center
    theta   = pi / 180 * (60 * i)
    
    return (cx + size * cos(theta), cy + size * sin(theta))
    
def window_coordinates(point):
    (px,py) = point
    (wx,wy) = WINDOWSIZE
    
    return (0.5*wx+HEXSIDE*px,0.7*wy-HEXSIDE*py)
    
def check_if_point_in_window(point):
    (px,py) = point
    (wx,wy) = WINDOWSIZE
    
    return (0 <= px <= wx and 0 <= py <= wy)
    
def random_ice_color():    
    blue = random.randrange(16)
    gray = blue*2
    
    return (255-gray,255-gray,255-blue)
    
def ice_color_array(n):
    l = []
    for i in range(n):
        l.append(random_ice_color())
    return l
    
def get_hex_center(hexagon_id):
    (i,j) = hexagon_id
    
    x = 1.5*i
    y = (0.5*i+j)*SQRT3
    
    return (x,y)

def main():
    pygame.init()
    random.seed(0)

    screen=pygame.display.set_mode(WINDOWSIZE)

    screen.fill(WHITE)

    hex_depth = 20
    
    arctic = geometry.Arctic(hex_depth)

    ice_color = ice_color_array(arctic.size)

    draw_api = DrawAPI(screen)
    fpsClock = pygame.time.Clock()
            
    for hex_id in arctic.matrix:
        draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color))

    player_bear = Bear((0,0),0,BLUE)
    another_bear = Bear((2,2),0,RED) 
    
    player_bear.draw(draw_api)
    another_bear.draw(draw_api)
    
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:
                if (event.key == K_UP):
                    #steptime = [] 
                    for astep in linspace(0,1,20):
                        screen.fill(WHITE)
                        #before = time.time()
                        for hex_id in arctic.matrix:
                            draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color),off=(0,astep))
                        player_bear.draw(draw_api)
                        another_bear.draw(draw_api,astep)
                        #after = time.time()
                        #steptime.append(after-before)
                        pygame.display.update()
                        fpsClock.tick(FPS)
                    
                    screen.fill(WHITE)
                    
                    ice_color = arctic.move_forward(ice_color,ice_color_array(2*arctic.depth+1))
                    
                    another_bear.shift_forward()
                    
                    for hex_id in arctic.matrix:
                        draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color))
                    
                    player_bear.draw(draw_api)
                    another_bear.draw(draw_api)
                    
                    #print(f"mean time: {sum(steptime)*1000/20}")
                    
                if (event.key == K_RIGHT):
                    for astep in linspace(0,1,20):
                        screen.fill(WHITE)
                        for hex_id in arctic.matrix:
                            draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color),rot=astep)
                        player_bear.draw(draw_api)
                        another_bear.draw(draw_api,rot=astep)
                        pygame.display.update()
                        fpsClock.tick(FPS)
                    
                    screen.fill(WHITE)
                                        
                    ice_color = arctic.turn_right(ice_color)
                    another_bear.shift_right()

                    for hex_id in arctic.matrix:
                        draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color))
                            
                    player_bear.draw(draw_api)
                    another_bear.draw(draw_api)                
                     
                if (event.key == K_LEFT):
                    for astep in linspace(0,-1,20):
                        screen.fill(WHITE)
                        for hex_id in arctic.matrix:
                            draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color),rot=astep)
                        player_bear.draw(draw_api)
                        another_bear.draw(draw_api,rot=astep)
                        pygame.display.update()
                        fpsClock.tick(FPS)
                    
                    screen.fill(WHITE)
                    
                    ice_color = arctic.turn_left(ice_color)
                    another_bear.shift_left()
                    
                    for hex_id in arctic.matrix:
                        draw_api.draw_hexagon(hex_id,color=arctic.get(hex_id,ice_color))
                                                
                    player_bear.draw(draw_api)
                    another_bear.draw(draw_api)
                    
                if (event.key == K_ESCAPE):
                    print(sys.getsizeof(draw_api.get_h_lookup))
        
        pygame.display.update()

main()