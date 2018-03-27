from Omok.Omok import Omok
from AI.Ai_random import *
import time
from AI.Ai_cnn import *

#상수 선언
SIZE = 40
LENGTH = 15

BLACK = 1
WHITE = 2

def main():
    omok = Omok.Omok.Omok(LENGTH, SIZE)
    ai1 = Ai_random(omok, LENGTH, BLACK)
    ai2 = Ai_random(omok, LENGTH, WHITE)
    while(True):
        a1 = ai1.put()
        if (a1 == 0):
            pass
        elif (a1 == -1):
            print("무승부")
            break
        else:
            print("BLACK WIN")
            break
        a2 = ai2.put()
        if (a2 == 0):
            pass
        elif (a2 == -1):
            print("무승부")
            break
        else:
            print("WHITE WIN")
            break
    '''ai1 = Ai_random.Ai_random(omok, LENGTH, WHITE)
    ai2 = Ai_cnn.Ai_cnn(BLACK)
    ai2.trainModel(ai1)'''
main()
