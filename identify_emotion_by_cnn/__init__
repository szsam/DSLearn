import tflearn
from tflearn import input_data, conv_1d, regression
import tensorflow as tf
from tflearn.layers.conv import global_max_pool
from tflearn.layers.merge_ops import merge
from tflearn.layers.estimator import regression
from tflearn.layers.core import dropout, fully_connected
from identify_emotion_by_cnn import preprocessor
from tflearn.data_utils import to_categorical, pad_sequences


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
model = tflearn.DNN(network, tensorboard_verbose=0)


def train_me():

    """
    神经网络训练部分
    :return:
    """

    """
    加载数据
    """
    train, test = preprocessor.load_data()
    trainX, trainY = train
    testX, testY = test

    """
    转化为固定长度的向量，这里固定长度为100
    """
    trainX = pad_sequences(trainX, maxlen=100, value=0.)
    testX = pad_sequences(testX, maxlen=100, value=0.)

    trainY = to_categorical(trainY, nb_classes=2)
    testY = to_categorical(testY, nb_classes=2)

    """
    开始训练
    """
    model.fit(trainX, trainY, n_epoch=10, shuffle=True, validation_set=(testX, testY), show_metric=True, batch_size=32)
    
    """
    模型保存
    """
    model.save("cnn.model")


def predict_me():
    """
    读取model，进行预测
    :return:
    """
    preprocessor.load_data()
    model.load("cnn.model")
    """
    做测试使用
    """

    test_string1 = "厉害呀，我们九零后不只是大家说的那么一文不值的，只是一少部分而已，不能一概而论，几零后也有那种一文不值的人渣……"
    test1 = preprocessor.predict_data(test_string1)

    test_string2 = "蛮不讲理，脑残无极限。"
    test2 = preprocessor.predict_data("只有人民有信仰，国家才有希望")

    test12 = pad_sequences([test1, test2], maxlen=100, value=0.)

    pred = model.predict(test12)

    print("测试结果：", pred)

if __name__ == "__main__":
    # train_me()
    predict_me()
