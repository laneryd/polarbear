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

def turn_left(arctic,p):
    q = list(p)
    for hex_id in arctic.matrix:
        q[arctic.left[hex_id]] = p[arctic.center[hex_id]]
    return q
    
def turn_right(arctic,p):
    q = list(p)
    for hex_id in arctic.matrix:
        q[arctic.right[hex_id]] = p[arctic.center[hex_id]]
    return q
    
def move_forward(arctic,p,elem):
    q = list(p)
    for hex_id in arctic.matrix:
        (i,j) = hex_id
        if max(j,i+j) >= arctic.depth:
            q[arctic.center[hex_id]] = elem.pop(0)
        else:
            q[arctic.center[hex_id]] = p[arctic.forward[hex_id]]
    return q

def get(arctic,hex_id,p):
    return p[arctic.center[hex_id]]