import tensorflow as tf
import os
import random
import math
import numpy as np
import tkinter.messagebox
#AVX 경고 무시
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#-------------------------------#
#           변수 설정           #
#-------------------------------#
epsilon = 1  # 무작위 액션 선택할 확률
epsilonMinimumValue = 0.1  # 입실론 최솟값
epsilonDiscount = 0.999  # 입실론 줄어드는 정도(공비)
gridSize = 15  # 판의 격자수
epoch = 100  # 시스템이 작동할 떄 한번에 실행할 횟수
nHidden = 1024  # 히든 레이어의 개수
nAction = gridSize * gridSize  # Action의 개수
nState = gridSize * gridSize  # 가능한 상태의 개수
maxMemory = 2048  # 경험을 저장할 메모리의 최대 개수
learningRate = 0.01  # 학습 정도
fileName = "/fileDeep.ckpt"  # Model을 저장할 파일 이름
batchSize = 64  # mini batch할 정도
NONE = 0
BLACK = 1000
WHITE = 2000
ERROR = -1000
DropoutRate = tf.placeholder(tf.float32)
DropoutHiddenRate = tf.placeholder(tf.float32)

def MakeConv(image, inChannelNumber, outChannelNumber, sizeFilter, nStddev):
    w_conv = tf.Variable(tf.random_normal([sizeFilter, sizeFilter, inChannelNumber, outChannelNumber], stddev = nStddev))
    h_conv = tf.nn.conv2d(image, w_conv, strides = [1, 1, 1, 1], padding = 'SAME')
    b_conv = tf.Variable(tf.constant(0.1, shape = [outChannelNumber]))
    R_conv = tf.nn.relu(h_conv + b_conv)
    return tf.nn.max_pool(R_conv, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = 'SAME')

nFilter1 = 32
sizeFilter1 = 6
channelFilter1 = 1
X = tf.placeholder(tf.float32, [None, nState])
xImage = tf.reshape(X, [-1, gridSize, gridSize, channelFilter1])
P_conv1 = MakeConv(xImage, channelFilter1, nFilter1, sizeFilter1, 0.01)
P_conv1 = tf.nn.dropout(P_conv1, DropoutRate)

nFilter2 = 64
sizeFilter2 = 6
P_conv2 = MakeConv(P_conv1, nFilter1, nFilter2, sizeFilter2, 0.01)
#Fully connected net
lastPool = P_conv2
nLastFilter = nFilter2
units1_num = nLastFilter * round(gridSize / 4) * round(gridSize / 4)

lastPool = tf.reshape(lastPool, [-1, units1_num])
w2 = tf.Variable(tf.random_normal([units1_num, nHidden]))
b2 = tf.Variable(tf.constant(0.1, shape = [nHidden]))
hidden = tf.nn.relu(tf.matmul(lastPool, w2) + b2)
hidden = tf.nn.dropout(hidden, DropoutHiddenRate)
w0 = tf.Variable(tf.zeros([nHidden, nAction]))
b0 = tf.Variable(tf.zeros([nAction]))
output_layer = tf.matmul(hidden, w0) + b0

Y = tf.placeholder(tf.float32, [None, nAction])
cost = tf.reduce_mean(tf.square(Y - output_layer)) / (2 * batchSize)
optimizer = tf.train.AdamOptimizer(learningRate).minimize(cost)


class OmokDQN:
    def __init__(self, config):
        self.omok = config['board']
        self.epsilonStart = config['epsilonStart']
        self.epsilonDiscount = config['epsilonDiscount']
        self.epsilonMinimumValue = config['epsilonMinimumValue']
        self.learningRate = config['learningRate']
        self.batchSize = config['batchSize']
        self.gridSize = config['gridSize']
        self.epoch = config.get('epoch')
        self.nHidden = config['nHidden']
        self.maxMemory = config['maxMemory']
        self.fileName = config['fileName']
        self.winReward = config['winReward']
        self.dropoutRate = config['dropoutRate']
        self.dropoutHiddenRate = config['dropoutHiddenRate']
        self.nAction = self.gridSize * self.gridSize
        self.nState = self.gridSize * self.gridSize
        self.type = config['type']
        self.discount = config['discount']
        self.bonusReward = config['bonusReward']

    def getActionRandom(self):
        while(True):
            action = random.randrange(0, self.nAction)
            x = int(action % self.gridSize)
            y = int(action / self.gridSize)
            if (self.omok.isPossable(x, y, self.type)):
                return action

    def getAction_DQN(self, sess):
        state = self.getState(BLACK, 0)
        print(state)
        q = sess.run(output_layer, feed_dict = {X: state, DropoutRate:1, DropoutHiddenRate:1})
        while(True):
            action = q.argmax()
            print(q)
            x = int(action % self.gridSize)
            y = int(action / self.gridSize)
            if (self.omok.isPossable(x, y, self.type)):
                return action
            else:
                q[0, action] = -99999

    def getState(self, currentType, nRotate):
        map = self.omok.getMap()
        for d in range(0, nRotate):
            t = np.zeros((self.gridSize, self.gridSize))
            for i in range(0, self.gridSize):
                for j in range(0, self.gridSize):
                    t[self.gridSize - j - 1][i] = map[i][j]
            map = t[:]

        state = np.reshape(map, (1, -1))
        if (currentType != self.type):
            tempState = state.copy()
            for i in range(self.nState):
                if(tempState[0, i] == BLACK):
                    tempState[0, i] = WHITE
                elif(tempState[0, i] == WHITE):
                    tempState[0, i] = BLACK
            state = tempState

        return state

    def trainModel_vsSelf(self):
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        
        saver = tf.train.Saver()
        
        if(os.path.isfile(os.getcwd() + self.fileName + ".index") == True):
            saver.restore(sess, os.getcwd() + self.fileName)
            print("모델을 성공적으로 불러왔습니다.")

        trainNumber = 0
        print("trainModel_vsSelf를 실행중입니다. 현재 훈련 횟수는 ", str(trainNumber), " 입니다.")

        while(True):
            trainNumber += 1
            epsilon = self.epsilonStart
            memory = replayMemory(self.gridSize, self.maxMemory, self.discount, self.dropoutRate, self.dropoutHiddenRate)
            for i in range(0, self.epoch):
                self.omok.reset()
                currentState = np.empty((4, self.gridSize * self.gridSize))
                nextState = np.empty((4, self.gridSize * self.gridSize))
                err = 0
                gameOver = False
                interaction = 0
                currentPlayer = BLACK
                #startTime = int(tt.gmtime())
                while(gameOver != True):
                    action = -9999
                    reward = 0
                    if(random.uniform(0, 1.0) <= epsilon):
                        action = self.getActionRandom()
                    else:
                        action = self.getAction_DQN(sess)
                    
                    if (epsilon > self.epsilonMinimumValue):
                        epsilon *= self.epsilonDiscount
                    
                    x = int(action % self.gridSize)
                    y = int(action / self.gridSize)

                    currentState = self.getState(currentPlayer, 0)
                    
                    aroundCount = self.omok.getAroundCount(x, y, currentPlayer)
                    reward += self.bonusReward * aroundCount
                    
                    result = self.omok.putStone(x, y, currentPlayer)

                    nextState= self.getState(currentPlayer, 0)

                    if (currentPlayer == result):
                        reward += 1

                    interaction +=1
                    if (result == BLACK):
                        gameOver = True
                        print("흑이 승리했습니다.       놓아진 바둑돌의 수 : ", str(interaction))
                    
                    if (result == WHITE):
                        gameOver = True
                        print("백이 승리했습니다.       놓아진 바둑돌의 수 : ", str(interaction))

                    memory.remember(currentState, action, reward, nextState, gameOver)

                    inputs, targets = memory.getBatch(output_layer, self.batchSize, self.winReward, sess)

                    _t, loss = sess.run([optimizer, cost], feed_dict = {X: inputs, Y: targets, DropoutRate:self.dropoutRate, DropoutHiddenRate:self.dropoutHiddenRate})
                    err += loss
                    if (interaction >= self.gridSize * self.gridSize):
                        print("무승부입니다.            놓아진 바둑돌의 수 : ", str(interaction))
                        break
                    if(currentPlayer == BLACK):
                        currentPlayer = WHITE
                    else:
                        currentPlayer = BLACK
                #print("걸린 시간 : " + str(int(tt.gmtime()+startTime)))
            print("trainModel_vsSelf를 실행중입니다. 현재 훈련 횟수는 ", str(trainNumber), " 입니다. 오류값은 ", str(err), " 입니다")
            save_path = saver.save(sess, os.getcwd() + self.fileName)
            print("모델이 다음 위치에 성공적으로 저장되었습니다 : " + save_path)

    def randPut(self):
        while(True):
            x = random.randrange(0, self.gridSize)
            y = random.randrange(0, self.gridSize)
            if (self.omok.isPossable(x, y, BLACK)):
                return self.omok.putStone(x, y, BLACK)

    def trainModel_vsRand(self):
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        
        saver = tf.train.Saver()
        
        if(os.path.isfile(os.getcwd() + self.fileName + ".index") == True):
            saver.restore(sess, os.getcwd() + self.fileName)
            print("모델을 성공적으로 불러왔습니다.")

        trainNumber = 0
        print("trainModel_vsRand를 실행중입니다. 현재 훈련 횟수는 ", str(trainNumber), " 입니다.")

        while(True):
            trainNumber += 1
            epsilon = self.epsilonStart
            memory = replayMemory(self.gridSize, self.maxMemory, self.discount, self.dropoutRate, self.dropoutHiddenRate)
            winCount = 0
            for i in range(0, self.epoch):
                self.omok.reset()
                currentState = np.empty((4, self.gridSize * self.gridSize))
                nextState = np.empty((4, self.gridSize * self.gridSize))
                err = 0
                gameOver = False
                interaction = 0
                currentPlayer = WHITE
                #startTime = int(tt.gmtime())
                while(gameOver != True):
                    action = -9999
                    reward = 0
                    if(random.uniform(0, 1.0) <= epsilon):
                        action = self.getActionRandom()
                    else:
                        action = self.getAction_DQN(sess)
                    
                    if (epsilon > self.epsilonMinimumValue):
                        epsilon *= self.epsilonDiscount
                    
                    x = int(action % self.gridSize)
                    y = int(action / self.gridSize)

                    if (interaction == 0):
                        result = self.omok.putStone(int(self.gridSize / 2), int(self.gridSize / 2), BLACK)
                    else:
                        result = self.randPut()

                    if (result == BLACK):
                        gameOver = True
                        print("흑(랜덤착수)이 승리했습니다.       놓아진 바둑돌의 수 : ", str(interaction))
                        break

                    currentState = self.getState(currentPlayer, 0)
                    
                    aroundCount = self.omok.getAroundCount(x, y, currentPlayer)
                    reward += self.bonusReward * aroundCount
                    
                    result = self.omok.putStone(x, y, currentPlayer)

                    nextState= self.getState(currentPlayer, 0)

                    interaction +=2
                    
                    if (result == WHITE):
                        gameOver = True
                        print("백(인공지능)이 승리했습니다.       놓아진 바둑돌의 수 : ", str(interaction))
                        winCount += 1
                        reward = self.winReward

                    if (interaction >= self.gridSize * self.gridSize):
                        print("무승부입니다.            놓아진 바둑돌의 수 : ", str(interaction))
                        break
                    memory.remember(currentState, action, reward, nextState, gameOver)

                    inputs, targets = memory.getBatch(output_layer, self.batchSize, self.winReward, sess)

                    _t, loss = sess.run([optimizer, cost], feed_dict = {X: inputs, Y: targets, DropoutRate:self.dropoutRate, DropoutHiddenRate:self.dropoutHiddenRate})
                    err += loss
            print("trainModel_vsSelf를 실행중입니다. 현재 훈련 횟수는 ", str(trainNumber), " 입니다. 오류값은 ", str(err), " 입니다. 인공지능의 승률은 ", str(int(winCount / self.epoch * 100)) , "% 입니다.")
            save_path = saver.save(sess, os.getcwd() + self.fileName)
            print("모델이 다음 위치에 성공적으로 저장되었습니다 : " + save_path)

    def playGame(self):
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        
        saver = tf.train.Saver()
        
        if(os.path.isfile(os.getcwd() + self.fileName + ".index") == True):
            saver.restore(sess, os.getcwd() + self.fileName)
            print("모델을 성공적으로 불러왔습니다.")
        while(True):
            while(True):
                result = self.omok.userInput(BLACK)
                if(result != -1000): break
            if (result == BLACK):
                print("당신은 승리했다")
                return
            action = self.getAction_DQN(sess)
            x = int(action % self.gridSize)
            y = int(action / self.gridSize)
            result = self.omok.putStone(x, y, self.type)
            if (result == self.type):
                print("당신은 패배했다")
                return
            


class replayMemory:
    def __init__(self, gridSize, maxMemory, discount, dropoutRate, dropoutHiddenRate):
        self.maxMemory = maxMemory
        self.gridSize = gridSize
        self.nState = gridSize * gridSize
        self.nAction = gridSize * gridSize
        self.discount = discount
        self.dropoutRate = dropoutRate
        self.dropoutHiddenRate = dropoutHiddenRate

        self.inputState = np.empty((self.maxMemory, self.nState))
        self.actions = np.zeros(self.maxMemory)
        self.nextState = np.empty((self.maxMemory, self.nState))
        self.gameOver = np.empty((self.maxMemory), dtype = np.bool)
        self.rewards = np.empty((self.maxMemory))
        self.count = 0
        self.current = 0

    def remember(self, currentState, action, reward, nextState, gameOver):
        self.actions[self.current] = action
        self.rewards[self.current] = reward
        self.inputState[self.current, ...] = currentState
        self.nextState[self.current, ...] = nextState
        self.gameOver[self.current] = gameOver
        self.count = max(self.count, self.current + 1)
        self.current = (self.current + 1) % self.maxMemory

    def getBatch(self, model, batchSize, winReward, sess):
        memoryLength = self.count
        chosenBatchSize = min(batchSize, memoryLength)

        inputs = np.zeros((chosenBatchSize, self.nState))
        targets = np.zeros((chosenBatchSize, self.nAction))

        for i in range(0, chosenBatchSize):
            randomIndex = random.randrange(0, memoryLength)
            current_inputState = np.reshape(self.inputState[randomIndex], (1, self.nState))

            target = sess.run(model, feed_dict = {X: current_inputState, DropoutRate: self.dropoutRate, DropoutHiddenRate: self.dropoutHiddenRate})

            current_nextState = np.reshape(self.inputState[randomIndex], (1, self.nState))
            current_output = sess.run(model, feed_dict = {X: current_nextState, DropoutRate:self.dropoutRate, DropoutHiddenRate:self.dropoutHiddenRate})

            nextStateMaxQ = np.amax(current_output)

            if(nextStateMaxQ > winReward):
                nextStateMaxQ = winReward
            if(self.gameOver[randomIndex] == True):
                target[0, [int(self.actions[randomIndex])]] = self.rewards[randomIndex]
            else:
                target[0, [int(self.actions[randomIndex])]] = self.rewards[randomIndex] + self.discount * nextStateMaxQ
            inputs[i] = current_inputState
            targets[i] = target
        return inputs, targets

