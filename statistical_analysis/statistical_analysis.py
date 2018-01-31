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
    Besides,special_words mean the followings:
        Word/Flag:
        助词/u
        叹词/e
        语气词/y
        拟声词/o

    Here is the list of the functions:
        stc_len -- 句子长度
        stc_phrase_count -- 词频统计
        stc_char_count -- 字频统计
        stc_digit_count -- 阿拉伯数字（0-9）使用频率统计
        stc_letter_count -- 英文字母（含大小写）使用频率统计
        stc_punct_count1 -- 标点符号使用频率统计(利用jieba分词)
        stc_punct_count2 -- 标点符号使用频率统计（利用正则表达式）
"""

import jieba
import jieba.posseg
import string
import re
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

#   This counts the digit from 0 to 9,
#   and digit_num contains all the digit from 0 to 9, of which value may be 0.
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

#   This counts the letter from a to z, and A to Z,
#   and letter_num contains all the letter from a to z, and A to Z, of which value may be 0.
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

#   This counts the punctuation character in the local file common_zh_punct,
#   and punct_num contains all the punctuations mentioned above, of which value may be 0.
def stc_punct_count(sentence):
    #initialize
    f = open('common_zh_punct', 'r', encoding='UTF-8')
    punct_num = dict(Counter(f.readline().encode('utf-8').decode('utf-8-sig')))
    for p in punct_num:
        punct_num[p] -= 1
    #process
    unit_list = list(sentence)
    for u in unit_list:
        if u in punct_num:
            punct_num[u] += 1
    f.close()
    return punct_num

#   This counts the special words，
#   and special_words_num doesn't contain all the special words in the world.
def stc_special_words_count(sentence):
    words = jieba.posseg.lcut(sentence)
    special_words_num = {}
    for w in words:
        if w.flag[0] == 'u' or w.flag[0] == 'e' or w.flag[0] == 'y' or w.flag[0] == 'o':
            if w.word not in special_words_num:
                special_words_num[w.word] = 1
            else:
                special_words_num[w.word] += 1
    return special_words_num

#   This counts the popular phrases，
#   and pop_phrase_num does contain all the popular phrases we collected manully,
#   but not contain all the popular phrases in the world, using jieba.
def stc_pop_phrase_count1(sentence):
    # initialize
    f = open('common_pop_phrase', 'r', encoding='UTF-8')
    lines = f.readlines()
    pop_phrases = []
    for i in lines:
        pop_phrases.append((i.encode('utf-8').decode('utf-8-sig'))[:-1])
    pop_phrase_num = dict(Counter(pop_phrases))
    for p in pop_phrase_num:
        pop_phrase_num[p] -= 1
    # process
    phrase_list = jieba.lcut(sentence, cut_all=False)
    print(phrase_list)
    for p in phrase_list:
        if p in pop_phrase_num:
            pop_phrase_num[p] += 1
    f.close()
    return  pop_phrase_num

#   This counts the popular phrases，
#   and pop_phrase_num does contain all the popular phrases we collected manully,
#   but not contain all the popular phrases in the world, using RE.
def stc_pop_phrase_count2(sentence):
    # initialize
    f = open('common_pop_phrase', 'r', encoding='UTF-8')
    lines = f.readlines()
    pop_phrases = []
    for i in lines:
        pop_phrases.append((i.encode('utf-8').decode('utf-8-sig'))[:-1])
    pop_phrase_num = dict(Counter(pop_phrases))
    for p in pop_phrase_num:
        pop_phrase_num[p] -= 1
    # process
    for p in pop_phrase_num:
        p0 = p
        pattern = re.compile(p0)
        pop_phrase_num[p] += len(pattern.findall(sentence))
    f.close()
    return  pop_phrase_num

if __name__ == '__main__':
    print(stc_len('你好，在吗？'))
    print(stc_phrase_count('我今天想吃一个苹果，然后看部film，不知道你是怎么想的呢？哈哈~'))
    print(stc_char_count('我今天想吃一个苹果，然后看部film，不知道你是怎么想的呢？哈哈~'))
    print(stc_digit_count('121221121221,321312434,42432'))
    print(stc_letter_count('dadadadkasjdkladjkwl'))
    print(stc_punct_count('，。、'))
    print(stc_special_words_count('今天的天气好差劲噢~'))
    print(stc_pop_phrase_count1('如果我有freestyle的话，惊不惊喜？'))    #won't find "惊不惊喜"
    print(stc_pop_phrase_count2('如果我有freestyle的话，惊不惊喜？'))   #will fild "惊不惊喜"

