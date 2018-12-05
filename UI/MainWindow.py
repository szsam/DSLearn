from UI.AreaLayout import AreaLayout1, AreaLayout2
import sys
from PyQt5.QtWidgets import *


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('DSLearn')
        # self.resize(600, 400)
        windowLayout = QHBoxLayout()

        # 将area1的logger和area2的terminal绑定起来
        area2 = AreaLayout2()
        self.logger = area2.terminal
        area1 = AreaLayout1(self.logger)

        windowLayout.addLayout(area1)
        windowLayout.addLayout(area2)
        self.setLayout(windowLayout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
