from Omok.Omok import Omok
import time

def main():
    omok = Omok(15, 30)
    
    while True:
        print("a")
        print(omok.userInput())
        time.sleep(3)
    
    '''while True:
        eval(input())'''
    
main()