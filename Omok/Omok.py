from .BoardViewer import BoardViewer
from .OmokBoard import OmokBoard

class Omok:
    __length = 0
    __size = 0
    __boardViewer = None
    __omokBoard = None
    __clickState = -3
    __clickType = 0
    
    def __init__(self, length = 15, size = -1):
        self.__length = length
        self.__size = size
        if self.__size != -1:
            self.__initBoardViewer()
            self.__boardViewer.bind("<Button-1>", self.__put)
            #self.__boardViewer.bind("<Button-1>", self.__putBlack)
            #self.__boardViewer.bind("<Button-3>", self.__putWhite)
        self.__initOmokBoard()
        
    def __initBoardViewer(self):
        self.__boardViewer = BoardViewer(self.__length, self.__size)
        
    def __initOmokBoard(self):
        self.__omokBoard = OmokBoard(self.__length)
        
    def __putBlack(self, event):
        if self.__clickState == -2:
            self.__clickState = self.putStone(int(event.x / self.__size - 0.5), int(event.y / self.__size - 0.5), 1)
        
    def __putWhite(self, event):
        if self.__clickState == -2:
            self.__clickState = self.putStone(int(event.x / self.__size - 0.5), int(event.y / self.__size - 0.5), 2)
            
    def __put(self, event):
        if self.__clickState == -2:
            self.__clickState = self.putStone(int(event.x / self.__size - 0.5), int(event.y / self.__size - 0.5), self.__clickType)
            
            #if self.__clickState != -1:
            #    DataShower.showArray(self.__omokBoard.getShape(int(event.x / self.__size - 0.5), int(event.y / self.__size - 0.5), self.__clickType))
        
    def putStone(self, x, y, type):
        if self.isPossable(x, y, type):
            if self.__boardViewer != None:
                self.__boardViewer.putStone(x + 1, y + 1, type)
            return self.__omokBoard.putStone(x, y, type)
        else:
            return -1
        
    def isPossable(self, x, y, type):
        return not (self.__omokBoard.isImpossable(x, y, type))
        
    def getMap(self):
        return self.__omokBoard.getMap()
        
    def showMap(self):
        self.__omokBoard.showMap()
        
    def reset(self):
        self.__omokBoard.reset()
        if self.__boardViewer != None:
            self.__boardViewer.reset()
        
    def get3DArray(self):
        return self.__omokBoard.get3DArray()
        
    def userInput(self, type):
        self.__clickState = -2
        self.__clickType = type
        while True:
            if self.__clickState != -2:
                break
        return self.__clickState
        
    def showinfo(self, title, context):
        self.__boardViewer.showinfo(title, context)
        
    def showWindow(self):
        self.__boardViewer.showWindow()
        
    def getAroundCount(self, x, y, type):
        return self.__omokBoard.getAroundCount(x, y, type)
        
    def getShape(self, x, y, type):
        return self.__omokBoard.getShape(x, y, type)