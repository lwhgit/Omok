from tkinter import *

class BoardViewer:
    size = 0
    length = 0
    root = None
    canvas = None
    
    def __init__(self, size = 40, length = 15):
        self.size = size
        self.length = length
        self.root = Tk()
        self.root.title("Omok")
        self.root.geometry(str(self.size * (self.length + 1)) + "x" + str(self.size * (self.length + 1)))
        self.__initBoard()
     
        
    def __initBoard(self):
        dotSize = self.size / 10
        self.canvas = Canvas(self.root, width = self.size * (self.length + 1), height = self.size * (self.length + 1), bg = "#FFDE7D")
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
        