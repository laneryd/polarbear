class Arctic:
    def __init__(self, depth):
        self.depth  = depth
        self.matrix = []
        self.center = {}
        self.right  = {}
        self.left   = {}
        
        count = 0

        for j in range(depth,-1,-1):
            for i in range(-depth,depth+1-j):
                self.matrix.append((i,j))
                self.center[(i,j)]   = count
                self.left[(-j,j+i)]  = count
                self.right[(i+j,-i)] = count
                count = count + 1

        for j in range(-1,-depth-1,-1):
            for i in range(-depth-j,depth+1):
                self.matrix.append((i,j))
                self.center[(i,j)]   = count
                self.left[(-j,j+i)]  = count
                self.right[(i+j,-i)] = count
                count = count + 1

def rotate_left(arctic,p):
    q = list(p)
    for hex_id in arctic.matrix:
        q[arctic.left[hex_id]] = p[arctic.center[hex_id]]
    return q
    
def rotate_right(arctic,p):
    q = list(p)
    for hex_id in arctic.matrix:
        q[arctic.right[hex_id]] = p[arctic.center[hex_id]]
    return q

def get(arctic,hex_id,p):
    return p[arctic.center[hex_id]]