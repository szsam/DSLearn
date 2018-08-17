import Core.NN as NN

from threading import Thread
from time import sleep, strftime, localtime, time

from PyQt5.QtWidgets import *

from Test.predict import predicts
import numpy as np

class AreaLayout1(QVBoxLayout):
    def __init__(self, logger):
        super().__init__()
        self.fileDialog = QFileDialog()
        self.logger = logger

        self.addLayout(self.createStepLayout1())
        self.addLayout(self.createStepLayout2())
        self.addLayout(self.createStepLayout3())
        self.addLayout(self.createStepLayout4())

    def on_chooseFileButton_clicked(self):
        self.trainFileName, _ = self.fileDialog.getOpenFileName()
        self.chooseFileLabel.setText('当前已选择：' + ('...' + self.trainFileName[-15:] if self.trainFileName else '未选择导入聊天文本'))
        self.chooseFileLabel.setToolTip(self.trainFileName)

    def createStepLayout1(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel('STEP1:'))
        self.chooseFileLabel = QLabel('选择导入聊天文本')
        layout.addWidget(self.chooseFileLabel)
        layout.addStretch()
        chooseFileButton = QPushButton('选择文件')
        chooseFileButton.clicked.connect(self.on_chooseFileButton_clicked)
        layout.addWidget(chooseFileButton)
        return layout

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
            sleep(3)
            self.log('结束训练')
            setState('ready')

        self.log('开始训练')
        setState('pending')
        Thread(target=train).start()

    def createStepLayout2(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel('STEP2:'))
        layout.addWidget(QLabel('训练模型'))
        layout.addStretch()
        self.beginTrainButton = QPushButton('开始训练')
        self.beginTrainButton.clicked.connect(self.on_beginTrainButton_clicked)
        layout.addWidget(self.beginTrainButton)
        return layout

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

            #sentences = [
            #    'The GREAT Billy Graham is dead. There was nobody like him! He will bemissed by Christians and all religions. A very special man.',
            #    'Billy Graham was a humble servant who prayed for SO many- and who, with wisdom and grace, gave hope and guidance to generations of Americans.'
            #]

            sentences = self.predictEdit.toPlainText().split('\n')
            results = predicts(model, sentences)
            self.log(str(results))
            idxs = np.argmax(results, axis=1)
            self.predictResultLabel.setText(str(idxs))
            self.log('结束预测')
            setState('ready')

        self.log('开始预测')
        setState('pending')
        Thread(target=predict).start()

    def createStepLayout3(self):
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
        return layout

    def createStepLayout4(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel('STEP4:'))
        layout.addWidget(QLabel('预测结果'))
        layout.addStretch()
        self.predictResultLabel = QLabel('unknown')
        layout.addWidget(self.predictResultLabel)
        return layout

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
