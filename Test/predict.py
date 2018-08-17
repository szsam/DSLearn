import Core.NN as NN
import pickle
import string
import Utils.Meta as Meta
import Utils.Helper as Helper


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
    with open('../Model/dict.pkl', 'rb') as file:
        one_hot_dict = pickle.load(file)

    str_words = words.split()
    int_words=[]
    dismiss_cnt = 0
    total_cnt = 0
    for word in str_words:
        word.strip(string.punctuation)
        total_cnt += 1
        if word not in one_hot_dict:
            int_words.append(0)
            dismiss_cnt += 1
        else:
            int_words.append(one_hot_dict[word])
    int_words = pad_sequence(int_words, Meta.max_string_len)
    Helper.debug('[WARNING] dismiss: '+str(dismiss_cnt)+'\ttotal: '+str(total_cnt))
    return int_words


def predicts(model, sentences):
    int_sentences = [int_words(sentence) for sentence in sentences]
    return model.predict(int_sentences)


if __name__ == '__main__':
    model = NN.build()
    model.load('../Model/model')

    sentences = [
        'The GREAT Billy Graham is dead. There was nobody like him! He will bemissed by Christians and all religions. A very special man.',
        'Billy Graham was a humble servant who prayed for SO many- and who, with wisdom and grace, gave hope and guidance to generations of Americans.'
    ]

    result = predicts(model, sentences)
    print(result)
