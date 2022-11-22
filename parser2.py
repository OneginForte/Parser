import codecs
import struct
import string
import operator

import sys
import os

from time import strftime, gmtime
import threading

from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication, QDesktopWidget,
                             QDialog, QTextEdit, QGridLayout, QPushButton, QWidget,
                             QSizePolicy, QListWidget,QScrollBar,QListWidgetItem, QVBoxLayout, QFileDialog, QMessageBox)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.lf=''
        self.setWindowTitle("Parser")
        self.cwd = os.getcwd() # Получить текущее местоположение файла программы
        self.resize(1000, 1000)
        self.all_tabs = []
        
        tempWidget=QWidget()
        self.setCentralWidget(tempWidget)
        tempFrame=QtWidgets.QFrame()
        self.palette=tempFrame.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255,255,255))
        tempFrame.setPalette(self.palette)
        tempFrame.setAutoFillBackground(True)
        #tempFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
  
  
  
        self.widget = QListWidget()
        #self.setGeometry(0, 0, 400, 300)
        self.btn_chooseFile = QPushButton(self)  
        self.btn_chooseFile.setObjectName("btn_chooseFile")  
        self.btn_chooseFile.setText("Выбрать файл")
        
        
        #self.layout = QVBoxLayout()
        #self.layout.addWidget(self.btn_chooseFile)
        
        #self.setLayout(self.layout)
        self.btn_chooseFile.clicked.connect(self.slot_btn_chooseFile)       
        self.widget.itemClicked.connect(self.clicked)
        
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.widget, 1, 1)
        grid.addWidget(self.btn_chooseFile, 0, 1)
        
        
        grid.setRowStretch(1, 1)
        grid.setColumnStretch(1, 1)
        
        tempWidget.setLayout(grid)
        self.show()
 
        
        

    def clicked(self, item):
        QMessageBox.information(self, "Parser", "Участник: " + item.text(),QMessageBox.Ok)
        
    def slot_btn_chooseFile(self):
        
        Dpars = Parser()

        fileName_choose, filetype = QFileDialog.getOpenFileName(self,  
                                   "Выбрать файл",  
                                    self.cwd, # Начальный путь 
                                    "Pro Files (*.pro)")   # Установить фильтрацию расширений файлов, через двойную точку с запятой        
        
        if fileName_choose == "":
            
            return


        File=Parser.init(Dpars, fileName_choose)
        self.lf=Parser.run(Dpars, File)
        QListWidget.clear(self.widget) 
        self.widget.addItems(self.lf)
        #self.show()       
    

class Parser:
    
    def __init__(self):
        
        self.M = 0
        self.lf = []
        self.kf = ''
        self.rez = [0,0,0,0]
        self.increment = 0
    
    def init(self, txt):
        #Открыть бинарный протокол для чтения
        f_pro = open(txt, 'rb') #'Весенний кросс 3.pro', 'rb'

        # Получить 282 байт записи из бинарного файла
        #self.data_bytes = self.f_pro.read(282)
        
        return f_pro 

    def run(self, data_bytes):
        #data_byte=Pobj.data_byte
        data_byte = data_bytes.read(282)
        s = ''
        
        while data_byte:
            self.rez = [0,0,0,0]
            tf = []
            C=(-1,)
            L=b''
            S=b''
            #Не забудем проверить, запись это или нет    
            if data_byte[0]==0: 
            
                # Выделяем стартовый номер
                S = [data_byte[8+i] for i in range(2)]
                self.M=bytes(S)
                self.M=struct.unpack('<h', self.M)
                C=self.M
                s = ''.join([str(element) for element in self.M])
                tf.append(C) #tf = tf+s
                s=s+"\t"
                tf.append(s)

                # Выделяем 24 байт имени из записи
                L = [data_byte[11+i] for i in range(24)]
                # Преобразуем list через bytes и метод join в string
                self.M=[bytes([x]) for x in L if x>0]
                s=[x.decode('cp1251','replace') for x in self.M]
                s = ''.join([str(element) for element in s])
                s=s+"\t"
                tf.append(s) #tf =   tf+"  \t"+s  #

                # Выделяем 41 байт наименования команды из записи
                L = [data_byte[166+i] for i in range(41)]
                # Преобразуем list через bytes и метод join в string
                self.M=[bytes([x]) for x in L if x>0]
                s=[x.decode('cp1251','replace') for x in self.M]
                s = ''.join([str(element) for element in s])
                s=s+"\t"       
                tf.append(s) #tf =  tf+"\t"+'\t'+'\t'+s  #
                
                # Выделяем год рождения
                S = [data_byte[216+i] for i in range(2)]
                self.M = bytes(S)
                self.M = struct.unpack('<H', self.M)
                s = ''.join([str(element) for element in self.M])
                s=s+"\t"
                tf.append(s) #tf+"\t"+s  
                self.M=0

                # Выделяем результат
                S = [data_byte[232+i] for i in range(4)]
                self.M = bytes(S)
                self.M = struct.unpack('L', self.M)
                s = ''.join([str(element) for element in self.M])
                msec = int(s)
                self.rez[0] = msec // 360000
                msec = msec%360000
                self.rez[1] = msec // 6000
                msec =  msec%6000
                self.rez[2] = msec // 100
                msec = msec%100
                self.rez[3] = msec
        
                s=''

                if self.rez[0]> 9:  
                    s= s + str(self.rez[0])
                else:
                    s = s+ '0' + str(self.rez[0])

                if self.rez[1] > 9:
                    s = s+ ':'+ str(self.rez[1])
                else:
                    s = s+':0' + str(self.rez[1])

                if self.rez[2] > 9:
                    s = s+ ':' + str(self.rez[2])
                else:
                    s = s+':0' + str(self.rez[2])

                if self.rez[3] > 9:
                    s = s+',' + str(self.rez[3])
                else:
                    s = s+',0' + str(self.rez[3])
                s=s#+"\n"
                tf.append(s) #  # 
                s = ''
        

            data_byte = data_bytes.read(282)
            #Игнорируем удаленные и пустые записи
            if C == (-1,): 
                continue
            self.lf.append(tf)
            self.increment += 1
        
        #Закроем уже не нужный протокол
        data_bytes.close()

            
        #Сортируем списки по номеру участников листов и преобразуем все в чистый текст   
        self.lf = sorted(self.lf) 
        [(self.lf[i].pop(0)) for i in range(len(self.lf))]
        self.lf = [''.join(self.lf[i]) for i in range(len(self.lf))] #''.join(map(str, Pobj.lf[i]))
        #[Pobj.lf.append(Pobj.lf[i]) for i in range(len(Pobj.lf))]
        #Pobj.lf = ','.join(map(str, Pobj.lf))
        #lf=''.join([str(element) for element in lf])
        return self.lf
        
        kf = ''.join(map(str, lf))

        print(kf)    
        print("Total records = ", increment)

        #Сохраним получившийся список в текстовый файл
        f = open('test.txt', 'w')
        f.write(kf)
        f.close()



#Pobj = Parser()

app = QApplication(sys.argv)

w = MainWindow()
#w.show()

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
