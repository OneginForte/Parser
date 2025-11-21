import os
#import struct
import sys
from threading import Timer
from time import sleep
import struct
from operator import itemgetter
from Pro_parser import Parser

#from time import gmtime, strftime
#from tkinter import CENTER

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect, pyqtSlot
from PyQt5.QtGui import QPainter, QFont, QColor, QPalette, QPixmap
from PyQt5.QtWidgets import ( QApplication, QComboBox, QFileDialog, QGridLayout, QListWidget,
                              QMessageBox, QPushButton, QVBoxLayout, QWidget, QCheckBox, QSpinBox)


class SecondWindow(QtWidgets.QWidget):
    viewText = pyqtSignal(list)
    
    
    
    def __init__(self, parent=None):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окно
        
        super().__init__(parent)
        self._parent = parent
        self.start = 0
        self._viewText = list()
        self._viewMode = 0 # Режим вывода. 0 - стартовый протокол. 1 - результаты 
        self._temp_viewMode = 0
        self._viewLoop = 0
        self._viewWindow = [[0],[0]]
        self._viewWindowHigh = 6
        self._viewCount1 = 1
        self._viewCount2 = 0
        self._viewCount3 = self._viewWindowHigh
        self.time = 0
        self.time_step = 35 #0.025
        self.timer_id = self.startTimer(200)
        self._top = 0
        self._left = 0
        self._width = 200
        self._height = 100
        self.image = QPixmap(r"evraz30.bmp")
        self._text1 = '"Треугольник"'
        self.secondWin1()
    
    @QtCore.pyqtProperty(list, notify=viewText)
    def updateSecondWin (self):
        return self._viewText
    
    @updateSecondWin.setter
    def updateSecondWin (self, text):
        
        self._viewText = text
        self.viewText.emit(text)
        self._temp_viewMode = self._viewMode
        _viewMode = self._viewText.pop(0)
        if _viewMode//10 and self._temp_viewMode == _viewMode%10:
            self._temp_viewMode = _viewMode%10
            _viewMode = 0
        else:
            _viewMode = _viewMode % 10
        self._left = self._viewText.pop(0)
        self._top = self._viewText.pop(0)
        if  _viewMode != 0:
            self._viewMode = _viewMode
            self.killTimer(self.timer_id)
            self._viewLoop = 1
            self.start = 1
            self.time_step = 35
            self._viewCount1 = 1
            self._viewCount2 = 0
            self._viewCount3 = self._viewWindowHigh
            self.time = 0
            self.timer_id = self.startTimer(200)
            #self.update()
        else: 
            self._viewMode = self._temp_viewMode

    def secondWin1(self):
                      
        self.setGeometry( self._top, self._left, self._width ,self._height )
        #self.mapToGlobal( QPoint(self._top, self._left))
        #self.setWindowTitle('Draw text')
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint)
        pal = self.palette()
        pal.setColor(QPalette.Background, Qt.black)
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("plastique"))
        #self.changePalette()
        self.resize(self._width ,self._height)
        
        self.show()


    def paintEvent(self, param):
        qp = QPainter(self)
        
        #if not self._viewText:
            
            #self.qp.begin(self)
        #    qp.drawPixmap(self.rect(), self.image)

        #self.qp.begin(self)
        #qp.setRenderHints(QPainter.Antialiasing)
        #if self._viewText:
            
            #qp.drawPixmap(self.rect(), self.image)

        if self._viewLoop == 1:
               
                qp.save()
                #self.qp = QPainter(self)
                #self.qp.begin(self) 
                self._drawText(qp, param)
                #self.qp.end()
                qp.restore()

        qp.end()
        #self.update()

    def _drawText(self, qp, param):

        #if self._viewText[0] == 0 or self._viewText[0] == 1 or self._viewText[0] == 2 or self._viewText[0] == 3:
   
        if self.start == 1: #len(self._viewText) != 0 and 

            if self._viewMode == 1:
                self.viewMode1(qp)
            if self._viewMode == 2:  # self._viewMode == 1:
                self.viewMode2(qp)
            if self._viewMode == 3:
                self.viewMode3(qp)
            if self._viewMode == 4:
                self.viewMode4(qp)
            if self._viewMode == 5:
                self.viewMode5(qp)
                 
                        #self._viewCount2 += self._viewCount3 
                        #self.time += self.time_step
                        #self.time += self.time_step
                        #self._viewCount2 += self._viewCount3    
                        # self._viewWindow[[0],[0]]
                        #self.time += self.time_step
                        #self.time += self.time_step                    
                        #self.time += self.time_step
        else:
            self.start = 0
            #self.qp.eraseRect ( self.top, self.left, self.width ,self.height )
            
    def timerEvent(self, event):
        if self.timer_id == event.timerId() and self.start == 1:
            if self.time == 0:
                self.update() 
            else: 
                self.time -= 1
    
    def viewMode1(self, qp):
        # self.qp.eraseRect(self._top, self._left, self._width, self._height)
        qp.setFont(QFont('Arial', 10))
        qp.setPen(QColor('white'))
        self._text2 = 'Протокол старта:'
        qp.drawText(QRect(0, 0, self._width, 18),Qt.AlignCenter, self._text1)
        qp.drawText(QRect(0, 18, self._width, 18), Qt.AlignCenter, self._text2)
        _text_indent = 52
        _nr_indent = 0
        _name_indent = 30
        _name_size = 30
        _comand_indent = 231
        _comand_size = 12
        _result_indent = 257
        _text_hight = 14
        qp.setFont(QFont('Arial', 10))
        qp.setPixelSize(10)
        qp.setPen(QColor('green'))

        for i in range(0,self._viewCount1):
            if (self._viewCount2+i) == (len(self._viewText)):
                break
                    # lfr_grp[i].pop(1)
            qp.drawText(_nr_indent, (i*_text_hight) + _text_indent,
                                self._viewText[self._viewCount2+i][0])
            txt = [self._viewText[self._viewCount2+i][1][k]
                           for k in range(_name_size) if len(self._viewText[self._viewCount2+i][1]) > k]
            txt = ''.join([str(element) for element in txt])

            qp.drawText(_name_indent, (i*_text_hight) + _text_indent, txt)

            txt = [self._viewText[self._viewCount2+i][2][k]
                            for k in range(_comand_size) if len(self._viewText[self._viewCount2+i][2]) > k]
            txt = ''.join([str(element) for element in txt])

            qp.drawText(_comand_indent, (i*_text_hight) + _text_indent, txt)

        if (self._viewCount2 + self._viewWindowHigh) > (len(self._viewText)):

            self._viewCount3 = (
                (len(self._viewText)) - self._viewCount2)

        if (self._viewCount2+self._viewCount1) == (len(self._viewText)):
            self._viewCount1 = 1
            self._viewCount2 = 0
            self._viewCount3 = self._viewWindowHigh
            self.time += self.time_step

        elif self._viewCount1 == self._viewCount3:
            self._viewCount1 = 1
            self._viewCount2 += self._viewWindowHigh
            self._viewCount3 = self._viewWindowHigh
            self.time += self.time_step
        else:
            self._viewCount1 += 1
       
    def viewMode2(self, qp):
        qp.setPen(QColor('white'))
        qp.setFont(QFont('Arial', 10))
        #self._text1 = '        Открытие лыжного сезона 2024'
        self._text2 = 'Текущие результаты команд:'
        _text_indent = 29
        _nr_indent = 0
        _name_indent = 25
        _name_size = 35
        _comand_indent = 111
        _comand_size = 8
        _result_indent = 140
        _text_hight = 14
        qp.drawText(QRect(0, 0, self._width, 18),Qt.AlignCenter, self._text1)
        #qp.drawText(QRect(0, 18, self._width, 18), Qt.AlignCenter, self._text2)
                
        for i in range(self._viewWindowHigh):
                    if i == len(self._viewText):
                        break
                    M = i+1
                    M = str(M)
                    txt = ''.join([str(element) for element in M])
                    M = int(txt)
                    if M < 100:
                        txt = " " + txt 
                    if M < 10:
                        txt = " " + txt  
               
                    qp.setPen(QColor('yellow'))
                    qp.drawText(0, (i*_text_hight)+_text_indent,txt)
                                        
                    qp.setPen(QColor('green'))                 
                    txt = [self._viewText[i][0][k]
                           for k in range(_name_size) if len(self._viewText[i][0]) > k]
                    txt = ''.join([str(element) for element in txt])
                    qp.drawText(_name_indent, (i*_text_hight)+_text_indent, txt)
                    
                    qp.setPen(QColor('red'))
                    qp.drawText(_result_indent, (i*_text_hight)+_text_indent, self._viewText[i][1])  
                    
                    

    def viewMode3(self, qp):
            # self.qp.eraseRect(self._top, self._left, self._width, self._height)
        qp.setFont(QFont('Arial', 10))
        qp.setPen(QColor('white'))
        #self._text1 = '          Спортивный забег "Пять Вершин"'
        self._text2 = 'Протокол финиша абсолют:'
        qp.drawText(QRect(0, 0, self._width, 18),Qt.AlignCenter, self._text1)
        #qp.drawText(QRect(0, 18, self._width, 18), Qt.AlignCenter, self._text2)
        _text_indent = 29
        _nr_indent = 20
        _name_indent = 41
        _name_size = 11
        _comand_indent = 119
        _comand_size = 4
        _result_indent = 149
        _text_hight = 14
        qp.setFont(QFont('Arial', 10))
        for i in range(0, self._viewCount1):
            if i == len(self._viewText):
                break
            M = self._viewCount2+i+1
            M = str(M)
            txt = ''.join([str(element) for element in M])
            M = int(txt)
            if M < 100:
               txt = " " + txt 
            if M < 10:
               txt = " " + txt  
               
            qp.setPen(QColor('yellow'))
            qp.drawText(0, (i*_text_hight)+_text_indent,txt)

            qp.setPen(QColor('green'))
            # lfr_grp[i].pop(1)
            qp.drawText(_nr_indent, (i*_text_hight)+_text_indent,
                        self._viewText[self._viewCount2+i][0])
            #txt = self._viewText[i][1]
            txt = [self._viewText[self._viewCount2+i][1][k]
                   for k in range(_name_size) if len(self._viewText[self._viewCount2+i][1]) > k]
            txt = ''.join([str(element) for element in txt])
            qp.drawText(_name_indent, (i*_text_hight)+_text_indent, txt)
            txt = [self._viewText[self._viewCount2+i][2][k]
                   for k in range(_comand_size) if len(self._viewText[self._viewCount2+i][2]) > k]
            txt = ''.join([str(element) for element in txt])
            qp.drawText(_comand_indent, (i*_text_hight)+_text_indent, txt)
            qp.setPen(QColor('red'))
            qp.drawText(_result_indent, (i*_text_hight)+_text_indent,
                        self._viewText[self._viewCount2+i][3])
            
        if (self._viewCount2 + self._viewWindowHigh) > (len(self._viewText)):

            self._viewCount3 = (
                (len(self._viewText)) - self._viewCount2)

        if (self._viewCount2+self._viewCount1) == (len(self._viewText)):
            self._viewCount1 = 1
            self._viewCount2 = 0
            self._viewCount3 = self._viewWindowHigh
            self.time += self.time_step

        elif self._viewCount1 == self._viewCount3:
            self._viewCount1 = 1
            self._viewCount2 += self._viewWindowHigh
            self._viewCount3 = self._viewWindowHigh
            self.time += self.time_step
        else:
            self._viewCount1 += 1

    def viewMode4(self, qp):
            # self.qp.eraseRect(self._top, self._left, self._width, self._height)
        qp.setFont(QFont('Arial', 10))
        qp.setPen(QColor('white'))
        #self._text1 = '        Спортивный забег "Пять Вершин"'
        self._text2 = 'Протокол финиша эстафета:'
        qp.drawText(QRect(0, 0, self._width, 18),Qt.AlignCenter, self._text1)
        #qp.drawText(QRect(0, 18, self._width, 18), Qt.AlignCenter, self._text2)
        _text_indent = 29
        _nr_indent = 20
        _name_indent = 41
        _name_size = 15
        _result_indent = 149
        _text_hight = 14
        _count_highlight = False
        _temp_highlight = 0
        qp.setFont(QFont('Arial', 10))
        for i in range (0, self._viewCount1):
            if (self._viewCount2+i) == (len(self._viewText)):
                break
            # lfr_grp[i].pop(1)
            M = self._viewCount2+i+1
            M = str(M)
            txt = ''.join([str(element) for element in M])
            M = int(txt)
            if M < 100:
               txt = " " + txt 
            if M < 10:
               txt = " " + txt  
               
            qp.setPen(QColor('yellow'))
            qp.drawText(0, (i*_text_hight)+_text_indent,txt)
            
            M = int((self._viewText[self._viewCount2+i][0]))
            
            if self._viewCount2+i+1 == 1:
                _temp_highlight = M%100
            
            if M%100 != _temp_highlight:
                _temp_highlight = M%100
                _count_highlight = not _count_highlight
            
            if  _count_highlight == False:  
        
                qp.setPen(QColor('orange'))
                   
            else:
                
                qp.setPen(QColor('green'))

            #qp.setPen(QColor('green'))
            qp.drawText(_nr_indent, (i*_text_hight)+_text_indent,
                        self._viewText[self._viewCount2+i][0])
            #txt = self._viewText[i][1]
            txt = [self._viewText[self._viewCount2+i][1][k]
                   for k in range(_name_size) if len(self._viewText[self._viewCount2+i][1]) > k]
            txt = ''.join([str(element) for element in txt])
            #qp.setPen(QColor('white'))
            qp.drawText(_name_indent, (i*_text_hight)+_text_indent, txt)
            #txt = [self._viewText[self._viewCount2+i][2][k]
            #       for k in range(8) if len(self._viewText[self._viewCount2+i][2]) > k]
            #txt = ''.join([str(element) for element in txt])
            #qp.drawText(193, (i*_text_hight)+_text_indent, txt)
            qp.setPen(QColor('red'))
            qp.drawText(_result_indent, (i*_text_hight)+_text_indent,
                        self._viewText[self._viewCount2+i][3])
            
        if (self._viewCount2 + self._viewWindowHigh) > (len(self._viewText)):

            self._viewCount3 = (
                (len(self._viewText)) - self._viewCount2)

        if (self._viewCount2+self._viewCount1) == (len(self._viewText)):
            self._viewCount1 = 1
            self._viewCount2 = 0
            self._viewCount3 = self._viewWindowHigh
            self.time += self.time_step

        elif self._viewCount1 == self._viewCount3:
            self._viewCount1 = 1
            self._viewCount2 += self._viewWindowHigh
            self._viewCount3 = self._viewWindowHigh
            self.time += self.time_step
        else:
            self._viewCount1 += 1

    def viewMode5(self, qp):
        qp.setPen(QColor('white'))
        qp.setFont(QFont('Arial', 10))
        #self._text1 = '        Спортивный забег "Пять Вершин"'
        self._text2 = 'Текущие командные результаты:'
        _text_indent = 29
        _nr_indent = 0
        _name_indent = 25
        _name_size = 35
        _comand_indent = 111
        _comand_size = 8
        _result_indent = 130
        _text_hight = 14
        qp.drawText(QRect(0, 0, self._width, 18),Qt.AlignCenter, self._text1)
        #qp.drawText(QRect(0, 18, self._width, 18), Qt.AlignCenter, self._text2)
                
        for i in range (0, self._viewCount1):
            if (self._viewCount2+i) == (len(self._viewText)):
                break
            M = self._viewCount2+i+1
            M = str(M)
            txt = ''.join([str(element) for element in M])
            M = int(txt)
            if M < 100:
                txt = " " + txt 
            if M < 10:
                txt = " " + txt  
               
            qp.setPen(QColor('yellow'))
            qp.drawText(0, (i*_text_hight)+_text_indent,txt)
                                        
            qp.setPen(QColor('green'))                 
            txt = [self._viewText[self._viewCount2+i][0][k]
                for k in range(_name_size) if len(self._viewText[self._viewCount2+i][0]) > k]
            txt = ''.join([str(element) for element in txt])
            qp.drawText(_name_indent, (i*_text_hight)+_text_indent, txt)
                    
            qp.setPen(QColor('red'))
            qp.drawText(_result_indent, (i*_text_hight)+_text_indent, self._viewText[self._viewCount2+i][1])  
        
        
        if (self._viewCount2 + self._viewWindowHigh) > (len(self._viewText)):

            self._viewCount3 = (
                (len(self._viewText)) - self._viewCount2)

        if (self._viewCount2+self._viewCount1) == (len(self._viewText)):
            self._viewCount1 = 1
            self._viewCount2 = 0
            self._viewCount3 = self._viewWindowHigh
            self.time += self.time_step

        elif self._viewCount1 == self._viewCount3:
            self._viewCount1 = 1
            self._viewCount2 += self._viewWindowHigh
            self._viewCount3 = self._viewWindowHigh
            self.time += self.time_step
        else:
            self._viewCount1 += 1            


class PT():

    def __init__(self, t, _hFunction):
        self.t = t
        self.hFunction = _hFunction
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
        super(MainWindow, self).__init__()
        #self.lfr = list()
        self.cwd = "" # Папка с программой
        self.cwd1 = "" # Папка по умолчанию, после первого открытия файла
        self.sorted_rule = 1    # Сортируем списки. 9 - по цеху, 4 - по имени, 8 - по результату, 5 - по цеху эстафета, 7 - по группе. По умолчанию 1 - по стартовому номеру
        self.view_rule = 0 # 1 - все подряд, 0 - с номерами, 2 - все подряд дополнительное правило
        self.group_rule = 0 # Сортировка по номеру группы. 0 - все.
        self.append_rule = 0 # Триггер для объединения результатов. 1 - эстафета
        self.autoreload = 0 # Триггер автообновления.
        self.autosave = 0 # Триггер автоматического сохранения.
        self.doublesave = 0 # Триггер сохранения двойного результата в один протокол.
        self.fullmsec = 0 # Триггер для отображения времени в абсолюте, в мсек.
        self.viewMode = 2 # Режим вывода. 0 - стартовый протокол. 2 - результаты
        self.viewSecond = 0
        self.reload_timer = 10
        self.all_tabs = []

        self.w2_top = 0
        self.w2_left = 0
        self.w2_width = 320
        self.w2_height = 240

        self.grp1 = []

        self.pro1 = []

        self.grp_zag = []
        self.increment_grp1 = 0

        self.increment_pro = 0
        self.increment_pro1 = 0


        self.local_filename_choose1 = ''

        
        self.mainWin1 ()
        self.w2 = SecondWindow()
        #self.w2.mapToGlobal( QPoint(self.w2_top, self.w2_left))
        #self.w2.show()

    def mainWin1 (self):
        
        self.setWindowIcon(QtGui.QIcon('src/Ski.ico'))
        self.setWindowTitle("Вывод результатов Марафон-Электро на дисплей.")
        self.cwd = os.getcwd() # Получить текущее местоположение файла программы
        #self.resize(1500, 1300)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
  
  
        self.list_widget = QListWidget()

        self.list_widget.setStyleSheet("QListWidget"
                                  "{"
                                  "border : 1px solid black;"
                                  "font: 12pt Arial;"
                                  "}"
                                  )
                               
        self.statusBar()
        
        
        self.btn_choose4 = QPushButton(self)  
        self.btn_choose4.setObjectName("Пустые")
        self.btn_choose4.setText("Показывать пустые")        
        self.btn_choose4.setCheckable(True)
        self.btn_choose4.setEnabled(False)
                
        #self.btn_choose5 = QPushButton(self)
        #self.btn_choose5.setObjectName("Вывод")
        #self.btn_choose5.setText("Вывести")
        #self.btn_choose5.setCheckable(True)
        #self.btn_choose5.setEnabled(False)
        
        self.btn_chooseFile1 = QPushButton(self)  
        self.btn_chooseFile1.setObjectName("Выбрать")
        self.btn_chooseFile1.setText("Открыть протокол")
        
        #self.btn_chooseFile2 = QPushButton(self)  
        #self.btn_chooseFile2.setObjectName("Выбрать")
        #self.btn_chooseFile2.setText("Открыть протокол 2")
        #self.btn_chooseFile2.setEnabled(False)
        
        #self.btn_chooseFile3 = QPushButton(self)  
        #self.btn_chooseFile3.setObjectName("Выбрать")
        #self.btn_chooseFile3.setText("Открыть протокол 3")
        #self.btn_chooseFile3.setEnabled(False)        

        #self.btn_chooseFile4 = QPushButton(self)  
        #self.btn_chooseFile4.setObjectName("Выбрать")
        #self.btn_chooseFile4.setText("Сохранить итоговый протокол")
        #self.btn_chooseFile4.setEnabled(False)

        self.text1 = QtWidgets.QLabel("  №                            Участник                                            Цех                                    г.р.                             Группа                            Итоговый")
        self.text2 = QtWidgets.QLabel("Сортировка",
                                    alignment=QtCore.Qt.AlignCenter)
        self.text3 = QtWidgets.QLabel("Группы",
                                    alignment=QtCore.Qt.AlignCenter)
        self.text4 = QtWidgets.QLabel("Координаты",
                                    alignment=QtCore.Qt.AlignCenter)
        self.text5 = QtWidgets.QLabel("Вывод",
                                    alignment=QtCore.Qt.AlignCenter)
        self.checkbox1 = QCheckBox('Обновлять автоматически', self)
        #self.checkbox2 = QCheckBox('Сохранять автоматически', self)
        #self.checkbox2.setEnabled(False)
        
        #self.checkbox3 = QCheckBox('Складывать оба результата', self)
        #self.checkbox3.setEnabled(False)
        #self.checkbox1.toggle()

        self.checkbox4 = QCheckBox("Стартовый номер", self)  
        self.checkbox4.setText("Стартовый номер")
        self.checkbox4.setChecked(True)
        self.checkbox4.setEnabled(False)
        
        self.checkbox5 = QCheckBox("Фамилия", self)  
        self.checkbox5.setText("Фамилия")
        self.checkbox5.setEnabled(False)

        self.checkbox6 = QCheckBox("Результат", self) 
        self.checkbox6.setText("Результат")        
        self.checkbox6.setEnabled(False)
        
        self.checkbox7 = QCheckBox("Цех", self)
        self.checkbox7.setText("Цех")
        self.checkbox7.setEnabled(False)
        
        self.checkbox8 = QCheckBox("Эстафета цикл", self)
        self.checkbox8.setText("Эстафета цикл")
        self.checkbox8.setEnabled(False)
        
        self.checkbox9 = QCheckBox("Вывести", self)
        self.checkbox9.setText("Вывести")
        #self.checkbox9.setCheckable(True)
        self.checkbox9.setEnabled(False)
        
        self.checkbox10 = QCheckBox("Командный результат", self)
        self.checkbox10.setText("Командный результат")
        #self.checkbox10.setCheckable(True)
        self.checkbox10.setEnabled(False)

        #self.checkbox7 = QCheckBox('Время абсолютное в мсек', self)
        #self.checkbox7.setEnabled(False)

        self.spinbox1 = QSpinBox(self)
        self.spinbox1.setRange(1, 60)
        self.spinbox1.setValue(5)
        self.spinbox1.setSuffix(' сек.')
        self.spinbox1.setFixedWidth(65)
        
        self.spinbox2 = QSpinBox(self)
        self.spinbox2.setRange(-65535, 65535)
        self.spinbox2.setValue(self.w2_top)
        self.spinbox2.setSuffix('px')
        self.spinbox2.setFixedWidth(65)
        
        self.spinbox3 = QSpinBox(self)
        self.spinbox3.setRange(-65535, 65535)
        self.spinbox3.setValue(self.w2_left)
        self.spinbox3.setSuffix('px')
        self.spinbox3.setFixedWidth(65)

        self.combobox1 = QComboBox(self)
        self.combobox1.setFixedWidth(165)
        self.combobox1.hidePopup()
         
        self.right_layout = QVBoxLayout()
      
        #self.setLayout(self.right_layout)
        
        self.left_layout = QVBoxLayout()
   
        #self.setLayout(self.left_layout)
        
        
        self.btn_choose4.pressed.connect(self.slot_btn_choose4)
        #self.btn_choose5.pressed.connect(self.slot_btn_choose5)
        self.btn_chooseFile1.clicked.connect(self.slot_btn_chooseFile1)
        #self.btn_chooseFile2.clicked.connect(self.slot_btn_chooseFile2)
        #self.btn_chooseFile3.clicked.connect(self.slot_btn_chooseFile3) 
        #self.btn_chooseFile4.clicked.connect(self.slot_btn_chooseFile4)              
        self.list_widget.itemClicked.connect(self.clicked)
        self.combobox1.activated[int].connect(self.onCombo1Selected)
        self.checkbox1.stateChanged.connect(self.checkBox_1)
        #self.checkbox2.stateChanged.connect(self.checkbox_2)
        #self.checkbox3.stateChanged.connect(self.checkbox_3)
        self.checkbox4.clicked.connect(self.checkbox_4) 
        self.checkbox5.clicked.connect(self.checkbox_5) 
        self.checkbox6.clicked.connect(self.checkbox_6)
        self.checkbox7.clicked.connect(self.checkbox_7)
        self.checkbox8.stateChanged.connect(self.checkbox_8)
        self.checkbox9.stateChanged.connect(self.checkbox_9)
        self.checkbox10.stateChanged.connect(self.checkbox_10)
        self.spinbox1.valueChanged.connect(self.spinBox_1)
        self.spinbox2.valueChanged.connect(self.spinBox_2)
        self.spinbox3.valueChanged.connect(self.spinBox_3)
       
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
        self.left_layout.addWidget(self.checkbox4) 
        self.left_layout.addWidget(self.checkbox5) 
        self.left_layout.addWidget(self.checkbox7)        
        self.left_layout.addWidget(self.checkbox6)
        self.left_layout.addWidget(self.text5)
        self.left_layout.addWidget(self.checkbox8)
        self.left_layout.addWidget(self.checkbox10)
        self.left_layout.addWidget(self.btn_choose4)
        #self.left_layout.addWidget(self.btn_choose5)
        self.left_layout.addWidget(self.checkbox9)
        
        self.left_layout.addWidget(self.text4)
        self.left_layout.addWidget(self.spinbox2)
        self.left_layout.addWidget(self.spinbox3)
        #self.left_layout.addWidget(self.checkbox7)   
        
        self.left_layout.addWidget(self.btn_chooseFile1) #,alignment=QtCore.Qt.AlignTop
        #self.left_layout.addWidget(self.btn_chooseFile2) 
        #self.left_layout.addWidget(self.btn_chooseFile3)
        
        self.left_layout.addWidget(self.checkbox1)
        self.left_layout.addWidget(self.spinbox1)
        
        #self.left_layout.addWidget(self.btn_chooseFile4)
        #self.left_layout.addWidget(self.checkbox2)
        #self.left_layout.addWidget(self.checkbox3)
        #self.left_layout.insertSpacing(10, 20)
        self.left_layout.addWidget(self.text3)
        self.left_layout.addWidget(self.combobox1)

        self.left_layout.insertSpacing(0, 20)
        self.left_layout.insertSpacing(10, 10)
        self.left_layout.insertSpacing(14, 10)
        self.left_layout.insertSpacing(17, 10)
        
        self.left_layout.addStretch()

        grid.addLayout(self.left_layout, 0, 0 , 
                       alignment=QtCore.Qt.AlignLeft) 
        
        grid.addLayout(self.right_layout, 0, 1, 0, 1, 
                       alignment=QtCore.Qt.AlignRight) 

        #grid.addWidget(self.list_widget, 0, 1, 20, 20)      
        
        #tempFrame.addWidget(grid)
        #centralWidget.addWidget(tempFrame)
        
        centralWidget.setLayout(grid)
        self.setGeometry(500, 300, 1000, 500)
        #self.oldPos = self.pos()
        
        #self.show()
 
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
            dPars, self.lfr_grp1, self.pro1, self.group_rule, self.view_rule, self.fullmsec)
        
        # Сортируем списки по нулевому полю
        lfr_pro1 = sorted(self.lfr_pro1)
       
        lfr_pro = [e.copy() for e in lfr_pro1]

        lfr_pro_t = self.pro_grp_sort(lfr_pro, self.lfr_grp1)

        QListWidget.clear(self.list_widget)

        
        lfr_pro_t = self.pro_preapare(lfr_pro_t)
        
        len_lfr = len(lfr_pro_t) 
        
        # Вывод на второе окно
        if self.viewSecond == 1:
            self.updateSecond(len_lfr, lfr_pro_t)
        
        # Преобразуем списки участников в чистый текст.
        lfr_pro_t = ['\t'.join(lfr_pro_t[i])
                         for i in range(len(lfr_pro_t))]

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
        #self.statusBar().setFixedSize(1000, 60)
        self.statusBar().showMessage(str("Число участников - ") +
                                     str(len_lfr) +  #self.increment_pro1 len_lfr
                                     str(" Записей в протоколе - ") +
                                     str(self.increment_pro)+
                                     str("  ")+
                                     str(self.local_filename_choose1)+
                                     str("  ") +
                                     str(self.local_filename_choose2)+
                                     str("  ") +
                                     str(self.local_filename_choose4))
        
    def updateSecond (self, len, lfr_pro_t):
        # ['6  ', 'Карпачева Оксана', 'НТМК', '1975', 'Ж2 НТМК         ', '00:00:32,18']
        # Пока выводим стартовый список. Потом будем выводить не стартовый.
        # Сортируем списки. 9 - по цеху, 4 - по имени, 8 - по результату, 5 - по цеху, 7 - по группе. По умолчанию 1 - по стартовому номеру
        text_v = []
        
        inc = 0
        for i in range(len):  # self.increment_pro
            if inc >= len:
                break
            text_temp = []
            inc += 1
            if self.append_rule != 2:
                text_temp.append(lfr_pro_t[i][0])
                text_temp.append(lfr_pro_t[i][1])
                text_temp.append(lfr_pro_t[i][2])
                text_temp.append(lfr_pro_t[i][5])
            else:
                text_temp.append(lfr_pro_t[i][0])
                text_temp.append(lfr_pro_t[i][1])
            #text_temp = ' '.join(text_temp)
            text_v.append(text_temp)

        text_v.insert(0,self.w2_top)
        text_v.insert(0,self.w2_left)
        if self.sorted_rule == 8:       
            if self.append_rule == 1:  # Триггер для объединения результатов. 1 - эстафета
                if self.autoreload == 1: # autoreload только обновляет выводимый текст, не сбрасывая экран
                    text_v.insert(0, 14)
                else:
                    text_v.insert(0, 4)
            elif self.append_rule == 2:  #текущие командные результаты
                if self.autoreload == 1:
                    text_v.insert(0, 15)
                else:
                    text_v.insert(0, 5)    
            else:
                if self.autoreload == 1:
                    text_v.insert(0, 13)
                else:
                    text_v.insert(0, 3)
        else:
            if self.autoreload == 1:
                text_v.insert(0, 11)
            else:
                text_v.insert(0, 1)
        # Обновляем содержимое второго окна
        self.w2.updateSecondWin = text_v
          
    
    def saveprot(self, prot):
        if self.local_filename_choose4 != "" and len(prot)>0:
            dPars.save_pro(self.local_filename_choose4, prot)
    
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
       
        # Удаляем лишние поля, при условии, что список не пустой.
        if len(lfr_pro_t) > 0 and self.append_rule != 2:
            [(lfr_pro_t[i].pop(0)) for i in range(len(lfr_pro_t))]
            [(lfr_pro_t[i].pop(0)) for i in range(len(lfr_pro_t))]
            [(lfr_pro_t[i].pop(1)) for i in range(len(lfr_pro_t))]
            [(lfr_pro_t[i].pop(5)) for i in range(len(lfr_pro_t))]
            if len(lfr_pro_t[0]) > 6 and self.group_rule != 1:
                [(lfr_pro_t[i].pop(6)) for i in range(len(lfr_pro_t))]
                if len(lfr_pro_t[0]) > 7 and self.group_rule != 1:
                    [(lfr_pro_t[i].pop(7)) for i in range(len(lfr_pro_t))]
        elif len(lfr_pro_t) > 0:
            [(lfr_pro_t[i].pop(1)) for i in range(len(lfr_pro_t))]
            [(lfr_pro_t[i].pop(1)) for i in range(len(lfr_pro_t))]
             
        # ['101', 'Яскунов Егор', 'ЦРМО-31м', '1900', '1группа М       ', '24:07,90']
        return lfr_pro_t

    def funcSort(x):
        return x%100   

    def relay_sort(self, lfr_pro):
    
        lfr_pro_t = []
        
        rez = [0, 0, 0, 0]
        msecf = 0
        msec = 0
        s = ''
        lfr_pro_t.append(lfr_pro[0])
        if len(lfr_pro) < 6:
            return     
        #_count = lfr_pro_s[i].count('4294967295')
        for k in lfr_pro:
            if isinstance(k, str):
                pass
            elif k != 4294967295:
                msec += k
                msecf += k
            else:
                msecf += k
            
        lfr_pro_t.append(msecf)
        lfr_pro_t.append(msec)
                #else:
                #    msec = lfr_pro_s[i][1]+lfr_pro_s[i][3]+lfr_pro_s[i][5]+lfr_pro_s[i][7]
                
        if msec!=4294967295:
                
            if self.fullmsec !=1:
                
                rez[0] = msec // 360000
                msec = msec % 360000
                rez[1] = msec // 6000
                msec = msec % 6000
                rez[2] = msec // 100
                msec = msec % 100
                rez[3] = msec
            else:
                rez[0] = 0
                rez[1] = 0
                rez[2] = msec // 100
                msec = msec % 100
                rez[3] = msec
                #rez[2] = rez[2]-msec
                    
                #msec = rez[0]*3600
                #msec += rez[1]*60
                #msec += rez
        else:
                rez[0] = 0
                rez[1] = 0
                rez[2] = 0
                rez[3] = 0
                #if time_rule !=1:
                #if rez[0] > 9:
                #    s =  str(rez[0]) + ':'
                #else:
                #    s = '0' + str(rez[0]) + ':'
        if rez[0] > 9:
            s = s + str(rez[0]) + ':'  
        else:
            s = s +'0' + str(rez[0]) + ':'
        
        if rez[1] > 9:
            s = s + str(rez[1]) + ':'  
        else:
            s = s +'0' + str(rez[1]) + ':'

        if rez[2] > 9:
            s = s  + str(rez[2])
        else:
            s = s + '0' + str(rez[2])

        if rez[3] > 9:
            s = s + ',' + str(rez[3])
        else:
            s = s + ',0' + str(rez[3])
                
        lfr_pro_t.append(s)   
                
                   
        
        return lfr_pro_t 
        

    def pro_grp_sort(self, lfr_pro, lfr_grp):
        # [0, 171, '171', 9, 'Мельник Елена', 'ОТиПБ1', '1988', '3группа Ж       ', 88875, '00:14:48,75']
        lfr_pro_t = ()
        # Выборка участников по группам
        if self.group_rule>1:
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

            lfr_pro = [e.copy() for e in lfr_pro_t]
                        
        if len(lfr_pro) == 0:
            return lfr_pro_t 
        # Сортируем списки. 9 - по цеху, 4 - по имени, 8 - по результату, 5 - по цеху, 7 - по группе. По умолчанию 1 - по стартовому номеру
        if self.sorted_rule == 8 and len(lfr_pro[0])>10:
                lfr_pro_t = sorted(
                    lfr_pro, key=lambda x: x[12])
                
        elif self.sorted_rule == 8 and self.append_rule == 1:
                lfr_pro = sorted(
                    lfr_pro, key=itemgetter(5, 1))
                lfr_pro_t = sorted(
                    lfr_pro, key=lambda x: (x[1] % 100))
                if self.view_rule == 0:
                    *lfr_pro_t, = filter(lambda x: x[8] != 4294967295, lfr_pro_t)
                    *lfr_pro_t, = filter(lambda x: x[8] != 0, lfr_pro_t)#(x[8] % 10)
        
        elif self.sorted_rule == 8 and self.append_rule == 2:
            lfr_pro = sorted(
                lfr_pro, key=itemgetter(5, 1))
            # lfr_pro_t = sorted(
            #    lfr_pro, key=lambda x: (x[1] % 100))

            # [0, 171, '171', 9, 'Мельник Елена', 'ОТиПБ1', '1988', '3группа Ж       ', 88875, '00:14:48,75']
            # ['101', 'Яскунов Егор', 'ЦРМО-31м', '1900', '1группа М       ', '24:07,90']
            # ['АТЦм', 146425, 'АТЦм', 269508, 'АТЦм', 238904, 'АТЦм', 232263]
            lfr_pro_s = []
            lfr_pro_t = []
            temp_group = lfr_pro[0][5]
            temp_null_count = 0
            for i in range(len(lfr_pro)):
                if temp_group == lfr_pro[i][5] and i != len(lfr_pro):
                    lfr_pro_s.append(lfr_pro[i][5])
                    lfr_pro_s.append(lfr_pro[i][8])    
                else:
                    lfr_pro_t.append(self.relay_sort(lfr_pro_s))
                    lfr_pro_s = []
                    lfr_pro_s.append(lfr_pro[i][5])
                    lfr_pro_s.append(lfr_pro[i][8])
                if lfr_pro[i][8] == 4294967295:
                    temp_null_count += 1
                temp_group = lfr_pro[i][5]
            
            if  len(lfr_pro) == temp_null_count:
                #lfr_pro_t = []
                return lfr_pro_t
                
            lfr_pro_t.append(self.relay_sort(lfr_pro_s))
            lfr_pro = [x for x in lfr_pro_t if x is not None]
            
            lfr_pro_t = sorted(
                    lfr_pro, key=lambda x: x[1])
            
               
        elif self.sorted_rule == 8:
                lfr_pro_t = sorted(
                    lfr_pro, key=lambda x: x[8])
                if self.view_rule == 0: # 0 с стартовым и результатом
                    *lfr_pro_t, = filter(lambda x: x[8] != 4294967295, lfr_pro_t)
                    *lfr_pro_t, = filter(lambda x: x[8] != 0, lfr_pro_t)#(x[8] % 10)
                
        elif self.sorted_rule == 5 and self.append_rule == 1:
                lfr_pro = sorted(
                    lfr_pro, key=itemgetter(5, 1) )
                lfr_pro_t = sorted(
                    lfr_pro, key=lambda x: (x[1] % 100) )
         
        elif self.sorted_rule == 5:
                #lfr_pro_t = sorted(
                #    lfr_pro, key=lambda x: x[5]) 
                lfr_pro_t = sorted(
                    lfr_pro, key=itemgetter(5, 1) )      
        else:    
                lfr_pro_t = sorted(
                    lfr_pro, key=lambda x: x[self.sorted_rule])
        
        return lfr_pro_t
    
        #*res, = filter(lambda x: x[1] == 31, spisok)

        #*res, = filter(lambda x: x[0][-1] != 'ь', spisok)


    #@pyqtSlot()
    def clicked(self, item):
        QMessageBox.information(
            self, "Подробнее", "Участник номер: " + item.text(), QMessageBox.Ok)

    def checkBox_1(self, state): # Автоматическое обновление протокола. Имеет баг при выводе.
       if state == Qt.Checked:
            self.autoreload = 1            
            self.t.start()
       else:
            self.autoreload = 0
            self.t.stop()

    def checkbox_2(self, state):
        if state == Qt.Checked:
            self.autosave = 1
        else:
            self.autosave = 0
        self.reload()

    def checkbox_3(self, state):
        if state == Qt.Checked:
            self.doublesave = 1
        else:
            self.doublesave = 0
        self.reload()

    # 4 - по имени, 8 - по результату, 3 - по группе. По умолчанию 1 - по стартовому номеру
    def checkbox_4(self):
        # self.btn_choose1.setChecked(True)
        self.checkbox4.setChecked(True)
        self.checkbox5.setChecked(False)
        self.checkbox6.setChecked(False)
        self.checkbox7.setChecked(False)
        self.checkbox8.setChecked(False)
        self.checkbox10.setChecked(False)
        self.checkbox8.setEnabled(False)
        self.checkbox10.setEnabled(False)
        self.sorted_rule = 1
        self.append_rule = 0
        self.reload()

    # 4 - по имени, 8 - по результату, 3 - по группе. По умолчанию 1 - по стартовому номеру
    def checkbox_5(self):
        self.checkbox4.setChecked(False)
        self.checkbox5.setChecked(True)
        self.checkbox6.setChecked(False)
        self.checkbox7.setChecked(False)
        self.checkbox8.setChecked(False)
        self.checkbox10.setChecked(False)
        self.checkbox8.setEnabled(False)
        self.checkbox10.setEnabled(False)
        
        self.sorted_rule = 4
        self.append_rule = 0
        self.reload()

    # 4 - по имени, 8 - по результату, 3 - по группе. По умолчанию 1 - по стартовому номеру
    def checkbox_6(self):
        self.checkbox4.setChecked(False)
        self.checkbox5.setChecked(False)
        self.checkbox7.setChecked(False)
        self.checkbox6.setChecked(True)
        self.checkbox8.setChecked(False)
        self.checkbox10.setChecked(False)
        self.checkbox8.setEnabled(True)
        self.checkbox10.setEnabled(True)
        
        # self.btn_choose3.setChecked(True)
        self.sorted_rule = 8
        self.reload()

    def checkbox_7(self):
        self.checkbox4.setChecked(False)
        self.checkbox5.setChecked(False)
        self.checkbox6.setChecked(False)
        self.checkbox7.setChecked(True)
        self.checkbox10.setChecked(False)
        self.checkbox8.setEnabled(True)
        self.checkbox10.setEnabled(False)
       
        # self.btn_choose3.setChecked(True)
        self.sorted_rule = 5
        self.reload()
 
    def checkbox_8(self, state):  # "Эстафета"
        if state == Qt.Checked:
            self.append_rule = 1
            self.checkbox10.setChecked(False)
            self.reload()
        elif self.append_rule == 2:
            return
        else:
            self.append_rule = 0
            self.reload()

    def checkbox_9(self, state): # Вывод второго окна
            # self.btn_choose1.setChecked(False)
            # self.btn_choose2.setChecked(False)
            # self.btn_choose3.setChecked(True)
        if state == Qt.Checked:
            self.viewSecond = 1
            self.w2 = SecondWindow()
            self.reload()
            # self.btn_choose5.setChecked(True)
        else:
            self.viewSecond = 0
            self.w2.close()
            # self.btn_choose5.setChecked(False)
            # self.reload()

    def checkbox_10(self, state):  # Командный
        if state == Qt.Checked:
            self.append_rule = 2
            self.checkbox8.setChecked(False)
            self.reload()
        elif self.append_rule == 1:
            return
        else:
            self.append_rule = 0
            self.reload()
            #    self.reload()


    def spinBox_1(self):
        if self.autoreload == 1:
            self.t.stop()
            self.reload_timer = self.spinbox1.value()
            self.t.start()
        else:
            self.reload_timer = self.spinbox1.value()
    def spinBox_2(self):
        self.w2_top = self.spinbox2.value()
        self.w2.move(self.w2_top, self.w2_left)
        
    def spinBox_3(self):
        self.w2_left = self.spinbox3.value()
        self.w2.move(self.w2_top, self.w2_left)

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
    

    def slot_btn_chooseFile1(self):

        old_file = self.local_filename_choose1

        if self.local_filename_choose1 != "":
            old_file = self.local_filename_choose1
        
        if self.cwd1 == "":
            self.cwd1 = self.cwd
        
        self.local_filename_choose1, _ = QFileDialog.getOpenFileName(self,
                                                                            "Выбрать протокол 1",
                                                                            self.cwd1,  # Начальный путь
                                                                            "Pro Files (*.pro)")   # Установить фильтрацию расширений файлов, через двойную точку с запятой

        if self.local_filename_choose1 == "":
            QMessageBox.warning(
                self, "Ошибка", "Не выбран протокол!", QMessageBox.Ok)
            if old_file != "":
               self.local_filename_choose1 = old_file
            return

        _, _, increment_grp1 = Parser.read_grp(
            dPars, self.local_filename_choose1)
        
        if increment_grp1 == 0:
            QMessageBox.warning(
                self, "Ошибка", "Данный протокол не имеет файла групп!", QMessageBox.Ok)
            self.local_filename_choose1 = ""
            return
        
        _, increment_pro1 = Parser.read_pro(
            dPars, self.local_filename_choose1)
        if increment_pro1 == 0:
            QMessageBox.warning(
                self, "Ошибка", "Это пустой протокол!", QMessageBox.Ok)
            self.local_filename_choose1 = ""
            return
        
        self.cwd1 =  self.local_filename_choose1.rsplit('.', 1)[0] 
        self.cwd = self.cwd1
        self.local_filename_choose2 = ""
        self.local_filename_choose4 = ""
        self.append_rule = 0
        
        self.checkbox4.setEnabled(True)
        self.checkbox5.setEnabled(True)
        self.checkbox6.setEnabled(True)
        self.checkbox7.setEnabled(True)
        self.checkbox9.setEnabled(True)
        self.btn_choose4.setEnabled(True)
        #self.btn_choose5.setEnabled(True)
        #self.checkbox2.setEnabled(False)
        #self.checkbox3.setCheckState(False)
        #self.checkbox3.setEnabled(False)
        #self.checkbox7.setEnabled(True)
        #self.btn_chooseFile2.setEnabled(True)
        #self.btn_chooseFile4.setEnabled(False)

        self.reload()

    def slot_btn_chooseFile2(self):

        old_file = self.local_filename_choose2

        if self.local_filename_choose2 != "":
            old_file = self.local_filename_choose2
            
        if self.cwd2 == "":
            self.cwd2 = self.cwd
        
        self.local_filename_choose2, _ = QFileDialog.getOpenFileName(self,
                                                                            "Выбрать протокол 2",
                                                                            self.cwd2,  # Начальный путь
                                                                            "Pro Files (*.pro)")   # Установить фильтрацию расширений файлов, через двойную точку с запятой

        if self.local_filename_choose2 == "" or self.local_filename_choose2 == self.local_filename_choose1:
            QMessageBox.warning(
                self, "Ошибка", "Выберете другой протокол!", QMessageBox.Ok)
            if old_file != "":
               self.local_filename_choose2 = old_file
            return
        
        self.cwd2 = self.local_filename_choose2.rsplit('.', 1)[0]
        
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
        _, increment_pro2 = Parser.repack_pro(
            dPars, grp2, pro2, self.group_rule, 0, self.fullmsec)

        # Проверим число участников. Протоколы не будут обратываться при не совпадении числа участников.
        if self.increment_pro1 != increment_pro2:  # or self.increment_pro != increment_pro_all2
            QMessageBox.warning(
                self, "Ошибка", "Не совпадает число участников в протоколе!", QMessageBox.Ok)
            self.local_filename_choose2 = ""
            self.pro2 = []
            self.lfr_pro2 = []
            return

        #self.btn_chooseFile3.setEnabled(False)
        #self.btn_chooseFile4.setEnabled(True)
        self.checkbox4.setChecked(True)
        self.checkbox5.setChecked(False)
        self.checkbox6.setChecked(False)
        self.checkbox7.setChecked(False)
        self.checkbox8.setChecked(False)
        #self.btn_choose5.setEnabled(True)
        #self.checkbox3.setEnabled(True)
        # Теперь подготовим протоколы к сравнению и объединению результатов. Обновим виджеты в окне.
        self.reload()
        

    def closeEvent(self, event):              # +++
        self.w2.close()

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':

    dPars = Parser()

    app = QApplication(sys.argv)

    w = MainWindow() 
    
    w.show()   

    w.t = PT(w.reload_timer, w.reload)

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
