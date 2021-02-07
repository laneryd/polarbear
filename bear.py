import geometry

TRAILLENGTH   = 3

class Bear:
    def __init__(self,position,direction,color):
        self.position    = position
        self.direction   = direction
        self.destination = geometry.adjacent(self.position,self.direction)
        
        self.trail = [position]
        for k in range(TRAILLENGTH-1):
            self.trail.append(geometry.adjacent(self.trail[k],self.direction+3))
        
        self.color = color
        
    def move(self):
        self.position    = geometry.adjacent(self.position,self.direction)
        self.destination = geometry.adjacent(self.position,self.direction)
        self.trail.insert(0,self.position)
        self.trail.pop()
        
    def draw(self,draw_api,astep=0,off=(0,0),rot=0):
        (ia,ja) = self.position
        (ib,jb) = self.destination
        (io,jo) = off
        offsum   = (io+(ib-ia)*astep,jo+(jb-ja)*astep)
        
        draw_api.highlight_hexagon(self.position,self.color,off=offsum,rot=rot)
        
    def turn_left(self):
        self.direction = (self.direction + 1) % 6
        
    def turn_right(self):
        self.direction = (self.direction - 1) % 6
        
    def rotate_left(self):
        self.position = geometry.rotate_left(self.position)
        for k in range(TRAILLENGTH):
            self.trail[k] = geometry.rotate_left(self.trail[k])
        
    def rotate_right(self):
        self.position = geometry.rotate_right(self.position)
        for k in range(TRAILLENGTH):
            self.trail[k] = geometry.rotate_right(self.trail[k])
        
    def shift_forward(self):
        self.position = geometry.adjacent(self.position,3)
        for k in range(TRAILLENGTH):
            self.trail[k] = geometry.adjacent(self.trail[k],3)