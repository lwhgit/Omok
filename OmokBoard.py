class OmokBoard:
    length = 0
    map = None
    viewer = None
    
    def __init__(self, length = 15):
        self.length = length
        self.map = [[0] * length for i in range(length)]
        
    def putStone(self, x, y, type):
        if self.__isImossable(x, y, type):
            return -1
        
        self.map[x][y] = type
        if self.viewer != None:
            self.viewer.putStone(x, y, type)
        if self.__check(x, y, type):
            return type
        return 0
        
    def __isImossable(self, x, y, type):
        dx = [0, 1, 1, 1];
        dy = [1, 1, 0, -1];
        
        if type == 1:
            for axis in range(4):
                for rotation in range(axis + 1, axis + 3):
                        
                    if rotation > 3:
                        rotation -= 3
                        
                    acount = self.__getCount(x, y, dx[axis], dy[axis], type)
                    rcount = self.__getCount(x, y, dx[rotation], dy[rotation], type)
                    
                    if ((acount == 2 and rcount == 3) or
                        (acount == 3 and rcount == 2) or
                        (acount == 3 and rcount == 3)):
                        return True
    
    def __check(self, x, y, type):
        dx = [0, 1, 1, 1];
        dy = [1, 1, 0, -1];
        for i in range(0, 4):
            if self.__getCount(x, y, dx[i], dy[i], type) == 4:
                return True
            
    def __getCount(self, x, y, dx, dy, type):
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
        return count
                    
    def setViewer(self, viewer):
        self.viewer = viewer
        
    def showMap(self):
        s = ""
        for y in range(0, self.length):
            for x in range(0, self.length):
                s += str("{0:>4d}".format(self.map[x][y]))
            s += "\n"
        print(s)