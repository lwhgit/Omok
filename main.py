from Omok.Omok import Omok
import time

def main():
    omok = Omok(15, 30)
    
    print(omok.putStone(0, 0, 1))
    time.sleep(0.5)
    print(omok.putStone(0, 1, 1))
    time.sleep(0.5)
    print(omok.putStone(0, 2, 1))
    time.sleep(0.5)
    print(omok.putStone(0, 3, 1))
    time.sleep(0.5)
    print(omok.putStone(0, 4, 1))
    time.sleep(0.5)
    
    while True:
        eval(input())
    
main()