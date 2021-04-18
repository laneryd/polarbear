import geometry
import itertools

TRAILLENGTH   = 8

class Bear:
    id_iter = itertools.count()

    def __init__(self,position,direction,color,trailcolor,sex):
        self.position    = position
        self.direction   = direction
        self.destination = geometry.adjacent(self.position,self.direction)
        
        self.trail = [position]
        for k in range(TRAILLENGTH-1):
            self.trail.append(geometry.adjacent(self.trail[k],(self.direction+5) % 6 - 2))
        
        self.color      = color
        self.trailcolor = trailcolor
        self.sex        = sex
        self.exhaustion = 0
        self.identity   = next(Bear.id_iter)
        
    def move(self):
        if self.destination == geometry.adjacent(self.position,self.direction):
            self.position = geometry.adjacent(self.position,self.direction)
            self.exhaustion += 1
        #self.purpose()
        self.trail.insert(0,self.position)
        self.trail.pop()
    
    def purpose(self):
        if self.exhaustion > 3:
            self.destination = self.position
            self.turn_left()
            self.exhaustion -= 1
        else:
            self.destination = geometry.adjacent(self.position,self.direction)
    
    def draw(self,draw_api,astep=0,off=(0,0),rot=0):
        if self.position != self.destination:
            (ia,ja) = self.position
            (ib,jb) = geometry.adjacent(self.position,self.direction)
            (io,jo) = off
            offsum   = (io+(ib-ia)*astep,jo+(jb-ja)*astep)
        else:
            offsum = off
                
        draw_api.highlight_hexagon(self.position,self.color,off=offsum,rot=rot)
        
    def turn_left(self):
        self.direction = (self.direction + 3) % 6 - 2
        
    def turn_right(self):
        self.direction = (self.direction + 1) % 6 - 2
        
    def rotate_left(self):
        self.position    = geometry.rotate_left(self.position)
        self.destination = geometry.rotate_left(self.destination)
        for k in range(TRAILLENGTH):
            self.trail[k] = geometry.rotate_left(self.trail[k])
        
    def rotate_right(self):
        self.position    = geometry.rotate_right(self.position)
        self.destination = geometry.rotate_right(self.destination)
        for k in range(TRAILLENGTH):
            self.trail[k] = geometry.rotate_right(self.trail[k])
        
    def shift_forward(self):
        self.position    = geometry.adjacent(self.position,3)
        self.destination = geometry.adjacent(self.destination,3)
        for k in range(TRAILLENGTH):
            self.trail[k] = geometry.adjacent(self.trail[k],3)
            
    def put_trail(self,arctic):
        for (k,hex_id) in enumerate(self.trail):
            fadingcolor = tuple([c*(TRAILLENGTH-k) for c in self.trailcolor])
            arctic.add_color(hex_id,fadingcolor)
            
    def describe(self):
        if self.sex == 'M':
            sex = 'Male'
        else:
            sex = 'Female'
        print('Polarbear', self.identity, 'at', self.position, 'destined for', self.destination)
        
    def relative_direction(self,absolute_direction):
        return (absolute_direction - self.direction + 2) % 6 - 2
        