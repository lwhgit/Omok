from OmokBoard import *
from BoardViewer import *
import threading

class Omok:
    size = 0
    length = 0
    OmokBoard = None
    boardViewer = None

    def __init__(self, size = 40, length = 15):
        self.size = size
        self.length = length
        self.initOmokBoard()
        self.initBoardViewer()
        
    def __thread(self):
        self.boardViewer = BoardViewer(self.size, self.length)
        self.boardViewer.show()

    def initOmokBoard(self):
        threading.Thread(target = self.__thread).start()
        
    def initBoardViewer(self):
        self.OmokBoard = OmokBoard(self.length)
        while True:
            if self.boardViewer != None:
                break
        self.OmokBoard.setViewer(self.boardViewer)
        
    def putStone(self, x, y, type):
        self.OmokBoard.putStone(x, y, type)
        