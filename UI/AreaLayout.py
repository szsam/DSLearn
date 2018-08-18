import Core.NN as NN
from Utils.Preprocessor import Preprocessor
import Utils.Meta as Meta
from Test.predict import predicts

from threading import Thread
from time import sleep, strftime, localtime, time
import numpy as np

from PyQt5.Qt import *


class AreaLayout1(QVBoxLayout):
    def __init__(self, logger):
        super().__init__()
        self.trainFileNames = []
        self.logger = logger
        self.fileDialog = QFileDialog()
        self.loader = Preprocessor()

        self.addWidget(self.createStepFrame1())
        self.addWidget(self.createStepFrame2())
        self.addWidget(self.createStepFrame3())
        self.addWidget(self.createStepFrame4())

    def on_chooseFileButton_clicked(self):
        self.trainFileNames, _ = self.fileDialog.getOpenFileNames(directory='../DataSet')
        text = '当前已选择：\n'
        text += '\n'.join([ file[-15:] for file in self.trainFileNames])
        self.chooseFileLabel.setText(text)
        self.chooseFileLabel.setToolTip(str(self.trainFileNames))

    def createStepFrame1(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        layout = QHBoxLayout()
        layout.addWidget(QLabel('STEP1:'))
        self.chooseFileLabel = QLabel('选择导入聊天文本')
        layout.addWidget(self.chooseFileLabel)
        layout.addStretch()
        chooseFileButton = QPushButton('选择文件')
        chooseFileButton.clicked.connect(self.on_chooseFileButton_clicked)
        layout.addWidget(chooseFileButton)
        frame.setLayout(layout)
        return frame

    def on_beginTrainButton_clicked(self):
        def setState(state):
            if state == 'pending':
                self.beginTrainButton.setEnabled(False)
                self.beginTrainButton.setText('训练中')
            elif state == 'ready':
                self.beginTrainButton.setEnabled(True)
                self.beginTrainButton.setText('开始训练')
            else:
                raise Exception('Unknown State')

        def train():
            X, Y = self.loader.load_data(self.trainFileNames, max_len=Meta.max_string_len)
            model = NN.train(X, Y)
            model.save('../Model/model')
            self.log('结束训练')
            setState('ready')

        self.log('开始训练')
        setState('pending')
        Thread(target=train).start()

    def createStepFrame2(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        layout = QHBoxLayout()
        layout.addWidget(QLabel('STEP2:'))
        layout.addWidget(QLabel('训练模型'))
        layout.addStretch()
        self.beginTrainButton = QPushButton('开始训练')
        self.beginTrainButton.clicked.connect(self.on_beginTrainButton_clicked)
        layout.addWidget(self.beginTrainButton)
        frame.setLayout(layout)
        return frame

    def on_predictButton_clicked(self):
        def setState(state):
            if state == 'pending':
                self.predictButton.setEnabled(False)
                self.predictButton.setText('预测中')
            elif state == 'ready':
                self.predictButton.setEnabled(True)
                self.predictButton.setText('进行预测')
            else:
                raise Exception('Unknown State')

        def predict():
            model = NN.build()
            model.load('../Model/model')
            self.loader.load_dict()

            #sentences = [
            #    'The GREAT Billy Graham is dead. There was nobody like him! He will bemissed by Christians and all religions. A very special man.',
            #    'Billy Graham was a humble servant who prayed for SO many- and who, with wisdom and grace, gave hope and guidance to generations of Americans.'
            #]

            sentences = self.predictEdit.toPlainText().split('\n')
            results = predicts(model, sentences)
            self.log(str(results))
            idxs = list(np.argmax(results, axis=1))
            text = "\n".join([self.loader.personDictionary.lookup(idx) for idx in idxs])
            self.predictResultLabel.setText(text)
            self.log('结束预测')
            setState('ready')

        self.log('开始预测')
        setState('pending')
        Thread(target=predict).start()

    def createStepFrame3(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        layout = QHBoxLayout()
        layout.addWidget(QLabel('STEP3:'))
        self.predictEdit = QTextEdit()
        self.predictEdit.setPlaceholderText('请输入要预测的用户文本')
        self.predictEdit.setAcceptRichText(False)
        #edit.setFixedSize(200, 100)
        layout.addWidget(self.predictEdit)
        self.predictButton = QPushButton('进行预测')
        self.predictButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.predictButton.clicked.connect(self.on_predictButton_clicked)
        layout.addWidget(self.predictButton)
        frame.setLayout(layout)
        return frame

    def createStepFrame4(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        layout = QHBoxLayout()
        layout.addWidget(QLabel('STEP4:'))
        layout.addWidget(QLabel('预测结果'))
        layout.addStretch()
        self.predictResultLabel = QLabel('unknown')
        layout.addWidget(self.predictResultLabel)
        frame.setLayout(layout)
        return frame

    def log(self, s):
        self.logger.append(strftime('%Y-%m-%d %H:%M:%S\n', localtime(time())) + s)


class AreaLayout2(QVBoxLayout):

    def on_clearButton_clicked(self):
        self.terminal.clear()

    def __init__(self):
        super().__init__()
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setFixedWidth(300)
        self.addWidget(self.terminal)
        self.clearButton = QPushButton("清除控制台")
        self.clearButton.clicked.connect(self.on_clearButton_clicked)
        self.addWidget(self.clearButton)
