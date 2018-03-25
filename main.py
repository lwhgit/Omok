import Omok
import time

def main():
    omok = Omok.Omok(40, 15)
    print(omok.putStone(5, 5, 1))
    time.sleep(0.5)
    print(omok.putStone(5, 6, 1))
    time.sleep(0.5)
    print(omok.putStone(5, 7, 1))
    time.sleep(0.5)
    print(omok.putStone(6, 8, 1))
    time.sleep(0.5)
    print(omok.putStone(7, 8, 1))
    time.sleep(0.5)
    print(omok.putStone(8, 8, 1))
    time.sleep(0.5)
    print(omok.putStone(5, 8, 1))
    time.sleep(0.5)
    print(omok.isPossable(5, 5 ,1))
    print(omok.isPossable(5, 6 ,1))
    print(omok.isPossable(5, 10 ,1))
    
main()