from queue import Queue
from threading import Thread

import numpy as np

import Core.NN as NN
import pickle
import string
import Utils.Meta as Meta
import Utils.Helper as Helper
import socket

from Utils.Preprocessor import Preprocessor


def pad_sequence(seq, max_len, default_value=0):
    if not isinstance(seq, list):
        raise TypeError('bad operand type')
    if len(seq) > max_len:
        pad_seq = seq[:max_len]
    else:
        pad_seq = seq
        pad_seq.extend([default_value for i in range(max_len - len(seq))])
    return pad_seq


def int_words(words):
    with open('../Model/wordDictionary.pkl', 'rb') as file:
        one_hot_dict = pickle.load(file).one_hot_dict
    str_words = Helper.splitSentence(words)
    int_words=[]
    dismiss_cnt = 0
    total_cnt = 0
    for word in str_words:
        total_cnt += 1
        if word not in one_hot_dict:
            int_words.append(0)
            dismiss_cnt += 1
        else:
            int_words.append(one_hot_dict[word])
    int_words = pad_sequence(int_words, Meta.max_string_len)
    Helper.debug('[WARNING] dismiss: %d\ttotal: %d' % (dismiss_cnt, total_cnt))
    return int_words


def predicts(model, sentences):
    int_sentences = [int_words(sentence) for sentence in sentences]
    return model.predict(int_sentences)

def build_connection(self):
    sk = socket.socket()
    sk.bind((socket.gethostname(), 8080))
    sk.listen(1)
    while True:
        c_sk, c_addr = sk.accept()
        print("Connection from: " + str(c_addr))
        print('Waiting...')
        data = c_sk.recv(1024).decode('utf-8')
        if not data:
            continue
        print('Get: ' + data)
        sentences_queue.put(data)
        print('sentences number: ' + str(sentences_queue.qsize()))
    c_sk.close()

# sentences_queue = Queue()

if __name__ == '__main__':
    model = NN.build()
    model.load('../Model/model')
    loader = Preprocessor()
    loader.load_dict()

    # sentences = [
    #    'The GREAT Billy Graham is dead. There was nobody like him! He will bemissed by Christians and all religions. A very special man.',
    #   'Billy Graham was a humble servant who prayed for SO many- and who, with wisdom and grace, gave hope and guidance to generations of Americans.'
    # ]

    # Thread(target=build_connection).start()

    sk = socket.socket()
    sk.bind((socket.gethostname(), 8080))
    sk.listen(1)
    while True:
        print('Waiting...')
        c_sk, c_addr = sk.accept()
        print("Connection from: " + str(c_addr))
        sentence = c_sk.recv(1024).decode('utf-8')
        if not sentence:
            continue
        print('Get: ' + sentence)
        sentences = []
        sentences.append(sentence)
        result = predicts(model, sentences)
        idxs = list(np.argmax(result, axis=1))
        print(idxs)
        result = "\n".join([loader.personDictionary.lookup(idx) for idx in idxs])
        c_sk.send(result.encode('utf-8'))
        print(result)
        # sentences_queue.put(data)
        # print('sentences number: ' + str(sentences_queue.qsize()))

    # result = predicts(model, sentences)
    # print(result)