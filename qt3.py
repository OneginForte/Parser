import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
 
 
class SecondWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окна
        super().__init__(parent, QtCore.Qt.Window)
        self.mainLayout = QVBoxLayout()
        self.build()
 
    def build(self):
        check = QCheckBox('some text')
        self.mainLayout.addWidget(check)
 
        self.setLayout(self.mainLayout)
 
 
class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.secondWin = None
        self.build()
 
    def build(self):
        self.mainLayout = QVBoxLayout()
 
        self.lab = QLabel('simple text', self)
        self.mainLayout.addWidget(self.lab)
 
        self.but1 = QPushButton('open window', self)
        self.but1.clicked.connect(self.open_win)
        self.mainLayout.addWidget(self.but1)
 
        self.setLayout(self.mainLayout)
 
    def open_win(self):
        if not self.secondWin:
            self.secondWin = SecondWindow(self)
        self.secondWin.show()
 
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())