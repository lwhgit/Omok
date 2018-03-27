from .OmokBoard import *
from .BoardViewer import *
import threading

class Omok:
    size = 0
    length = 0
    omokBoard = None
    boardViewer = None

    def __init__(self, length = 15, size = -1):
        self.size = size
        self.length = length
        if size != -1:
            self.initBoardViewer()
        self.initOmokBoard()
        
    def __thread(self):
        self.boardViewer = BoardViewer(self.length, self.size)
        self.boardViewer.show()

    def initBoardViewer(self):
        threading.Thread(target = self.__thread).start()
        
    def initOmokBoard(self):
        self.omokBoard = OmokBoard(self.length)
        if self.size != -1:
            while True:
                if self.boardViewer != None:
                    break
                    
            self.omokBoard.setViewer(self.boardViewer)
        
    def putStone(self, x, y, type):
        return self.omokBoard.putStone(x, y, type)
        
    def isPossable(self, x, y, type):
        return not (self.omokBoard.isImpossable(x, y, type))
        
    def getMap(self):
        return self.omokBoard.map
        
    def showMap(self):
        self.omokBoard.showMap()
        
    def setEvent(self, eventName, callback):
        if self.boardViewer != None:
            self.boardViewer.setEvent(eventName, callback)
            
    def reset(self):
        self.omokBoard.reset()
        self.boardViewer.reset()
        
    def get3DArray(self):
        return self.omokBoard.get3DArray()
        