from __future__ import division, print_function, absolute_import
import tensorflow as tf
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_1d, global_max_pool
from tflearn.layers.merge_ops import merge
from tflearn.layers.estimator import regression
from tflearn.data_utils import to_categorical, pad_sequences
from tflearn.datasets import imdb
import pickle
import numpy as np
"""
还是加载imdb.pkl数据
"""
train, test, _ = imdb.load_data(path='imdb.pkl', n_words=10000,
                                valid_portion=0.1)
trainX, trainY = train
testX, testY = test
"""
转化为固定长度的向量，这里固定长度为100
"""
trainX = pad_sequences(trainX, maxlen=100, value=0.)
testX = pad_sequences(testX, maxlen=100, value=0.)
"""
二值化向量
"""
trainY = to_categorical(trainY, nb_classes=2)
testY = to_categorical(testY, nb_classes=2)
"""
构建卷积神经网络，这里卷积神经网网络为1d卷积
"""
network = input_data(shape=[None, 100], name='input')
network = tflearn.embedding(network, input_dim=10000, output_dim=128)
branch1 = conv_1d(network, 128, 3, padding='valid', activation='relu', regularizer="L2")
branch2 = conv_1d(network, 128, 4, padding='valid', activation='relu', regularizer="L2")
branch3 = conv_1d(network, 128, 5, padding='valid', activation='relu', regularizer="L2")
network = merge([branch1, branch2, branch3], mode='concat', axis=1)
network = tf.expand_dims(network, 2)
network = global_max_pool(network)
network = dropout(network, 0.5)
network = fully_connected(network, 2, activation='softmax')
network = regression(network, optimizer='adam', learning_rate=0.001,
                     loss='categorical_crossentropy', name='target')
"""
训练开始
"""
model = tflearn.DNN(network, checkpoint_path="",tensorboard_verbose=0)
model.fit(trainX, trainY, n_epoch = 1, shuffle=True, validation_set=(testX, testY), show_metric=True, batch_size=32)
"""
模型保存
"""
model.save("cnn.model")
"""
做测试使用
"""
test=np.linspace(1,101,100).reshape(1,100)

print("测试结果：",model.predict(test))
