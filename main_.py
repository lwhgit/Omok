from Omok.Omok import *
import numpy as np
from AI.AI import *
from tkinter import messagebox

#상수 선언
SIZE = 40
LENGTH = 15

BLACK = 1000
WHITE = 2000

def main():

    print("1. 인공지능 vs. 랜덤 학습(GUI X)\n2. 인공지능 vs. 랜덤 학습(GUI O)\n3. 인공지능(백) vs. 인간(흑) 모드\n4. 종료")
    select = int(input('입력 : '))
    if (select == 1):
        omok = Omok(LENGTH)
    elif (select == 2 or select == 3):
        omok = Omok(LENGTH, SIZE)
    else:
        return


    config = {
        'board' : omok,
        'epsilonStart' : 0,
        'epsilonDiscount' : 0.999,
        'epsilonMinimumValue' : 0.1,
        'learningRate' : 0.01,
        'batchSize' : 64,
        'gridSize' : LENGTH,
        'epoch' : 100,
        'nHidden' : 1024,
        'maxMemory' : 2048,
        'fileName' : '/fileDeep.ckpt',
        'winReward' : 1,
        'dropoutRate' : 0.8,
        'dropoutHiddenRate' : 0.7,
        'type' : WHITE,
        'discount' : 0.9,
        'bonusReward' : 0.02
        
        }
    ai = OmokDQN(config)

    if (select == 1 or select == 2):
        ai.trainModel_vsRand()
    elif (select == 3):
        ai.playGame()

main()
