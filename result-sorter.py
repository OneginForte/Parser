import os
import struct
import sys

from Pro_parser import Parser

#from time import gmtime, strftime
#from tkinter import CENTER

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import ( QApplication, QComboBox, QFileDialog, QGridLayout, QListWidget,
                              QMessageBox, QPushButton, QVBoxLayout, QWidget)


class MainWindow(QtWidgets.QMainWindow):
    
    
    
    def __init__(self):
        self.lfr = ""
        self.sorted_rule = 0
        self.group_rule = 0
        self.all_tabs = []

        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon('Ski.ico'))
        self.setWindowTitle("Генератор итоговых результатов для Марафон-Электро.")
        self.cwd = os.getcwd() # Получить текущее местоположение файла программы
        #self.resize(1500, 1300)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
  
  
        self.list_widget = QListWidget()

        self.list_widget.setStyleSheet("QListWidget"
                                  "{"
                                  "border : 1px solid black;"
                                  "font: 10pt fixedsys;"
                                  "}"
                                  )
                               
        self.statusBar()
        
        self.btn_choose1 = QPushButton(self)  
        self.btn_choose1.setObjectName("Номер")  
        self.btn_choose1.setText("Номер")
        self.btn_choose1.setCheckable(True)
        self.btn_choose1.setChecked(True)
        self.btn_choose1.setEnabled(False)
        
        self.btn_choose2 = QPushButton(self)  
        self.btn_choose2.setObjectName("Фамилия")
        self.btn_choose2.setText("Фамилия")
        self.btn_choose2.setCheckable(True)
        self.btn_choose2.setEnabled(False)

        self.btn_choose3 = QPushButton(self)  
        self.btn_choose3.setObjectName("Результат")
        self.btn_choose3.setText("Результат")        
        self.btn_choose3.setCheckable(True)
        self.btn_choose3.setEnabled(False)
        
        self.btn_chooseFile = QPushButton(self)  
        self.btn_chooseFile.setObjectName("Выбрать")
        self.btn_chooseFile.setText("Открыть протокол")

        self.text1 = QtWidgets.QLabel("Список участников, имеющие стартовый номер",
                                    alignment=QtCore.Qt.AlignCenter)
        self.text2 = QtWidgets.QLabel("Сортировка",
                                    alignment=QtCore.Qt.AlignCenter)
        self.text3 = QtWidgets.QLabel("Группы",
                                    alignment=QtCore.Qt.AlignCenter)

        
        self.combo = QComboBox(self)
        self.combo.setFixedWidth(125)
        self.combo.hidePopup()
        
        
        self.right_layout = QVBoxLayout()
      
        #self.setLayout(self.right_layout)
        
        self.left_layout = QVBoxLayout()
   
        #self.setLayout(self.left_layout)
        
        self.btn_choose1.pressed.connect(self.slot_btn_choose1) 
        self.btn_choose2.pressed.connect(self.slot_btn_choose2) 
        self.btn_choose3.pressed.connect(self.slot_btn_choose3)
        self.btn_chooseFile.clicked.connect(self.slot_btn_chooseFile)       
        self.list_widget.itemClicked.connect(self.clicked)
        self.combo.activated[int].connect(self.onComboSelected)
        
        
        grid = QGridLayout()
        grid.setSpacing(5)

        #grid.setColumnStretch(0, 1)
        #grid.setColumnStretch(1, 1)
        #grid.setRowStretch(0, 1)
        #grid.setRowStretch(0, 1)
        
        self.right_layout.addWidget(self.text1)
        self.right_layout.addWidget(self.list_widget, 1)
        #self.right_layout.addStretch(1) 
        self.left_layout.addWidget(self.text2)
        self.left_layout.addWidget(self.btn_choose1) 
        self.left_layout.addWidget(self.btn_choose2) 
        self.left_layout.addWidget(self.btn_choose3)         
        self.left_layout.addWidget(self.btn_chooseFile) #,alignment=QtCore.Qt.AlignTop
        self.left_layout.addWidget(self.text3)
        self.left_layout.addWidget(self.combo)

        self.left_layout.addStretch()

        grid.addLayout(self.left_layout, 0, 0 , 
                       alignment=QtCore.Qt.AlignLeft) 
        
        grid.addLayout(self.right_layout, 0, 1, 0, 1, 
                       alignment=QtCore.Qt.AlignRight) 

        #grid.addWidget(self.list_widget, 0, 1, 20, 20)      
        
        #tempFrame.addWidget(grid)
        #centralWidget.addWidget(tempFrame)
        
        centralWidget.setLayout(grid)
        self.setGeometry(500, 300, 900, 500)
        self.show()
 

    def clicked(self, item):
        QMessageBox.information(self, "Подробнее", "Участник номер: " + item.text(),QMessageBox.Ok)

    def onComboSelected(self, index_val):
        self.group_rule=index_val    
        self.reload()
    
    def slot_btn_choose1(self):
        #self.btn_choose1.setChecked(True)
        self.btn_choose2.setChecked(False)
        self.btn_choose3.setChecked(False)
        self.sorted_rule = 0
        self.reload()

    def slot_btn_choose2(self):
        self.btn_choose1.setChecked(False)
        #self.btn_choose2.setChecked(True)
        self.btn_choose3.setChecked(False)
        self.sorted_rule = 1
        self.reload()
        
    def slot_btn_choose3(self):    
        self.btn_choose1.setChecked(False)
        self.btn_choose2.setChecked(False)
        #self.btn_choose3.setChecked(True)
        self.sorted_rule = 2
        self.reload()
         
    
    def slot_btn_chooseFile(self):
        
        self.local_filename_choose, filetype = QFileDialog.getOpenFileName(self,
                                   "Выбрать протокол",  
                                    self.cwd, # Начальный путь 
                                    "Pro Files (*.pro)")   # Установить фильтрацию расширений файлов, через двойную точку с запятой        
        
        if self.local_filename_choose == "":
            
            return

        self.reload()

        self.btn_choose1.setEnabled(True)
        self.btn_choose2.setEnabled(True)
        self.btn_choose3.setEnabled(True)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()

    def reload(self):

        filename_grp = self.local_filename_choose.rsplit('.', 1)[0] + '.grp'

        dPars.grp_zag, dPars.grp, dPars.increment_grp= Parser.read_grp(
            dPars, filename_grp)

        dPars.pro1, dPars.increment_pro1, dPars.increment = Parser.read_pro(
            dPars, self.local_filename_choose)
        
        self.lfr1 = Parser.repack(
            dPars, dPars.grp, dPars.pro1, w.group_rule, w.sorted_rule)
        QListWidget.clear(self.list_widget)

        # Преобразуем списки участников в чистый текст.
        self.lfr1 = [''.join(self.lfr1[i]) for i in range(len(self.lfr1))]

        self.list_widget.addItems(self.lfr1)

        combo_index = self.combo.currentIndex()
        self.combo.clear()
        self.combo.addItems(dPars.grp)
        if combo_index == -1:
            combo_index = 0
        self.combo.setCurrentIndex(combo_index)
        self.statusBar().showMessage(str("Число участников - ") +
                                     str(dPars.increment) +
                                     str(" Записей в протоколе - ") +
                                     str(dPars.increment_pro1))



if __name__ == '__main__':

    dPars = Parser()

    app = QApplication(sys.argv)

    w = MainWindow()

    sys.exit(app.exec())

        #M=[bytes([x]) for x in S]
#s=str(M)
#s.decode()
#s=[x.decode('cp1251' , 'ignore') for x in s]
#print("total =", increment)
        #s =' '.join(map(str, L))
        #s=str(L)
        #s = s.decode('cp1251' , 'ignore')
        #print("name = ", L)  # [i:i+len]
        #print("name = ", M)  
        #d=d.split( '/n' )
        #M=[bytes([x]) for x in S]
#tf=str(tf)
#tf = tf.split(',')
#s = tf+s
#lf.sort()
#lf=str(lf)
#lf=lf.split( "'" )
#,key=lambda x:x[0:3]
#lf = str(lf)
#lf = (''.join(str(lf)))
#lf = ''.join(map(str, lf))
#lf = ''.join([str(element) for element in lf])
