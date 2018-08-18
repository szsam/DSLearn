import re

import Utils.Helper as Helper
import Utils.Meta as Meta
from Utils.Dictionary import WordDictionary, PersonDictionary

import numpy as np
import string
import csv
import pickle


class Preprocessor:

    def __init__(self):
        self.wordDictionary = WordDictionary(Meta.max_one_hot)
        self.personDictionary = PersonDictionary()
        self.X = []
        self.Y = []

    def one_hot(self, filename, label):
        with open(filename, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                words = Helper.splitSentence(row['text'])
                features = []
                for word in words:
                    # 去除标点符号
                    # word = word.strip(string.punctuation)
                    if 'http' in word:
                        continue
                    if self.wordDictionary.isFull():
                        Helper.debug("[WARNING] Missing word:" + word)
                        continue
                    features.append(self.wordDictionary.lookup(word))
                self.X.append(features)
                self.Y.append(label)
        Helper.debug("[INFORMATION] Total One Hot: %d" % self.wordDictionary.count())

    def pad_sequences(self, max_len, default_value=0):
        for i in range(len(self.X)):
            if len(self.X[i]) > max_len:
                self.X[i] = self.X[i][:max_len]
            else:
                self.X[i].extend([default_value for _ in range(max_len - len(self.X[i]))])

    def load_data(self, file_list: list, max_len=None):
        # 对出现过的单词进行onehot编码，并形成字典
        for idx, file in enumerate(file_list):
            self.personDictionary.addPerson(idx, file)
            label = [0] * len(file_list)
            label[idx] = 1
            self.one_hot(file, label)
        # 将字典保存
        self.save_dict()
        # 计算原始数据长度的均值和方差
        count = [len(x) for x in self.X]
        mean, var = Helper.analysis(count)
        Helper.debug("[INFORMATION] MEAN: %f\tVAR: %f" % (mean, var))
        # 对每个句子进行pad操作
        self.pad_sequences(max_len, 0)
        Helper.debug("[SUCCESS] Load data from file")
        return np.array(self.X), np.array(self.Y)

    def save_dict(self):
        with open('../Model/wordDictionary.pkl', 'wb') as file:
            pickle.dump(self.wordDictionary, file)
        with open('../Model/personDictionary.pkl', 'wb') as file:
            pickle.dump(self.personDictionary, file)

    def load_dict(self):
        # 读取字典
        with open('../Model/wordDictionary.pkl', 'rb') as file:
            self.wordDictionary = pickle.load(file)
        with open('../Model/personDictionary.pkl', 'rb') as file:
            self.personDictionary = pickle.load(file)
