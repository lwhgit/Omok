class OmokBoard:
    length = 0
    map = None
    viewer = None
    
    def __init__(self, length = 15):
        self.length = length
        self.map = [[0] * length for i in range(length)]
        
    def putStone(self, x, y, type):
        if self.isImpossable(x, y, type):
            return -1
        
        self.map[x][y] = type
        if self.viewer != None:
            self.viewer.putStone(x + 1, y + 1, type)
        if self.__check(x, y, type):
            return type
        return 0
        
    def isImpossable(self, x, y, type):
        dx = [0, 1, 1, 1];
        dy = [1, 1, 0, -1];
        
        if (x < 0) or (x >= self.length) or (y < 0) or (y >= self.length) or self.map[x][y] != 0:
            return True
        
        if type == 1:
            for axis in range(4):
                for rotation in range(axis + 1, axis + 3):
                        
                    if rotation > 3:
                        rotation -= 3
                        
                    acount = self.__getCount(x, y, dx[axis], dy[axis], type)
                    rcount = self.__getCount(x, y, dx[rotation], dy[rotation], type)
                    
                    if ((acount == (2, 0) and rcount == (3, 0)) or
                        (acount == (3, 0) and rcount == (2, 0)) or
                        (acount == (3, 0) and rcount == (3, 0))):
                        return True
                        
        return False
    
    def __check(self, x, y, type):
        dx = [0, 1, 1, 1];
        dy = [1, 1, 0, -1];
        for i in range(0, 4):
            if self.__getCount(x, y, dx[i], dy[i], type)[0] == 4:
                return True
            
    def __getCount(self, x, y, dx, dy, type):
        side1 = 0
        side2 = 0
        count = 0
        i = 0
        
        while True:
            i += 1
            
            tx = x + dx * i
            ty = y + dy * i
            
            if 0 <= tx and tx < self.length and 0 <= ty and ty < self.length:
                if self.map[tx][ty] == type:
                    count += 1
                else:
                    break
            else:
                break
        
        tx += dx
        ty += dy
        if 0 <= tx and tx < self.length and 0 <= ty and ty < self.length:
            side1 = self.map[tx][ty]
        else:
            side1 = 0
            
        i = 0
        
        while True:
            i += 1
            
            tx = x - dx * i
            ty = y - dy * i
            
            if 0 <= tx and tx < self.length and 0 <= ty and ty < self.length:
                if self.map[tx][ty] == type:
                    count += 1
                else:
                    break
            else:
                break
        
        tx -= dx
        ty -= dy
        if 0 <= tx and tx < self.length and 0 <= ty and ty < self.length:
            side2 = self.map[tx][ty]
        else:
            side2 = 0
                
        return (count, side1 + side2)
                    
    def setViewer(self, viewer):
        self.viewer = viewer
        
    def showMap(self):
        s = ""
        for y in range(0, self.length):
            for x in range(0, self.length):
                s += str("{0:>4d}".format(self.map[x][y]))
            s += "\n"
        print(s)