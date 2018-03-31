from Omok.Omok import Omok
from Util.DataShower import DataShower
import time
import sys

def main():
    omok = Omok(15, 30)
    #omok.showinfo("asd", "asdasd")
    
    while True:
        #print("Your turn")
        print(omok.userInput(1))
        DataShower.showArray(omok.getShape(5, 5, 1))
        #time.sleep(1)
    
    while True:
        eval(input())
    
    
main()