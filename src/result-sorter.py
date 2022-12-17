import os
#import struct
import sys
from threading import Timer
from Pro_parser import Parser

#from time import gmtime, strftime
#from tkinter import CENTER

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import ( QApplication, QComboBox, QFileDialog, QGridLayout, QListWidget,
                              QMessageBox, QPushButton, QVBoxLayout, QWidget, QCheckBox, QSpinBox)


class SecondWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окна
        super().__init__(parent, QtCore.Qt.Window)
        self.mainLayout = QVBoxLayout()
        self.secondWin1()
 
    def secondWin1(self):
        check = QCheckBox('some text')
        self.mainLayout.addWidget(check)
        self.setLayout(self.mainLayout)


class PT():

    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()
        
    def stop(self):
        self.thread.cancel()

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.lfr = ""
        self.sorted_rule = 1 # 4 - по имени, 8 - по результату, 3 - по группе. По умолчанию 1 - по стартовому номеру.
        self.view_rule = 0 # 1 - все подряд, 0 - с номерами.
        self.group_rule = 0 # Сортировка по номеру группы. 0 - все.
        self.append_rule = 0 # Триггер для объединения результатов.
        self.autoreload = 0 # Триггер автообновления.
        self.autosave = 0 # Триггер автоматического сохранения.
        self.doublesave = 0 # Триггер сохранения двойного результата в один протокол.
        self.reload_timer = 10
        self.all_tabs = []

        self.grp1 = []
        self.grp2 = []
        self.grp3 = []
        self.pro1 = []
        self.pro2 = []
        self.pro3 = b''
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
        self.local_filename_choose4 = ''
        
        self.mainWin1 ()

    def mainWin1 (self):
        
        self.setWindowIcon(QtGui.QIcon('src/Ski.ico'))
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
        self.btn_choose1.setObjectName("Стартовый номер")  
        self.btn_choose1.setText("Стартовый номер")
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
                
        self.btn_choose5 = QPushButton(self)
        self.btn_choose5.setObjectName("Генератор")
        self.btn_choose5.setText("Сгенерировать итоговый")
        #self.btn_choose5.setCheckable(True)
        self.btn_choose5.setEnabled(False)
        
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

        self.text1 = QtWidgets.QLabel("  №                            Участник                                                                         Цех                                    г.р.                             Группа                                    Резульат1     Результат2     Итоговый")
        self.text2 = QtWidgets.QLabel("Сортировка",
                                    alignment=QtCore.Qt.AlignCenter)
        self.text3 = QtWidgets.QLabel("Группы",
                                    alignment=QtCore.Qt.AlignCenter)

        self.checkbox1 = QCheckBox('Обновлять автоматически', self)
        self.checkbox2 = QCheckBox('Сохранять автоматически', self)
        self.checkbox2.setEnabled(False)
        self.checkbox3 = QCheckBox('Складывать оба результата', self)
        self.checkbox3.setEnabled(False)
        #self.checkbox1.toggle()

        self.spinbox1 = QSpinBox(self)
        self.spinbox1.setRange(1, 60)
        self.spinbox1.setValue(5)
        self.spinbox1.setSuffix(' сек.')
        self.spinbox1.setFixedWidth(65)

        self.combobox1 = QComboBox(self)
        self.combobox1.setFixedWidth(165)
        self.combobox1.hidePopup()
        
        
        self.right_layout = QVBoxLayout()
      
        #self.setLayout(self.right_layout)
        
        self.left_layout = QVBoxLayout()
   
        #self.setLayout(self.left_layout)
        
        self.btn_choose1.pressed.connect(self.slot_btn_choose1) 
        self.btn_choose2.pressed.connect(self.slot_btn_choose2) 
        self.btn_choose3.pressed.connect(self.slot_btn_choose3)
        self.btn_choose4.pressed.connect(self.slot_btn_choose4)
        self.btn_choose5.pressed.connect(self.slot_btn_choose5)
        self.btn_chooseFile1.clicked.connect(self.slot_btn_chooseFile1)
        self.btn_chooseFile2.clicked.connect(self.slot_btn_chooseFile2)
        self.btn_chooseFile3.clicked.connect(self.slot_btn_chooseFile3) 
        self.btn_chooseFile4.clicked.connect(self.slot_btn_chooseFile4)              
        self.list_widget.itemClicked.connect(self.clicked)
        self.combobox1.activated[int].connect(self.onCombo1Selected)
        self.checkbox1.stateChanged.connect(self.checkBox_1)
        self.checkbox2.stateChanged.connect(self.checkbox_2)
        self.checkbox3.stateChanged.connect(self.checkbox_3)
        self.spinbox1.valueChanged.connect(self.spinBox_1)
       
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
        self.left_layout.insertSpacing(10, 20)
        self.left_layout.addWidget(self.btn_chooseFile1) #,alignment=QtCore.Qt.AlignTop
        self.left_layout.addWidget(self.btn_chooseFile2) 
        self.left_layout.addWidget(self.btn_chooseFile3)
        self.left_layout.insertSpacing(10, 10)
        self.left_layout.addWidget(self.checkbox1)
        self.left_layout.addWidget(self.spinbox1)
        self.left_layout.addWidget(self.btn_choose5)
        self.left_layout.addWidget(self.btn_chooseFile4)
        self.left_layout.addWidget(self.checkbox2)
        self.left_layout.addWidget(self.checkbox3)
        self.left_layout.insertSpacing(10, 20)
        self.left_layout.addWidget(self.text3)
        self.left_layout.addWidget(self.combobox1)

        self.left_layout.addStretch()

        grid.addLayout(self.left_layout, 0, 0 , 
                       alignment=QtCore.Qt.AlignLeft) 
        
        grid.addLayout(self.right_layout, 0, 1, 0, 1, 
                       alignment=QtCore.Qt.AlignRight) 

        #grid.addWidget(self.list_widget, 0, 1, 20, 20)      
        
        #tempFrame.addWidget(grid)
        #centralWidget.addWidget(tempFrame)
        
        centralWidget.setLayout(grid)
        self.setGeometry(500, 300, 1200, 500)
        #self.oldPos = self.pos()
        
        self.show()
 
    def reload(self):
           
        # Считаем файл групп
        self.grp_zag, self.grp1, self.increment_grp1 = Parser.read_grp(
            dPars, self.local_filename_choose1)
        
        # Считаем файл протоколов. Возвращает raw binary блоки по 282 байт и число обработанных записей
        self.pro1, self.increment_pro = Parser.read_pro(
            dPars, self.local_filename_choose1)

        # Распакуем список групп и сами протоколы. Вернет списки и число годных записей. 
        # Зависимость от group_rule - сортировка по номеру группы, 0 - все, и view_rule - 1 - все подряд, 0 - с номерами.
        self.lfr_grp1 = Parser.repack_grp(dPars, self.grp1)
        self.lfr_pro1, self.increment_pro1 = Parser.repack_pro(
            dPars, self.lfr_grp1, self.pro1, self.group_rule, self.view_rule)
        
        # Сортируем списки по нулевому полю
        lfr_pro1 = sorted(self.lfr_pro1)

        # Если у нас открыт второй протокол, то объединям результаты в один общий.
        if self.local_filename_choose2!= "":
            
            # Считаем файл групп.
            self.grp_zag2, self.grp2, self.increment_grp2 = Parser.read_grp(
                dPars, self.local_filename_choose2)

            # Есть вероятность, что это идентичные протоколы.
            # Считаем файл протоколов.Возвращает raw binary блоки по 282 байт и число обработанных записей.
            self.pro2, increment_pro_all2 = Parser.read_pro(
                dPars, self.local_filename_choose2)

            # Распакуем список групп и сами протоколы. Вернет списки и число годных записей. Список групп берем из первого протокола, как основного.
            # Зависимость от group_rule - сортировка по номеру группы, 0 - все, и view_rule - 1 - все подряд, 0 - с номерами.
            # Важно, чтобы возвращаемые self.increment_pro1 и self.increment_pro2 совпадали, иначе не сработает объединение.
            self.lfr_grp2 = Parser.repack_grp(dPars, self.grp2)
            self.lfr_pro2, self.increment_pro2 = Parser.repack_pro(
                dPars, self.lfr_grp1, self.pro2, self.group_rule, self.view_rule)


            # Сортируем списки по нулевому полю
            lfr_pro2 = sorted(self.lfr_pro2)
            self.pro3 = b''
            
            lfr_pro1 = self.append_pro_result (lfr_pro1, lfr_pro2)

            # Запишем получившийся binary протокол.
            if self.local_filename_choose4 != "" and self.autosave == 1:
                self.saveprot (self.pro3)
        
        lfr_pro = [e.copy() for e in self.lfr_pro1]

        lfr_pro_t = self.pro_grp_sort(lfr_pro, self.lfr_grp1)

        QListWidget.clear(self.list_widget)
        
        lfr_pro_t = self.pro_preapare (lfr_pro_t)
        
        len_lfr = len(lfr_pro_t)    

        #lfr_pro_t.insert(
        #    0, '№         Участник\t\t    Цех\t\tг.р.\t   Группа         Резульат1   Результат2   Итоговый')

        self.list_widget.addItems(lfr_pro_t)

        combo_index = self.combobox1.currentIndex()
        self.combobox1.clear()

        lfr_grp = [e.copy() for e in self.lfr_grp1]

        lfr_grp = self.group_prepare (lfr_grp)
        
        self.combobox1.addItems(lfr_grp)
        if combo_index == -1:
            combo_index = 0
        self.combobox1.setCurrentIndex(combo_index)
        self.statusBar().showMessage(str("Число участников - ") +
                                     str(len_lfr) +  #self.increment_pro1
                                     str(" Записей в протоколе - ") +
                                     str(self.increment_pro))
   
    
    def saveprot(self, prot):
        if self.local_filename_choose4 != "" and len(prot)>0:
            dPars.save_pro(self.local_filename_choose4, prot)
 
    def append_pro_result (self, lfr_pro1, lfr_pro2):
        # Обьединим результаты. Проверка по стартовому номеру и имени.
        for i in range(len(lfr_pro1)):
            if lfr_pro1[i][0] == lfr_pro2[i][0] \
                or lfr_pro1[i][1] == lfr_pro2[i][1]:
                # Загрузка финишей второго протокола в общий
                lfr_pro1[i].append(lfr_pro2[i][8])
                lfr_pro1[i].append(lfr_pro2[i][9])
                   # Сравнение результатов первого протокола и второго.
                   # Вывод результата, в зависимости в протоколе нулевой.
                   # Если в первом протоколе результат нулевой, принимаем результат второго протокола как финишный
                   # Если нулевой результат во втором протоколе, то вероятно второй протокол еще не заполнился.
                   # Принудительная фиксация результатов по флагу self.append_rule

                if lfr_pro1[i][8] >= lfr_pro1[i][10]:
                        if self.doublesave == 1:
                            self.pro3 += self.pro1[(lfr_pro1[i][0])][1]
                        else: 
                            lfr_pro1[i].append(lfr_pro1[i][10])
                            lfr_pro1[i].append(lfr_pro1[i][11])
                        self.pro3 += self.pro2[(lfr_pro2[i][0])][1]
                elif (lfr_pro1[i][8] <= lfr_pro1[i][10] and lfr_pro1[i][10] != 4294967295) or \
                        self.append_rule == 1:
                        self.pro3 += self.pro1[(lfr_pro1[i][0])][1] 
                        if self.doublesave == 1:
                            self.pro3 += self.pro2[(lfr_pro2[i][0])][1]
                        else:
                            lfr_pro1[i].append(lfr_pro1[i][8])
                            lfr_pro1[i].append(lfr_pro1[i][9])
                            
                else:
                        if self.doublesave == 1:
                            self.pro3 += self.pro1[(lfr_pro1[i][0])][1]
                        else:
                            lfr_pro1[i].append(4294967295)
                            lfr_pro1[i].append(' 00:00:00,00')
                        self.pro3 += self.pro2[(lfr_pro2[i][0])][1]

                
                #if lfr_pro1[i][8] >= lfr_pro1[i][10]:
                #    lfr_pro1[i].append(lfr_pro1[i][10])
                #    lfr_pro1[i].append(lfr_pro1[i][11])
                #    self.pro3 = self.pro3 + \
                #        self.pro2[(lfr_pro2[i][0])][1]
                #elif (lfr_pro1[i][8] <= lfr_pro1[i][10] and lfr_pro1[i][10] != 4294967295) or \
                #        self.append_rule == 1:
                #    lfr_pro1[i].append(lfr_pro1[i][8])
                #    lfr_pro1[i].append(lfr_pro1[i][9])
                #    self.pro3 = self.pro3 + \
                #        self.pro1[(lfr_pro1[i][0])][1]
                #else:
                #    lfr_pro1[i].append(4294967295)
                #    lfr_pro1[i].append(' 00:00:00,00')
                #    self.pro3 = self.pro3 + \
                #        self.pro2[(lfr_pro2[i][0])][1]
                    # if lfr_pro1[i][8] == 4294967295 or lfr_pro1[i][10] == 4294967295:
                        # lfr_pro1[i].append(lfr_pro1[i][10])
                        # lfr_pro1[i].append(lfr_pro1[i][11])
                        # self.pro3 = self.pro3 + \
                        # self.pro2[(lfr_pro2[i][0])][1]

                           #lfr_pro1[i].append(lfr_pro1[i][8])
                           #lfr_pro1[i].append(lfr_pro1[i][9])
                           #self.pro3 = self.pro3 + self.pro1[(lfr_pro1[i][0])][1]

        return lfr_pro1
    
    def group_prepare(self, lfr_grp):
     # ['Все', 1, '0', 0, 255, '0']
        for i in range(2, len(lfr_grp)):
            lfr_grp[i][0] = lfr_grp[i][0]+lfr_grp[i][2]

        [(lfr_grp[i].pop(1)) for i in range(len(lfr_grp))]
        [(lfr_grp[i].pop(1)) for i in range(len(lfr_grp))]
        [(lfr_grp[i].pop(1)) for i in range(len(lfr_grp))]
        [(lfr_grp[i].pop(1)) for i in range(len(lfr_grp))]
        [(lfr_grp[i].pop(1)) for i in range(len(lfr_grp))]

        lfr_grp = [''.join(lfr_grp[i])
                   for i in range(len(lfr_grp))]
        return lfr_grp

    def pro_preapare(self, lfr_pro_t):
        
        # Удаляем лишние поля перед сортировкой, при условии, что список не пустой.
        if len(lfr_pro_t) > 0:
            [(lfr_pro_t[i].pop(0)) for i in range(len(lfr_pro_t))]
            [(lfr_pro_t[i].pop(0)) for i in range(len(lfr_pro_t))]
            [(lfr_pro_t[i].pop(1)) for i in range(len(lfr_pro_t))]
            [(lfr_pro_t[i].pop(5)) for i in range(len(lfr_pro_t))]
            if len(lfr_pro_t[0]) > 6 and self.group_rule != 1:
                [(lfr_pro_t[i].pop(6)) for i in range(len(lfr_pro_t))]
                if len(lfr_pro_t[0]) > 7 and self.group_rule != 1:
                    [(lfr_pro_t[i].pop(7)) for i in range(len(lfr_pro_t))]

            # Преобразуем списки участников в чистый текст.
            lfr_pro_t = [''.join(lfr_pro_t[i])
                         for i in range(len(lfr_pro_t))]
        return lfr_pro_t

    def pro_grp_sort(self, lfr_pro, lfr_grp):
        
        lfr_pro_t = ()
        # Выборка участников по группам
        if self.group_rule>0:
            # Сортируем списки по третьему полю
            lfr_pro = sorted(lfr_pro, key=lambda x: x[3])
            # Проверим на результирующую группу

            if lfr_grp[self.group_rule][4]==255: 
                
                for i in range(1, len(lfr_grp)):
                    # Выборка между группами                    
                    lenlfr=len(lfr_pro)
                    for k in reversed(lfr_pro):
                        lenlfr = lenlfr-1
                        if k[3] == i and lfr_grp[i][4] == self.group_rule:
                            lfr_pro_t+=(k,)
                            
            else:
                lenlfr = len(lfr_pro)
                for k in reversed(lfr_pro):
                    lenlfr = lenlfr-1
                    if k[3] == self.group_rule:
                        lfr_pro_t+=(k,)
                        
            
            # Сортируем списки. 4 - по имени, 8 - по результату, 3 - по группе. По умолчанию 1 - по стартовому номеру
            lfr_pro_t = sorted(
                lfr_pro_t, key=lambda x: x[self.sorted_rule])
        else:        
            # Сортируем списки. 4 - по имени, 8 - по результату, 3 - по группе. По умолчанию 1 - по стартовому номеру
            lfr_pro_t = sorted(
                lfr_pro, key=lambda x: x[self.sorted_rule])
        
        return lfr_pro_t


    #@pyqtSlot()
    def clicked(self, item):
        QMessageBox.information(
            self, "Подробнее", "Участник номер: " + item.text(), QMessageBox.Ok)

    def checkBox_1(self, state):
       if state == Qt.Checked:
            self.autoreload = 1            
            t.start()
       else:
            self.autoreload = 0
            t.stop()

    def checkbox_2(self, state):
        if state == Qt.Checked:
            self.autosave = 1
        else:
            self.autosave = 0

    def checkbox_3(self, state):
        if state == Qt.Checked:
            self.doublesave = 1
        else:
            self.doublesave = 0
            

    def spinBox_1(self):
        self.reload_timer = self.spinbox1.value()

    # def mousePressEvent(self, event):
    #    self.oldPos = event.globalPos()

    # def mouseMoveEvent(self, event):
        #delta = QPoint (event.globalPos() - self.oldPos)
        #self.move(self.x() + delta.x(), self.y() + delta.y())
        #self.oldPos = event.globalPos()

    def onCombo1Selected(self, index_val):
        self.group_rule = index_val
        self.reload()

    # 4 - по имени, 8 - по результату, 3 - по группе. По умолчанию 1 - по стартовому номеру
    def slot_btn_choose1(self):
        # self.btn_choose1.setChecked(True)
        self.btn_choose2.setChecked(False)
        self.btn_choose3.setChecked(False)
        self.sorted_rule = 1
        self.reload()

    # 4 - по имени, 8 - по результату, 3 - по группе. По умолчанию 1 - по стартовому номеру
    def slot_btn_choose2(self):
        self.btn_choose1.setChecked(False)
        # self.btn_choose2.setChecked(True)
        self.btn_choose3.setChecked(False)
        self.sorted_rule = 4
        self.reload()

    # 4 - по имени, 8 - по результату, 3 - по группе. По умолчанию 1 - по стартовому номеру
    def slot_btn_choose3(self):
        self.btn_choose1.setChecked(False)
        self.btn_choose2.setChecked(False)
        # self.btn_choose3.setChecked(True)
        self.sorted_rule = 8
        self.reload()

    # 4 - по имени, 8 - по результату, 3 - по группе. По умолчанию 1 - по стартовому номеру
    def slot_btn_choose4(self):
        # self.btn_choose1.setChecked(False)
        # self.btn_choose2.setChecked(False)
        # self.btn_choose3.setChecked(True)
        if self.btn_choose4.isChecked():
            self.view_rule = 0
            self.reload()
        else:
            self.view_rule = 1
            self.reload()

    def slot_btn_choose5(self):
        mess = QMessageBox.question(
            self, "Внимание!", "Вы точно уверены?", QMessageBox.No | QMessageBox.Ok)
        if mess == QMessageBox.Ok:
            self.append_rule = 1
            self.reload()
     
        if mess == QMessageBox.No: 
            self.append_rule = 0
            self.reload()
            
        

    def slot_btn_chooseFile1(self):

        old_file = self.local_filename_choose1

        if self.local_filename_choose1 != "":
            old_file = self.local_filename_choose1
        self.local_filename_choose1, filetype = QFileDialog.getOpenFileName(self,
                                                                            "Выбрать протокол 1",
                                                                            self.cwd,  # Начальный путь
                                                                            "Pro Files (*.pro)")   # Установить фильтрацию расширений файлов, через двойную точку с запятой

        if self.local_filename_choose1 == "":
            QMessageBox.warning(
                self, "Ошибка", "Не выбран протокол!", QMessageBox.Ok)
            if old_file != "":
               self.local_filename_choose1 = old_file
            return

        grp_zag, grp1, increment_grp1 = Parser.read_grp(
            dPars, self.local_filename_choose1)
        
        if increment_grp1 == 0:
            QMessageBox.warning(
                self, "Ошибка", "Данный протокол не имеет файла групп!", QMessageBox.Ok)
            self.local_filename_choose1 = ""
            return
        
        pro1, increment_pro1 = Parser.read_pro(
            dPars, self.local_filename_choose1)
        if increment_pro1 == 0:
            QMessageBox.warning(
                self, "Ошибка", "Это пустой протокол!", QMessageBox.Ok)
            self.local_filename_choose1 = ""
            return
        
        self.cwd =  self.local_filename_choose1.rsplit('.', 1)[0] 
        self.local_filename_choose2 = ""
        self.append_rule = 0
        
        self.btn_choose1.setEnabled(True)
        self.btn_choose2.setEnabled(True)
        self.btn_choose3.setEnabled(True)
        self.btn_choose4.setEnabled(True)
        self.btn_choose5.setEnabled(False)
        self.checkbox2.setEnabled(False)
        self.checkbox3.setCheckState(False)
        self.checkbox3.setEnabled(False)
        self.btn_chooseFile2.setEnabled(True)
        self.btn_chooseFile4.setEnabled(False)

        self.reload()

    def slot_btn_chooseFile2(self):

        old_file = self.local_filename_choose2

        if self.local_filename_choose1 != "":
            old_file = self.local_filename_choose1
        self.local_filename_choose2, filetype = QFileDialog.getOpenFileName(self,
                                                                            "Выбрать протокол 2",
                                                                            self.cwd,  # Начальный путь
                                                                            "Pro Files (*.pro)")   # Установить фильтрацию расширений файлов, через двойную точку с запятой

        if self.local_filename_choose2 == "" or self.local_filename_choose2 == self.local_filename_choose1:
            QMessageBox.warning(
                self, "Ошибка", "Выберете другой протокол!", QMessageBox.Ok)
            if old_file != "":
               self.local_filename_choose2 = old_file
            return

        filename_grp = self.local_filename_choose2.rsplit('.', 1)[0] + '.grp'

        # Считаем файл групп.
        grp_zag2, grp2, increment_grp2 = Parser.read_grp(
            dPars, filename_grp)
        if increment_grp2 == 0:
            QMessageBox.warning(
                self, "Ошибка", "Данный протокол не имеет файла групп!", QMessageBox.Ok)
            self.local_filename_choose1 = ""
            return

        # Проверим по нему, имеет вообще смысл дальше разбирать протокол.
        if increment_grp2 != self.increment_grp1:
            QMessageBox.warning(
                self, "Ошибка", "Не совпадают файлы групп!", QMessageBox.Ok)
            self.local_filename_choose2 = ""
            return

        # Здесь мы думаем, что есть вероятность, что протоколы идентичны по структуре.
        # Считаем файл протоколов.Возвращает raw binary блоки по 282 байт и число обработанных записей.
        pro2, increment_pro_all2 = Parser.read_pro(
            dPars, self.local_filename_choose2)
        if increment_pro_all2 == 0:
            QMessageBox.warning(
                self, "Ошибка", "Это пустой протокол!", QMessageBox.Ok)
            self.local_filename_choose2 = ""
            return

        # Распакуем список групп и сами протоколы. Вернет списки и число годных записей.
        grp2 = Parser.repack_grp(dPars, grp2)
        lfr_pro2, increment_pro2 = Parser.repack_pro(
            dPars, grp2, pro2, self.group_rule, 0)

        # Проверим число участников. Протоколы не будут обратываться при не совпадении числа участников.
        if self.increment_pro1 != increment_pro2:  # or self.increment_pro != increment_pro_all2
            QMessageBox.warning(
                self, "Ошибка", "Не совпадает число участников в протоколе!", QMessageBox.Ok)
            self.local_filename_choose2 = ""
            self.pro2 = []
            self.lfr_pro2 = []
            return

        self.btn_chooseFile3.setEnabled(False)
        self.btn_chooseFile4.setEnabled(True)
        self.btn_choose1.setChecked(True)
        self.btn_choose2.setChecked(False)
        self.btn_choose3.setChecked(False)
        self.btn_choose5.setEnabled(True)
        self.checkbox3.setEnabled(True)
        # Теперь подготовим протоколы к сравнению и объединению результатов. Обновим виджеты в окне.
        self.reload()
        
        

    def slot_btn_chooseFile3(self):
        return

    def slot_btn_chooseFile4(self):

        self.local_filename_choose4, filetype = QFileDialog.getSaveFileName(self,
                                                                            "Выбрать файл итогового протокола",
                                                                            self.cwd,  # Начальный путь
                                                                            "Pro Files (*.pro)")   # Установить фильтрацию расширений файлов, через двойную точку с запятой

        if self.local_filename_choose4 == self.local_filename_choose1 or self.local_filename_choose4 == self.local_filename_choose2:
            QMessageBox.warning(
                self, "Ошибка", "Нельзя заменить входной протокол", QMessageBox.Ok)
            
            return

        if self.local_filename_choose4 == "":
            return
        self.checkbox2.setEnabled(True)
        self.reload()
        if len(self.pro3) != 0 and self.autosave != 1:
            self.saveprot(self.pro3)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':

    dPars = Parser()
    

    app = QApplication(sys.argv)

    w = MainWindow()
    t = PT(w.reload_timer, w.reload)
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
