from Omok.Omok import *
import numpy as np
from AI.AI import *
from tkinter import messagebox

#상수 선언
SIZE = 40
LENGTH = 15

BLACK = 1
WHITE = 2

def main():

    print("1. 인공지능 자기 학습(GUI X)\n2. 인공지능 자기 학습(GUI O)\n3. 인공지능(흑) vs. 인간(백) 모드\n4. 종료")
    select = int(input('입력 : '))
    if (select == 1):
        omok = Omok(LENGTH)
    elif (select == 2 or select == 3):
        omok = Omok(LENGTH, SIZE)
    else:
        return


    config = {
        'board' : omok,
        'epsilonStart' : 1,
        'epsilonDiscount' : 0.999,
        'epsilonMinimumValue' : 0.1,
        'learningRate' : 0.001,
        'batchSize' : 50,
        'gridSize' : LENGTH,
        'epoch' : 100,
        'nHidden' : 1024,
        'maxMemory' : 2048,
        'fileName' : '/fileDeep.ckpt',
        'winReward' : 1,
        'dropoutRate' : 0.8,
        'dropoutHiddenRate' : 0.5,
        'type' : BLACK,
        'discount' : 0.9
        }
    ai = OmokDQN(config)

    if (select == 1 or select == 2):
        ai.trainModel_vsSelf()
    elif (select == 3):
        ai.playGame()

main()
