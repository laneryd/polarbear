class Arctic:
    def __init__(self, depth):
        self.depth  = depth
        self.matrix = []

        for j in range(depth,-1,-1):
            for i in range(-depth,depth+1-j):
                self.matrix.append((i,j))

        for j in range(-1,-depth-1,-1):
            for i in range(-depth-j,depth+1):
                self.matrix.append((i,j))
