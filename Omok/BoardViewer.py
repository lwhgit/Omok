from tkinter import *
from tkinter import messagebox
import threading

class BoardViewer:
    __length = 0
    __size = 0
    __root = None
    __canvas = None
    __thread = None
    
    def __init__(self, length, size):
        self.__length = length
        self.__size = size
        
        self.thread = threading.Thread(target = self.__show)
        self.thread.start()
        
        while True:
            if self.__canvas != None:
                break
        
    def __show(self):
        self.__initWindow()
        self.__initBoard()
        
    def __initWindow(self):
        self.__root = Tk()
        self.__root.title("Omok")
        self.__root.geometry(str((self.__size * (self.__length + 1)) + 150) + "x" + str(self.__size * (self.__length + 1)))
        self.__root.resizable(0, 0)
        self.__initBoard()
        self.__initWidget()
        self.__root.protocol("WM_DELETE_WINDOW", self.__wmDelWin)
        self.__root.mainloop()
    
    def __initBoard(self):
        try:
            dotSize = self.__size / 10
            
            if self.__canvas == None:
                self.__canvas = Canvas(self.__root, width = self.__size * (self.__length + 1), height = self.__size * (self.__length + 1), bg = "#FFDE7D")
            else:
                self.__canvas.create_rectangle(0, 0, self.__size * (self.__length + 2), self.__size * (self.__length + 2), fill = "#FFDE7D")
                
            for i in range(0, self.__length):
                self.__canvas.create_line(self.__size,                  self.__size + self.__size * i,  self.__size * self.__length,    self.__size + self.__size * i,  fill = "black", tag = "line")
                self.__canvas.create_line(self.__size + self.__size * i,  self.__size * self.__length,    self.__size + self.__size * i,  self.__size,                  fill = "black", tag = "line")
                
                if self.__length >= 7:
                    self.__canvas.create_oval(self.__size * 4 - dotSize,                  self.__size * 4 - dotSize,                  self.__size * 4 + dotSize,                  self.__size * 4 + dotSize,                  fill = "black")
                    self.__canvas.create_oval(self.__size * 4 - dotSize,                  self.__size * (self.__length - 3) - dotSize,  self.__size * 4 + dotSize,                  self.__size * (self.__length - 3) + dotSize,  fill = "black")
                    self.__canvas.create_oval(self.__size * (self.__length - 3) - dotSize,  self.__size * 4 - dotSize,                  self.__size * (self.__length - 3) + dotSize,  self.__size * 4 + dotSize,                  fill = "black")
                    self.__canvas.create_oval(self.__size * (self.__length - 3) - dotSize,  self.__size * (self.__length - 3) - dotSize,  self.__size * (self.__length - 3) + dotSize,  self.__size * (self.__length - 3) + dotSize,  fill = "black")
                    
                if self.__length % 2 == 1:
                    self.__canvas.create_oval(self.__size * (self.__length / 2 + 0.5) - dotSize,  self.__size * (self.__length / 2 + 0.5) - dotSize,  self.__size * (self.__length / 2 + 0.5) + dotSize,  self.__size * (self.__length / 2 + 0.5) + dotSize,  fill = "black")
                    
                    if self.__length >= 13:
                        self.__canvas.create_oval(self.__size * (self.__length / 2 + 0.5) - dotSize,  self.__size * 4 - dotSize,  self.__size * (self.__length / 2 + 0.5) + dotSize,  self.__size * 4 + dotSize,  fill = "black")
                        self.__canvas.create_oval(self.__size * 4 - dotSize,  self.__size * (self.__length / 2 + 0.5) - dotSize,  self.__size * 4 + dotSize,  self.__size * (self.__length / 2 + 0.5) + dotSize,  fill = "black")
                        self.__canvas.create_oval(self.__size * (self.__length / 2 + 0.5) - dotSize,  self.__size * (self.__length - 3) - dotSize,  self.__size * (self.__length / 2 + 0.5) + dotSize,  self.__size * (self.__length - 3) + dotSize,  fill = "black")
                        self.__canvas.create_oval(self.__size * (self.__length - 3) - dotSize,  self.__size * (self.__length / 2 + 0.5) - dotSize,  self.__size * (self.__length - 3) + dotSize,  self.__size * (self.__length / 2 + 0.5) + dotSize,  fill = "black")
                        
            self.__canvas.pack(side = "left")
        except:
            pass
        
    def __initWidget(self):
        hideBtn = Button(self.__root, text = "HIDE", command = self.__hideWindow)
        hideBtn.config(width = 15, height = 5)
        #hideBtn.place(x = self.__size * (self.__length + 1), y = 0)
        hideBtn.pack()
    
    def __wmDelWin(self):
        self.__root.quit()
        threading.Event().set()
        
    def __hideWindow(self):
        self.__root.withdraw()
        
    def showWindow(self):
        self.__root.deiconify()
        
    def reset(self):
        self.__initBoard()
        
    def putStone(self, x, y, type):
        if type == 1000:
            self.__canvas.create_oval(self.__size * x - self.__size / 2,  self.__size * y - self.__size / 2,  self.__size * x + self.__size / 2,  self.__size * y + self.__size / 2,  fill = "black")
        elif type == 2000:
            self.__canvas.create_oval(self.__size * x - self.__size / 2,  self.__size * y - self.__size / 2,  self.__size * x + self.__size / 2,  self.__size * y + self.__size / 2,  fill = "white")
            
    def bind(self, eventName, func):
        self.__canvas.bind(eventName, func)
        
    def showinfo(self, title, context):
        messagebox.showinfo(title, context)