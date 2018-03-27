import tensorflow as tf
import os
import random
import math
import numpy as np
import Omok

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
channelFilter1 = 3
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
sizeLastConv = gridSize / 2 / 2

lastPool = tf.reshape(lastPool, [-1, nLastFilter * sizeLastConv * sizeLastConv])
w2 = tf.Variable(tf.random_normal([nLastFilter * sizeLastConv * sizeLastConv, nHidden]))
b2 = tf.Variable(tf.constant(0.1, shape = [nHidden]))
hidden = tf.nn.relu(tf.matmul(lastPool, w2) + b2)
hidden = tf.nn.dropout(hidden, dropoutHiddonRate)
w0 = tf.Variable(tf.zeros([nHidden, nAction]))
b0 = tf.Variable(tf.zeros([nAction]))
output_layer = tf.matmul(hidden, w0)+b0

#비용 함수 정의
Y = tf.placeholder(tf.float32, [None, nAction])
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(output_layer, Y))
optimizer = tf.train.AdamOptimizer(learningRate).minimize(cost)
#predict_op = tf.argmax(outout_layer, 1)

class Ai_cnn:
    def __init__(self, type):
        self.myType = type
        if (type == BLACK): self.enemyType = WHITE
        else: self.enemyType = BLACK
            
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        
        saver = tf.train.Saver()
        
        if(os.path.isfile(os.getcwd() + nameFile) == True):
            saver.restore(sess, os.getcwd() + nameFile)
            print("Model is loaded")
            
    def trainModel(self, Ai):
        omok = Omok.Omok(15)
        countWin = 0
        for i in range(0, 100):
            #omok.reset()
            err = 0
            overGame = False
             
    def Put(self, sess, omok):
        state = omok.getState()
        q = sess.run(output_layer, feed_dict = {X: state, dropoutRate:0.8, dropoutHiddonRate:0.5})
        while(True):
            action = q.argmax()
            if (state[action] == NONE):
                return action #깃허브 연습
            else:
                q[0, action] = -99999
        nextState = omok.getState()
        return nextState
