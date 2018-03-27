from tkinter import *

class BoardViewer:
    size = 0
    length = 0
    root = None
    canvas = None
    frame = None
    
    def __init__(self, length = 15, size = 40):
        self.size = size
        self.length = length
        self.root = Tk()
        self.root.title("Omok")
        self.root.geometry(str(self.size * (self.length + 1)) + "x" + str(self.size * (self.length + 1)))
        self.root.resizable(0, 0)
        self.frame = Frame(self.root)
        self.frame.pack()
        self.__initBoard()
        
    def __initBoard(self):
        dotSize = self.size / 10
        
        if self.canvas == None:
            self.canvas = Canvas(self.frame, width = self.size * (self.length + 1), height = self.size * (self.length + 1), bg = "#FFDE7D")
        else:
            self.canvas.create_rectangle(0, 0, self.size * (self.length + 2), self.size * (self.length + 2), fill = "#FFDE7D")
            
        for i in range(0, self.length):
            self.canvas.create_line(self.size,                  self.size + self.size * i,  self.size * self.length,    self.size + self.size * i,  fill = "black", tag = "line")
            self.canvas.create_line(self.size + self.size * i,  self.size * self.length,    self.size + self.size * i,  self.size,                  fill = "black", tag = "line")
            
            if self.length >= 7:
                self.canvas.create_oval(self.size * 4 - dotSize,                  self.size * 4 - dotSize,                  self.size * 4 + dotSize,                  self.size * 4 + dotSize,                  fill = "black")
                self.canvas.create_oval(self.size * 4 - dotSize,                  self.size * (self.length - 3) - dotSize,  self.size * 4 + dotSize,                  self.size * (self.length - 3) + dotSize,  fill = "black")
                self.canvas.create_oval(self.size * (self.length - 3) - dotSize,  self.size * 4 - dotSize,                  self.size * (self.length - 3) + dotSize,  self.size * 4 + dotSize,                  fill = "black")
                self.canvas.create_oval(self.size * (self.length - 3) - dotSize,  self.size * (self.length - 3) - dotSize,  self.size * (self.length - 3) + dotSize,  self.size * (self.length - 3) + dotSize,  fill = "black")
                
            if self.length % 2 == 1:
                self.canvas.create_oval(self.size * (self.length / 2 + 0.5) - dotSize,  self.size * (self.length / 2 + 0.5) - dotSize,  self.size * (self.length / 2 + 0.5) + dotSize,  self.size * (self.length / 2 + 0.5) + dotSize,  fill = "black")
                
                if self.length >= 13:
                    self.canvas.create_oval(self.size * (self.length / 2 + 0.5) - dotSize,  self.size * 4 - dotSize,  self.size * (self.length / 2 + 0.5) + dotSize,  self.size * 4 + dotSize,  fill = "black")
                    self.canvas.create_oval(self.size * 4 - dotSize,  self.size * (self.length / 2 + 0.5) - dotSize,  self.size * 4 + dotSize,  self.size * (self.length / 2 + 0.5) + dotSize,  fill = "black")
                    self.canvas.create_oval(self.size * (self.length / 2 + 0.5) - dotSize,  self.size * (self.length - 3) - dotSize,  self.size * (self.length / 2 + 0.5) + dotSize,  self.size * (self.length - 3) + dotSize,  fill = "black")
                    self.canvas.create_oval(self.size * (self.length - 3) - dotSize,  self.size * (self.length / 2 + 0.5) - dotSize,  self.size * (self.length - 3) + dotSize,  self.size * (self.length / 2 + 0.5) + dotSize,  fill = "black")
                    
        self.canvas.pack()
        
    def putStone(self, x, y, type):
        if type == 1:
            self.canvas.create_oval(self.size * x - self.size / 2,  self.size * y - self.size / 2,  self.size * x + self.size / 2,  self.size * y + self.size / 2,  fill = "black")
        elif type == 2:
            self.canvas.create_oval(self.size * x - self.size / 2,  self.size * y - self.size / 2,  self.size * x + self.size / 2,  self.size * y + self.size / 2,  fill = "white")
            
    def show(self):
        self.root.mainloop()
        
    def setEvent(self, eventName, callback):
        self.canvas.bind(eventName, callback)
        
    def reset(self):
        self.__initBoard()
        