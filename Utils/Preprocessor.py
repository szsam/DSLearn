import Utils.Helper as Helper
import Utils.Meta as Meta
import numpy as np
import string
import csv
import pickle
import random
import Utils.Word2Vec as Word2Vec


class Preprocessor:

    def __init__(self):
        self.one_hot_dict = {}  # type: dict[str, int]
        self.X = []
        self.Y = []

    def one_hot(self, filename, tag):

        one_hot_cnt = 1
        with open(filename, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                str_words = row['text'].split()
                int_words = []
                for word in str_words:
                    word = word.strip(string.punctuation)
                    if 'http' in word:
                        continue
                    if one_hot_cnt >= Meta.max_one_hot:
                        Helper.debug("[WARNING] Missing word:" + word)
                        continue
                    if word not in self.one_hot_dict:
                        self.one_hot_dict[word] = one_hot_cnt
                        one_hot_cnt += 1
                    int_words.append(self.one_hot_dict[word])
                self.X.append(int_words)
                self.Y.append(tag)
        Helper.debug("[INFORMATION] Total One Hot: " + str(one_hot_cnt))

    def pad_sequence(seq, max_len, default_value=0):
        if not isinstance(seq, list):
            raise TypeError('bad operand type')
        if len(seq) > max_len:
            pad_seq = seq[:max_len]
        else:
            pad_seq = seq
            pad_seq.extend([default_value for i in range(max_len - len(seq))])
        return pad_seq

    def load_data(self, max_len=None, n_word2vec=300):

        # 对出现过的单词进行onehot编码，并形成字典
        self.one_hot('../DataSet/BarackObama.csv', [0, 1])
        self.one_hot('../DataSet/DonaldTrumpTweets.csv', [1, 0])

        with open('../Model/dict.pkl', 'bw') as file:
            pickle.dump(self.one_hot_dict, file)

        # 计算原始数据的均值和方差
        count = []
        for i in range(len(self.X)):
            count.append(len(self.X[i]))
        mean, var = Helper.analysis(count)
        Helper.debug("[INFORMATION] MEAN: " + str(mean) + "\tVAR: " + str(var))

        # 对每个句子进行pad操作
        for i in range(len(self.X)):
            self.X[i] = Preprocessor.pad_sequence(self.X[i], max_len, 0)
        Helper.debug("[SUCCESS] Load data from file")

        return np.array(self.X), np.array(self.Y)