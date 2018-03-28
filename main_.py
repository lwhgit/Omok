from Omok.Omok import *
from AI.Ai_random import *
import time
from AI.Ai_cnn import *

#상수 선언
SIZE = 40
LENGTH = 15

BLACK = 1
WHITE = 2

def main():
    print(int(15 / 2 / 2))
    omok = Omok(LENGTH)
    ai1 = Ai_random(omok, LENGTH, WHITE)
    ai2 = Ai_cnn(BLACK)
    ai2.trainModel(ai1, omok)
main()
