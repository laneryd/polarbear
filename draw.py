import pygame
from math import cos, sin, sqrt, pi, atan2

HEXSIDE       = 50
HEXSIZEFACTOR = 0.95
WINDOWSIZE    = (500,400)
WHITE         = (255,255,255)
HEXEDGECOLOR  = (127,127,127)
SQRT3 = sqrt(3)

class DrawAPI:
    def __init__(self,display):
        self.display = display
        self.get_h_lookup = {}
        self.clear()

    def draw_hexagon(self,hex_id,color=WHITE,off=(0,0),rot=0):
        if (hex_id,off,rot) not in self.get_h_lookup:
            (i,j) = hex_id
            j = j + off[1]

            h = get_hexagon(i,j,rot)
            self.get_h_lookup[(hex_id,off,rot)] = h
        
        h = self.get_h_lookup[(hex_id,off,rot)]
        
        if h:
            pygame.draw.polygon(self.display,color,h)
            pygame.draw.polygon(self.display,HEXEDGECOLOR,h,1)
        
    def highlight_hexagon(self,hex_id,color,off=(0,0),rot=0):
        (i,j) = hex_id
        i = i + off[0]
        j = j + off[1]
        
        h = get_hexagon(i,j,rot)
        
        if h:    
            pygame.draw.polygon(self.display,color,h)

    def clear(self):
        self.display.fill(WHITE)

def get_hexagon(i,j,rot):
    center = get_hex_center((i,j))
    h = []
    for k in range(6):
        corner = get_hex_corner(center,HEXSIZEFACTOR,k)
        corner = add_rotation(corner,rot)
        corner = add_perspective(corner)
        corner = window_coordinates(corner)
        h.append(corner)
    if not any(check_if_point_in_window(p) for p in h):
        h = []
    return h
        
def get_hex_corner(center, size, i):
    (cx,cy) = center
    theta   = pi / 180 * (60 * i)
    
    return (cx + size * cos(theta), cy + size * sin(theta))
            
def get_hex_center(hexagon_id):
    (i,j) = hexagon_id
    
    x = 1.5*i
    y = (0.5*i+j)*SQRT3
    
    return (x,y)
    
def get_hex_distance(hex_id_a, hex_id_b):
    (xa,ya) = get_hex_center(hex_id_a)
    (xb,yb) = get_hex_center(hex_id_b)
    
    return sqrt((xb-xa)**2 + (yb-ya)**2)
    
def get_hex_angle(hex_id_a, hex_id_b):
    (xa,ya) = get_hex_center(hex_id_a)
    (xb,yb) = get_hex_center(hex_id_b)
    
    return atan2(-(xb-xa),(yb-ya))*180/pi
    
def add_rotation(p,rotation_step):
    (x,y) = p
    theta = pi / 180 * (rotation_step * 60)
    
    return (x*cos(theta)-y*sin(theta),x*sin(theta)+y*cos(theta))
    
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
    
def window_coordinates(point):
    (px,py) = point
    (wx,wy) = WINDOWSIZE
    
    return (0.5*wx+HEXSIDE*px,0.7*wy-HEXSIDE*py)
    
def check_if_point_in_window(point):
    (px,py) = point
    (wx,wy) = WINDOWSIZE
    
    return (0 <= px <= wx and 0 <= py <= wy)
    
def init():
    pygame.init()

    draw_api = DrawAPI(pygame.display.set_mode(WINDOWSIZE))
    return draw_api