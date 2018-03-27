import tensorflow as tf
import os
import random
import math
import numpy as np
import Omok
import Ai_random

#AVX 경고 무시
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#-------------------------------------------------------------------------#
# https://github.com/deepseasw/OmokQLearning/blob/master/OmokTrainDeep.py #
# 를 많이 참조하여 만들었음, 아직 미완성, 수정중임                        #
#-------------------------------------------------------------------------#

#-------------------------------#
#           변수 설정           #
#-------------------------------#

gridSize = 15
NONE = 0
BLACK = 1
WHITE = 2
ERROR = -1
nAction = gridSize * gridSize
nState = gridSize * gridSize
dropoutRate = 0.8   #Dropout되는 정도
dropoutHiddonRate = 0.5 #FC에서 Dropout되는 정도
learningRate = 0.0001
nHidden = 625
nameFile = "fileDeep.ckpt.index"
winReward = 1
epsilonMinimumValue = 0.1
epsilonDiscount = 0.999
batchSize = 50

#-------------------------------#
#           모델 설정           #
#-------------------------------#

def MakeConv(image, inChannelNumber, outChannelNumber, sizeFilter, nStddev):
    w_conv = tf.Variable(tf.random_normal([sizeFilter, sizeFilter, inChannelNumber, outChannelNumber], stddev = nStddev))
    h_conv = tf.nn.conv2d(image, w_conv, strides = [1, 1, 1, 1], padding = 'SAME')
    b_conv = tf.Variable(tf.constant(0.1, shape = [outChannelNumber]))
    R_conv = tf.nn.relu(h_conv + b_conv)
    return tf.nn.max_pool(R_conv, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = 'SAME')
    
#Conv 1
nFilter1 = 32
sizeFilter1 = 6
channelFilter1 = 1
X = tf.placeholder(tf.float32, [None, nState])
xImage = tf.reshape(X, [-1, gridSize, gridSize, channelFilter1])
P_conv1 = MakeConv(xImage, channelFilter1, nFilter1, sizeFilter1, 0.01)
P_conv1 = tf.nn.dropout(P_conv1, dropoutRate)

#Conv 2
nFilter2 = 64
sizeFilter2 = 6
P_conv2 = MakeConv(P_conv1, nFilter1, nFilter2, sizeFilter2, 0.01)

#Fully connected net
lastPool = P_conv2
nLastFilter = nFilter2
sizeLastConv = int(gridSize / 2 / 2)

lastPool = tf.reshape(lastPool, [-1, nLastFilter * sizeLastConv * sizeLastConv])
w2 = tf.Variable(tf.random_normal([nLastFilter * sizeLastConv * sizeLastConv, nHidden]))
b2 = tf.Variable(tf.constant(0.1, shape = [nHidden]))
hidden = tf.nn.relu(tf.matmul(lastPool, w2) + b2)
hidden = tf.nn.dropout(hidden, dropoutHiddonRate)
w0 = tf.Variable(tf.zeros([nHidden, nAction]))
b0 = tf.Variable(tf.zeros([nAction]))
output_layer = tf.matmul(hidden, w0) + b0

#비용 함수 정의
Y = tf.placeholder(tf.float32, [None, nAction])
cost = tf.reduce_mean(tf.square(Y - output_layer)) / (2 * batchSize)
optimizer = tf.train.AdamOptimizer(learningRate).minimize(cost)
#predict_op = tf.argmax(outout_layer, 1)

class Ai_cnn:
    length = 15
    myType = 0
    def __init__(self, type):
        self.myType = type
        if (type == BLACK): self.enemyType = WHITE
        else: self.enemyType = BLACK

    def getActionRandom(self, omok):
        while(True):
            action = random.randrange(0, nAction)
            x = action % omok.length
            y = action / omok.length
            if (omok.isPossable(x, y, self.myType)):
                return action

    def getAction(self, sess, omok):
        state = omok.getState()
        q = sess.run(output_layer, feed_dict = {X: state, dropoutRate:0.8, dropoutHiddonRate:0.5})
        while(True):
            action = q.argmax()
            x = action % omok.length
            y = action / omok.length
            if (omok.isPossable(x, y, self.myType)):
                return action
            else:
                q[0, action] = -99999

    def trainModel(self, Ai):
        omok = Omok.Omok(15)
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        
        saver = tf.train.Saver()
        
        if(os.path.isfile(os.getcwd() + nameFile) == True):
            saver.restore(sess, os.getcwd() + nameFile)
            print("Model is loaded")

        interaction = 0
        while(True):
            epsilon = 0.9
            countWin = 0
            memory = replayMemory(15, 500, 0.9)

            for i in range(0, 100):
                omok.reset()
                err = 0
                gameOver = False
                while(gameOver != True):
                    action = -9999
                    currentState = omok.getMap()

                    if(random.uniform(0, 1.0) <= epsilon):
                        action = self.getActionRandom(omok)
                    else:
                        action = self.getAction(sess, omok)
                    
                    if (epsilon > epsilonMinimumValue):
                        epsilon *= epsilonDiscount
                    
                    x = action % omok.length
                    y = action / omok.length

                    result = omok.putStone(x, y, self.myType)
                    nextState = omok.getMap()

                    if (result == self.myType):
                        countWin += 1
                        gameOver = True
                        reward = 1
                    
                    result = Ai.put()

                    if (result == self.enemyType):
                        gameOver = True
                        reward = -1

                    memory.remember(currentState, action, reward, nextState, gameOver)

                    inputs, targets = memory.getBatch(output_layer, batchSize, nAction, nState, sess)

                    _t, loss = sess.run([optimizer, cost], feed_dict = {X: inputs, Y: targets, dropoutRate:0.8, dropoutHiddonRate:0.5})
                    err += loss
            print("Epoch " + str(interaction) + str(i) + ": err = " + str(err) + ": Win count = " + str(countWin) +
				" Win ratio = " + str(float(countWin) / float(i + 1) * 100))

            if((i % 10 == 0) and (i != 0)):
                save_path = saver.save(sess, os.getcwd() + nameFile)
                print("Model saved infile : " + save_path)
            interaction += 1





class replayMemory:
    def __init__(self, gridSize, maxMemory, discount):
        self.maxMemory = maxMemory
        self.gridSize = gridSize
        self.nState = gridSize * gridSize
        self.discount = discount

        self.inputState = np.empty((self.maxMemory, self.nState))
        self.actions = np.zeros(self.maxMemory)
        self.nextState = np.empty((self.maxMemory, self.nState))
        self.gameOver = np.empty((self.maxMemory), dtype = np.bool)
        self.rewards =np.empty((self.maxMemory))
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

    def getBatch(self, model, batchSize, nAction, nState, sess):
        memoryLength = self.count
        chosenBatchSize = min(batchSize, memoryLength)

        inputs = np.zeros((chosenBatchSize, nState))
        targets = np.zeros((channelFilter1, nameFile))

        for i in range(0, chosenBatchSize):
            randomIndex = random.randrange(0, memoryLength)
            current_inputState = np.reshape(self.inputState[randomIndex], (1, nState))

            target = sess.run(model, feed_dict = {X: current_inputState, dropoutRate:0.8, dropoutHiddonRate:0.5})

            current_nextState = np.reshape(self.inputState[randomIndex], (1, nState))
            current_output = sess.run(model, feed_dict = {X: current_nextState, dropoutRate:0.8, dropoutHiddonRate:0.5})

            nextStateMaxQ = np.amax(current_output)

            if(nextStateMaxQ > winReward):
                nextStateMaxQ = winReward
            
            if(self.gameOver[randomIndex] == True):
                target[0, [self.actions[randomIndex]]] = self.rewards[randomIndex]
            else:
                target[0, [self.actions[randomIndex]]] = self.rewards[randomIndex] + self.discount * nextStateMaxQ
            inputs[i] = current_inputState
            targets[i] = target
        return inputs, targets

