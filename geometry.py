def new_position_left(hex_id):
    (i,j) = hex_id
    return (i+j,-i)

def new_position_right(hex_id):
    (i,j) = hex_id
    return (-j,j+i)
    
def new_position_forward(hex_id):
    (i,j) = hex_id
    return (i,j-1)

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

    def turn_left(self,p):
        q = list(p)
        for hex_id in self.matrix:
            q[self.left[hex_id]] = p[self.center[hex_id]]
        return q
        
    def turn_right(self,p):
        q = list(p)
        for hex_id in self.matrix:
            q[self.right[hex_id]] = p[self.center[hex_id]]
        return q
        
    def move_forward(self,p,elem):
        q = list(p)
        for hex_id in self.matrix:
            (i,j) = hex_id
            if max(j,i+j) >= self.depth:
                q[self.center[hex_id]] = elem.pop(0)
            else:
                q[self.center[hex_id]] = p[self.forward[hex_id]]
        return q

    def get(self,hex_id,p):
        return p[self.center[hex_id]]