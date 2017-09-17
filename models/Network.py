#! /user/bin/evn python
# -*- coding:utf8 -*-

"""
Network
======

A class for something.

@author: Guoxiu He
@contact: guoxiu.he@whu.edu.cn
@site: https://frankblood.github.io
@time: 17-9-16下午8:10
@copyright: "Copyright (c) 2017 Guoxiu He. All Rights Reserved"
"""

from __future__ import print_function
from __future__ import division

import os
import sys

curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(curdir))

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")

from keras.callbacks import EarlyStopping, ModelCheckpoint
import time
from keras.models import Sequential, Model
from keras.layers import Input, Embedding, Dense, LSTM, GRU, Conv1D, GlobalMaxPooling1D, MaxPooling1D, GlobalAveragePooling1D
from keras.layers import TimeDistributed, RepeatVector, Permute, Lambda, Bidirectional, Dropout
from keras.layers.merge import concatenate, add, dot, multiply
from keras.layers.normalization import BatchNormalization
from keras import backend as K
from keras.layers import Activation
from keras.optimizers import RMSprop, Adam, SGD, Adagrad, Adadelta, Adamax, Nadam
from keras.layers.advanced_activations import PReLU

class Network(object):
    def __init__(self, maxlen=200, units=5, nb_words=200000,
                 embedding_dims=200, rnn_dim=200, dropout_rate=0.5,
                 loss='categorical_crossentropy', optimizer='nadam'):
        self.nb_words = nb_words
        self.embedding_dims = embedding_dims
        self.maxlen = maxlen
        self.rnn_dim = rnn_dim
        self.dropout_rate = dropout_rate
        self.units = units
        self.loss = loss
        self.optimizer = optimizer

    def set_name(self, model_name):
        self.model_name = model_name

    def build(self, embedding_matrix=None):
        self.model = Model()

    def inference(self, x, model_path, batch_size):
        self.model.load_weights(filepath=model_path)
        y = self.model.predict(x, batch_size=batch_size)
        return y

    def train(self, feature, target):

        early_stopping = EarlyStopping(monitor='val_acc', patience=3)
        now_time = '_'.join(time.asctime(time.localtime(time.time())).split(' '))
        bst_model_path = './models/save/' + self.model_name + '_' + now_time + '.h5'
        print('bst_model_path:', bst_model_path)
        model_checkpoint = ModelCheckpoint(bst_model_path, monitor='val_acc', save_best_only=True,
                                           save_weights_only=True)

        if os.path.exists(bst_model_path):
            self.model.load_weights(bst_model_path)

        self.model.fit(feature, target,
                       batch_size=50,
                       nb_epoch=10, shuffle=True,
                       validation_split=0.2,
                       # callbacks=[model_checkpoint])
                       callbacks=[early_stopping, model_checkpoint])

def func():
    pass


if __name__ == "__main__":
    pass
