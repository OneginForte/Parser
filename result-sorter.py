import os
#import struct
import sys

from Pro_parser import Parser

#from time import gmtime, strftime
#from tkinter import CENTER

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import ( QApplication, QComboBox, QFileDialog, QGridLayout, QListWidget,
                              QMessageBox, QPushButton, QVBoxLayout, QWidget)


class MainWindow(QtWidgets.QMainWindow):
    
    
    
    def __init__(self):
        self.lfr = ""
        self.sorted_rule = 0 # 3 - по имени, 7 - по результату, 2 - по группе. По умолчанию 0 - по стартовому номеру
        self.view_rule = 0 # 0 - все подряд, 1 - с номерами
        self.group_rule = 0 # Сортировка по номеру группы. 0 - все
        self.all_tabs = []

        self.grp1 = []
        self.grp2 = []
        self.grp3 = []
        self.pro1 = []
        self.pro2 = []
        self.pro3 = []
        self.grp_zag = []
        self.increment_grp1 = 0
        self.increment_grp2 = 0
        self.increment_grp3 = 0
        self.increment_pro = 0
        self.increment_pro1 = 0
        self.increment_pro2 = 0
        self.increment_pro3 = 0

        self.local_filename_choose1 = ''
        self.local_filename_choose2 = ''
        self.local_filename_choose3 = ''

        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon('Ski.ico'))
        self.setWindowTitle("Генератор итоговых результатов для Марафон-Электро.")
        self.cwd = os.getcwd() # Получить текущее местоположение файла программы
        #self.resize(1500, 1300)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

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
        
        self.btn_choose4 = QPushButton(self)  
        self.btn_choose4.setObjectName("Пустые")
        self.btn_choose4.setText("Показывать пустые")        
        self.btn_choose4.setCheckable(True)
        self.btn_choose4.setEnabled(False)
                
        
        self.btn_chooseFile1 = QPushButton(self)  
        self.btn_chooseFile1.setObjectName("Выбрать")
        self.btn_chooseFile1.setText("Открыть протокол 1")
        
        self.btn_chooseFile2 = QPushButton(self)  
        self.btn_chooseFile2.setObjectName("Выбрать")
        self.btn_chooseFile2.setText("Открыть протокол 2")
        self.btn_chooseFile2.setEnabled(False)
        
        self.btn_chooseFile3 = QPushButton(self)  
        self.btn_chooseFile3.setObjectName("Выбрать")
        self.btn_chooseFile3.setText("Открыть протокол 3")
        self.btn_chooseFile3.setEnabled(False)        

        self.btn_chooseFile4 = QPushButton(self)  
        self.btn_chooseFile4.setObjectName("Выбрать")
        self.btn_chooseFile4.setText("Сохранить итоговый протокол")
        self.btn_chooseFile4.setEnabled(False)

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
        self.btn_choose4.pressed.connect(self.slot_btn_choose4)
        self.btn_chooseFile1.clicked.connect(self.slot_btn_chooseFile1)
        self.btn_chooseFile2.clicked.connect(self.slot_btn_chooseFile2)
        self.btn_chooseFile3.clicked.connect(self.slot_btn_chooseFile3) 
        self.btn_chooseFile4.clicked.connect(self.slot_btn_chooseFile4)              
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
        self.left_layout.addWidget(self.btn_choose4)          
        self.left_layout.addWidget(self.btn_chooseFile1) #,alignment=QtCore.Qt.AlignTop
        self.left_layout.addWidget(self.btn_chooseFile2) 
        self.left_layout.addWidget(self.btn_chooseFile3)
        self.left_layout.addWidget(self.btn_chooseFile4)  
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
        self.setGeometry(500, 300, 1100, 500)
        #self.oldPos = self.pos()
        self.show()
 

    def clicked(self, item):
        QMessageBox.information(self, "Подробнее", "Участник номер: " + item.text(),QMessageBox.Ok)
    
    #def mousePressEvent(self, event):
    #    self.oldPos = event.globalPos()

    #def mouseMoveEvent(self, event):
        #delta = QPoint (event.globalPos() - self.oldPos)
        #self.move(self.x() + delta.x(), self.y() + delta.y())
        #self.oldPos = event.globalPos()

    def onComboSelected(self, index_val):
        self.group_rule=index_val    
        self.reload()
    
    def slot_btn_choose1(self): # 3 - по имени, 7 - по результату, 2 - по группе. По умолчанию 0 - по стартовому номеру
        #self.btn_choose1.setChecked(True)
        self.btn_choose2.setChecked(False)
        self.btn_choose3.setChecked(False)
        self.sorted_rule = 0
        self.reload()

    def slot_btn_choose2(self): # 3 - по имени, 7 - по результату, 2 - по группе. По умолчанию 0 - по стартовому номеру
        self.btn_choose1.setChecked(False)
        #self.btn_choose2.setChecked(True)
        self.btn_choose3.setChecked(False)
        self.sorted_rule = 3
        self.reload()
        
    def slot_btn_choose3(self): # 3 - по имени, 7 - по результату, 2 - по группе. По умолчанию 0 - по стартовому номеру   
        self.btn_choose1.setChecked(False)
        self.btn_choose2.setChecked(False)
        #self.btn_choose3.setChecked(True)
        self.sorted_rule = 7
        self.reload()

    def slot_btn_choose4(self): # 3 - по имени, 7 - по результату, 2 - по группе. По умолчанию 0 - по стартовому номеру   
        #self.btn_choose1.setChecked(False)
        #self.btn_choose2.setChecked(False)
        #self.btn_choose3.setChecked(True)
        if self.btn_choose4.isChecked():
            self.view_rule = 0
            self.reload()  
        else:
            self.view_rule = 1
            self.reload()        
         
    
    def slot_btn_chooseFile1(self):
        
        self.local_filename_choose1, filetype = QFileDialog.getOpenFileName(self,
                                   "Выбрать протокол 1",  
                                    self.cwd, # Начальный путь 
                                    "Pro Files (*.pro)")   # Установить фильтрацию расширений файлов, через двойную точку с запятой        
        
        if self.local_filename_choose1 == "":
            QMessageBox.warning(self, "Ошибка", "Не выбран протокол!",QMessageBox.Ok)
            return

        self.preload(self.local_filename_choose1)

        self.btn_choose1.setEnabled(True)
        self.btn_choose2.setEnabled(True)
        self.btn_choose3.setEnabled(True)
        self.btn_choose4.setEnabled(True)
        self.btn_chooseFile2.setEnabled(True)

    def slot_btn_chooseFile2(self):
        
        self.local_filename_choose2, filetype = QFileDialog.getOpenFileName(self,
                                   "Выбрать протокол 2",  
                                    self.cwd, # Начальный путь 
                                    "Pro Files (*.pro)")   # Установить фильтрацию расширений файлов, через двойную точку с запятой        
        
        if self.local_filename_choose2 == "" or self.local_filename_choose2==self.local_filename_choose1 :
            
            QMessageBox.warning(self, "Ошибка", "Выберете другой протокол",QMessageBox.Ok)
            return

        # Считаем файл протоколов. Возвращает блоки по 282 байт и число обработанных записей
        self.pro2, increment_pro_all2 = Parser.read_pro(
            dPars, self.local_filename_choose2)
        
        # Распакуем список групп и сами протоколы. Вернет списки и число годных записей. Список групп берет из первого протокола
        #self.lfr_grp1 = Parser.repack_grp(dPars, self.grp1)
        self.lfr_pro2, self.increment_pro2 = Parser.repack_pro(
            dPars, self.lfr_grp1, self.pro2, self.group_rule, 0)

        # Считаем файл протоколов. Возвращает блоки по 282 байт и число обработанных записей
        self.pro1, self.increment_pro = Parser.read_pro(
            dPars, self.local_filename_choose1)
        self.lfr_pro1, self.increment_pro1 = Parser.repack_pro(
            dPars, self.lfr_grp1, self.pro1, self.group_rule, 0)
        
        if self.increment_pro1 != self.increment_pro2:  # or self.increment_pro != increment_pro_all2
            QMessageBox.warning(
                self, "Ошибка", "Не совпадает число участников в протоколе", QMessageBox.Ok)
            self.local_filename_choose2 = ""
            self.pro2 = []
            self.lfr_pro2 = []
            return

        self.btn_chooseFile4.setEnabled(True)
        self.btn_chooseFile3.setEnabled(True)


        self.btn_choose2.setChecked(True)
        self.btn_choose2.setChecked(False)
        self.btn_choose3.setChecked(False)
        self.sorted_rule = 0

        # Теперь подготовим протоколы к сравнению и переносу результатов. Потом вынесем в отдельную функцию
        # Сортировка участников по нулевому столбцу
        #self.lfr_pro2 = Parser.sort(self, self.lfr_pro2)
        
        # Сортируем списки по нулевому полю
        lfr_pro1 = sorted(self.lfr_pro1)

        # Удаляем значения для сортировки
        # [(lfr_pro1[i].pop(0)) for i in range(len(lfr_pro1))]

        # Сортировка участников по нулевому столбцу
        #self.lfr_pro1 = Parser.sort(self, self.lfr_pro1)  
        # Сортируем списки по нулевому полю
        lfr_pro2 = sorted(self.lfr_pro2)

        # Удаляем значения для сортировки
        #[(lfr_pro2[i].pop(0)) for i in range(len(lfr_pro2))]

        for i in range(self.increment_pro1):
            if lfr_pro1[i][0] == lfr_pro2[i][0] or lfr_pro1[i][1] == lfr_pro2[i][1]:
                lfr_pro1[i].append(lfr_pro2[i][7])
                lfr_pro1[i].append(lfr_pro2[i][8])

        self.lfr_pro1 = [e.copy() for e in lfr_pro1]
        lfr_pro1 = sorted(lfr_pro1, key=lambda x: x[self.sorted_rule])

        [(lfr_pro1[i].pop(0)) for i in range(len(lfr_pro1))]
        [(lfr_pro1[i].pop(1)) for i in range(len(lfr_pro1))]
        [(lfr_pro1[i].pop(5)) for i in range(len(lfr_pro1))]
        [(lfr_pro1[i].pop(6)) for i in range(len(lfr_pro1))]

        # Преобразуем списки участников в чистый текст.
        lfr_pro1 = [''.join(lfr_pro1[i])
                   for i in range(len(lfr_pro1))]

        QListWidget.clear(self.list_widget)
        self.list_widget.addItems(lfr_pro1)
        self.combo.clear()
        self.combo.addItems(self.lfr_grp1)     


    def slot_btn_chooseFile3(self):        
        return

    def slot_btn_chooseFile4(self):    

        self.local_filename_choose4, filetype = QFileDialog.getSaveFileName(self,
                                   "Сохранить итоговый протокол",  
                                    self.cwd, # Начальный путь 
                                    "Pro Files (*.pro)")   # Установить фильтрацию расширений файлов, через двойную точку с запятой  

        if self.local_filename_choose4 == "" or self.local_filename_choose4==self.local_filename_choose1 or self.local_filename_choose4==self.local_filename_choose2 or self.local_filename_choose4==self.local_filename_choose3:
            
            QMessageBox.warning(self, "Ошибка", "Нельзя заменить входной протокол",QMessageBox.Ok)

                
        
    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()

    def preload(self, local_filename_choose):
        # Загрузим первый протокол, выведем список.
        self.increment_pro = 0
        self.increment_pro1 = 0

        filename_grp = local_filename_choose.rsplit('.', 1)[0] + '.grp'

        # Считаем файл групп
        self.grp_zag, self.grp1, self.increment_grp1 = Parser.read_grp(
            dPars, filename_grp)

        # Считаем файл протоколов. Возвращает блоки по 282 байт и число обработанных записей
        self.pro1, self.increment_pro = Parser.read_pro(
            dPars, local_filename_choose)
        
        # Распакуем список групп и сами протоколы. Вернет списки и число годных записей.
        self.lfr_grp1 = Parser.repack_grp(dPars, self.grp1)
        self.lfr_pro1, self.increment_pro1 = Parser.repack_pro(
            dPars, self.lfr_grp1, self.pro1, self.group_rule, self.view_rule)
        
        # Сортировка участников по нулевому столбцу
        #lfr_pro = Parser.sort(self, self.lfr_pro1)
        # Сортируем списки по нулевому полю, в зависимости от правила сортировки
        lfr_pro = [e.copy() for e in self.lfr_pro1]
        lfr_pro = sorted(lfr_pro, key=lambda x: x[self.sorted_rule])

        # Удаляем значения для сортировки
        [(lfr_pro[i].pop(0)) for i in range(len(lfr_pro))]
        [(lfr_pro[i].pop(1)) for i in range(len(lfr_pro))]
        [(lfr_pro[i].pop(5)) for i in range(len(lfr_pro))]

        # Преобразуем списки участников в чистый текст.
        lfr_pro = [''.join(lfr_pro[i])
                         for i in range(len(lfr_pro))]

        QListWidget.clear(self.list_widget)
        self.list_widget.addItems(lfr_pro)

        combo_index = self.combo.currentIndex()
        self.combo.clear()
        self.combo.addItems(self.lfr_grp1)
        if combo_index == -1:
            combo_index = 0
        self.combo.setCurrentIndex(combo_index)
        self.statusBar().showMessage(str("Число участников - ") +
                                     str(self.increment_pro1) +
                                     str(" Записей в протоколе - ") +
                                     str(self.increment_pro))

    def reload(self):

        # Распакуем список групп и сами протоколы. Вернет списки и число годных записей.
        self.lfr_grp1 = Parser.repack_grp(dPars, self.grp1)
        #self.lfr_pro1, self.increment_pro1 = Parser.repack_pro(
        #    dPars, self.lfr_grp1, self.pro1, self.group_rule, self.sorted_rule, self.view_rule)

        # Сортировка участников по нулевому столбцу
        #lfr_pro = Parser.sort(self, self.lfr_pro1)
        # Сортируем списки по нулевому полю, в зависимости от правила сортировки
        lfr_pro = [e.copy() for e in self.lfr_pro1]
        
        lfr_pro = sorted(lfr_pro, key=lambda x: x[self.sorted_rule])

        # Удаляем значения для сортировки
        [(lfr_pro[i].pop(0)) for i in range(len(lfr_pro))]
        [(lfr_pro[i].pop(1)) for i in range(len(lfr_pro))]
        [(lfr_pro[i].pop(5)) for i in range(len(lfr_pro))]

        # Преобразуем списки участников в чистый текст.
        lfr_pro = [''.join(lfr_pro[i])
                         for i in range(len(lfr_pro))]

        QListWidget.clear(self.list_widget)
        self.list_widget.addItems(lfr_pro)

        combo_index = self.combo.currentIndex()
        self.combo.clear()
        self.combo.addItems(self.lfr_grp1)
        if combo_index == -1:
            combo_index = 0
        self.combo.setCurrentIndex(combo_index)
        self.statusBar().showMessage(str("Число участников - ") +
                                     str(self.increment_pro1) +
                                     str(" Записей в протоколе - ") +
                                     str(self.increment_pro))


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
