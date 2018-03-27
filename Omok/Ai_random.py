import random

class Ai_random:
    #check = None
    length = 0
    type = 0
    omok = None
    map = None

    def __init__(self, omok, length, t):
        self.length = length
        self.type = t
        self.omok = omok
    
    def put(self):
        while(True):
            x = random.randrange(0, self.length)
            y = random.randrange(0, self.length)
            if (self.omok.isPossable(x, y, self.type)):
                return self.omok.putStone(x, y, self.type)
            num = 0
            for i in range(0, self.length):
                for j in range(0, self.length):
                    if (self.omok.isPossable(i, j, self.type)):
                        num += 1
            if (num == 0):
                return -1

              