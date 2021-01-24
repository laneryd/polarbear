import os
import pygame, sys
import time
import random
from pygame.locals import *
from math import cos, sin, sqrt, pi
from numpy import arange, linspace

os.environ['SDL_VIDEO_WINDOW_POS'] = "3000,200"

WINDOWSIZE = (500,400)
FPS = 30

HEXSIDE       = 50
WHITE         = (255,255,255)
HEXEDGECOLOR  = (127,127,127)
LIGHTBLUE     = (191,191,255)
BLUE          = (63, 63, 255)
SQRT3 = sqrt(3)

class DrawAPI:
    def __init__(self,display):
        self.display = display
        self.get_h_lookup = {}

    def draw_hexagon(self,hex_id,color=WHITE,off=0,rot=0):
        if (hex_id,off,rot) not in self.get_h_lookup:
            (i,j) = hex_id
            j = j - off
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
        
    def highlight_hexagon(self,hexagon_id):
        center = get_hex_center(hexagon_id)
        h = []
        for k in range(6):
            corner = get_hex_corner(center,0.95,k)
            corner = add_perspective(corner)
            corner = window_coordinates(corner)
            h.append(corner)
            
        pygame.draw.polygon(self.display,BLUE,h)

def add_perspective(p):
    (x,y) = p
    a = 2/3
    e = 2/3
    h = 1/20
    
    #return (a*x/abs(h*y+1),e*y/abs(h*y+1))
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
    
    return (0.5*wx+HEXSIDE*px,0.5*wy-HEXSIDE*py)
    
def check_if_point_in_window(point):
    (px,py) = point
    (wx,wy) = WINDOWSIZE
    
    return (0 <= px <= wx and 0 <= py <= wy)
    
def random_ice_color():
    # gray = random.randrange(32)
    # blue = min(random.randrange(16),gray)
    
    blue = random.randrange(16)
    gray = blue*2
    
    return (255-gray,255-gray,255-blue)
    
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
    
    hex_n = 3*hex_depth*hex_depth+3*hex_depth+1 
    
    hex_number = []
    elem = {}
    count = 0
    
    for j in range(hex_depth,-1,-1):
        hex_row = []
        for i in range(-hex_depth,hex_depth+1-j):
            hex_row.append((i,j))
            elem[(i,j)] = count
            count = count + 1
        hex_number.append(hex_row)

    for j in range(-1,-hex_depth-1,-1):
        hex_row = []
        for i in range(-hex_depth-j,hex_depth+1):
            hex_row.append((i,j))
            elem[(i,j)] = count
            count = count + 1
        hex_number.append(hex_row)
                
    ice_color  = []    
    for i in range(hex_n):
        ice_color.append(random_ice_color())

    draw_api = DrawAPI(screen)
    fpsClock = pygame.time.Clock()
    
    for hex_row in hex_number:
        for hex_id in hex_row:
            draw_api.draw_hexagon(hex_id,color=ice_color[elem[hex_id]])

    draw_api.highlight_hexagon((0,0))
    
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:
                if (event.key == K_UP):
                    steptime = [] 
                    for astep in linspace(0,1,20):
                        screen.fill(WHITE)
                        before = time.time()
                        for hex_row in hex_number:
                            for hex_id in hex_row:
                                draw_api.draw_hexagon(hex_id,color=ice_color[elem[hex_id]],off=astep)
                        draw_api.highlight_hexagon((0,0))
                        after = time.time()
                        steptime.append(after-before)
                        pygame.display.update()
                        fpsClock.tick(FPS)
                    
                    screen.fill(WHITE)
                    
                    for hex_row in hex_number:
                            for hex_id in hex_row:
                                draw_api.draw_hexagon(hex_id,color=ice_color[elem[hex_id]])
                            
                    draw_api.highlight_hexagon((0,0))
                    #print(f"mean time: {sum(steptime)*1000/20}")
                    
                if (event.key == K_RIGHT):
                    for astep in linspace(0,1,20):
                        screen.fill(WHITE)
                        for hex_row in hex_number:
                            for hex_id in hex_row:
                                draw_api.draw_hexagon(hex_id,color=ice_color[elem[hex_id]],rot=astep)
                        draw_api.highlight_hexagon((0,0))
                        pygame.display.update()
                        fpsClock.tick(FPS)
                    
                    screen.fill(WHITE)
                    
                    for hex_row in hex_number:
                            for hex_id in hex_row:
                                draw_api.draw_hexagon(hex_id,color=ice_color[elem[hex_id]])
                            
                    draw_api.highlight_hexagon((0,0))
                     
                if (event.key == K_LEFT):
                    for astep in linspace(0,-1,20):
                        screen.fill(WHITE)
                        for hex_row in hex_number:
                            for hex_id in hex_row:
                                draw_api.draw_hexagon(hex_id,color=ice_color[elem[hex_id]],rot=astep)
                        draw_api.highlight_hexagon((0,0))
                        pygame.display.update()
                        fpsClock.tick(FPS)
                    
                    screen.fill(WHITE)
                    
                    for hex_row in hex_number:
                            for hex_id in hex_row:
                                draw_api.draw_hexagon(hex_id,color=ice_color[elem[hex_id]])
                                                
                    draw_api.highlight_hexagon((0,0))                   
                    
                if (event.key == K_ESCAPE):
                    print(sys.getsizeof(draw_api.get_h_lookup))
        
        pygame.display.update()

main()