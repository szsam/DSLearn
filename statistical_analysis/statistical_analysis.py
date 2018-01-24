"""
    This file is about the statistical analysis on the sentences.

    We basically specify that:
        '我们爱您' is a string;
        Both '我' and '们' are the units of the string '我们爱您'.
    At the same time, we specify that:
        '我' is a char;
        '我们' is a phrase;
        '我们爱您' is a sentence;
        '1' is a digit;
        'a' is a letter;
        '！' is a punctuation.

    Here is the list of the functions:
        stc_len -- 句子长度
        stc_phrase_count -- 词频统计
        stc_char_count -- 字频统计
        stc_digit_count -- 阿拉伯数字（0-9）使用频率统计
        stc_letter_count -- 英文字母（含大小写）使用频率统计
        stc_punct_count -- 标点符号使用频率统计

"""

import jieba
import string
from collections import Counter

#   stc == sentence
def stc_len(sentence):
    return len(sentence)

def stc_phrase_count(sentence):
    phrase_list = jieba.lcut(sentence, cut_all = False)
    cnt = Counter(phrase_list)
    return dict(cnt)

def stc_char_count(sentence):
    unit_list = list(sentence)
    cnt = Counter(unit_list)
    return dict(cnt)

#   count the digit from 0 to 9
def stc_digit_count(sentence):
    #initialize
    digit_num = dict(Counter(string.digits))
    for d in digit_num:
        digit_num[d] -= 1
    #process
    unit_list = list(sentence)
    for u in unit_list:
        if u in digit_num:
            digit_num[u] += 1
    return digit_num

#   count the letter from a to z, and A to Z
def stc_letter_count(sentence):
    #initialize
    letter_num = dict(Counter(string.ascii_letters))
    for l in letter_num:
        letter_num[l] -= 1
    #process
    unit_list = list(sentence)
    for u in unit_list:
        if u in letter_num:
            letter_num[u] += 1
    return letter_num

#   count the ASCII character which are considered
#   punctuation character in the C locale
def stc_punct_count(sentence):
    #initialize
    punct_num = dict(Counter(string.punctuation))
    for p in punct_num:
        punct_num[p] -= 1
    #process
    unit_list = list(sentence)
    for u in unit_list:
        if u in punct_num:
            punct_num[u] += 1
    return punct_num

if __name__ == '__main__':
    print(stc_len('你好，在吗？'))
    print(stc_phrase_count('我今天想吃一个苹果，然后看部film，不知道你是怎么想的呢？哈哈~'))
    print(stc_char_count('我今天想吃一个苹果，然后看部film，不知道你是怎么想的呢？哈哈~'))
    print(stc_digit_count('121221121221,321312434,42432'))
    print(stc_letter_count('dadadadkasjdkladjkwl'))
    print(stc_punct_count('.,/.,.,=-*-+/+./!#@$#%#%%#^$^^'))