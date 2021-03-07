import random

def rotate_left(hex_id):
    (i,j) = hex_id
    return (i+j,-i)

def rotate_right(hex_id):
    (i,j) = hex_id
    return (-j,j+i)
    
def adjacent(hex_id,direction):
    (i,j) = hex_id
    surrounding = {0:(i,j+1),1:(i-1,j+1),2:(i-1,j),3:(i,j-1),4:(i+1,j-1),5:(i+1,j)}
    return surrounding.get(direction)
    
def random_ice_color():    
    blue = random.randrange(16)
    gray = blue*2
    
    return (255-gray,255-gray,255-blue)
    
def ice_color_array(n):
    l = []
    for i in range(n):
        l.append(random_ice_color())
    return l

class Arctic:
    def __init__(self, depth):
        self.depth   = depth
        self.size    = 3*depth*depth+3*depth+1 
        self.matrix  = []
        self.center  = {}
        self.right   = {}
        self.left    = {}
        self.forward = {}
        
        count = 0

        for j in range(depth,-1,-1):
            for i in range(-depth,depth+1-j):
                self.matrix.append((i,j))
                self.center[(i,j)]    = count
                self.left[(-j,j+i)]   = count
                self.right[(i+j,-i)]  = count
                self.forward[(i,j-1)] = count
                count = count + 1

        for j in range(-1,-depth-1,-1):
            for i in range(-depth-j,depth+1):
                self.matrix.append((i,j))
                self.center[(i,j)]    = count
                self.left[(-j,j+i)]   = count
                self.right[(i+j,-i)]  = count
                self.forward[(i,j-1)] = count
                count = count + 1
                
        self.pure = ice_color_array(self.size)
        self.ice  = list(self.pure)
        
    def remain(self):
        self.ice  = list(self.pure)
    
    def turn_left(self):
        self.pure = self.turn_array_left(self.pure)
        self.ice  = list(self.pure)
        
    def turn_right(self):
        self.pure = self.turn_array_right(self.pure)
        self.ice  = list(self.pure)
        
    def move_forward(self):
        self.pure = self.move_array_forward(self.pure,ice_color_array(2*self.depth+1))
        self.ice  = list(self.pure)

    def turn_array_left(self,p):
        q = list(p)
        for hex_id in self.matrix:
            q[self.left[hex_id]] = p[self.center[hex_id]]
        return q
        
    def turn_array_right(self,p):
        q = list(p)
        for hex_id in self.matrix:
            q[self.right[hex_id]] = p[self.center[hex_id]]
        return q
        
    def move_array_forward(self,p,elem):
        q = list(p)
        for hex_id in self.matrix:
            (i,j) = hex_id
            if max(j,i+j) >= self.depth:
                q[self.center[hex_id]] = elem.pop(0)
            else:
                q[self.center[hex_id]] = p[self.forward[hex_id]]
        return q

    # def get(self,hex_id,p):
        # return p[self.center[hex_id]]
    
    def contains(self, hex_id):
        return hex_id in self.center
    
    def color(self,hex_id):
        return self.ice[self.center[hex_id]]
        
    def set_color(self,hex_id,color):
        self.ice[self.center[hex_id]] = color 
        
    def add_color(self,hex_id,color):
        if self.contains(hex_id):
            ice_color = self.ice[self.center[hex_id]]
            new_color = tuple([max(0,sum(c)) for c in zip(ice_color,color)])
            self.ice[self.center[hex_id]] = new_color