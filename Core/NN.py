import Utils.Meta as Meta

import tflearn
from tflearn import input_data, conv_1d, lstm, embedding
from tflearn.layers.conv import global_max_pool
from tflearn.layers.merge_ops import merge
from tflearn.layers.estimator import regression
from tflearn.layers.core import dropout, fully_connected


def build():
    network = input_data([None, Meta.max_string_len])
    network = embedding(network, input_dim=Meta.max_one_hot, output_dim=128)
    branch1 = conv_1d(network, 128, 3, padding='valid', activation='relu', regularizer="L2")
    branch2 = conv_1d(network, 128, 4, padding='valid', activation='relu', regularizer="L2")
    branch3 = conv_1d(network, 128, 5, padding='valid', activation='relu', regularizer="L2")
    network = merge([branch1, branch2, branch3], mode='concat', axis=1)
    network = dropout(network, 0.5)
    network = lstm(network, 128)
    # network = fully_connected(network, 20)
    network = fully_connected(network, 2, activation='softmax')
    network = tflearn.regression(network, optimizer='adam', learning_rate=0.001, loss='categorical_crossentropy')
    model = tflearn.DNN(network, tensorboard_verbose=0)
    return model


def train(X,Y):
    model = build()
    model.fit(X, Y, n_epoch=Meta.n_epoch, validation_set=0.1, show_metric=True)
    return model
