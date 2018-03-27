from Omok.Omok import Omok
import time

omok = None
a = 30
def main():
    global omok
    omok = Omok(15, a)
    omok.setEvent("<Button-1>", black)
    omok.setEvent("<Button-2>", func)
    omok.setEvent("<Button-3>", white)
    
    while True:
        eval(input())
    #omok.setEvent("<r>", key)
    
def black(event):
    print(int(event.x / a- 0.5), int(event.y / a- 0.5))
    print(omok.putStone(int(event.x / a- 0.5), int(event.y /a - 0.5), 1))
    
def white(event):
    print(omok.putStone(int(event.x / a- 0.5), int(event.y /a- 0.5), 2))
    
def func(event):
    print("reset")
    arr = omok.get3DArray()
    showArr(arr[0])
    showArr(arr[1])
    showArr(arr[2])

def showArr(arr):
    s = ""
    for y in range(0, 15):
        for x in range(0, 15):
            s += str("{0:>4d}".format(arr[x][y]))
        s += "\n"
    print(s)

main()