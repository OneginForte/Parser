import os
import struct
import sys

#from time import gmtime, strftime
#from tkinter import CENTER

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import ( QApplication, QComboBox, QFileDialog, QGridLayout, QListWidget,
                             QMessageBox,QPushButton, QVBoxLayout, QWidget)


class MainWindow(QtWidgets.QMainWindow):
    
    
    
    def __init__(self):
        self.lfr = ""
        self.sorted_rule = 0
        self.group_rule = 0
        self.all_tabs = []

        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon('Ski.ico'))
        self.setWindowTitle("Быстрый просмотрщик файлов протоколов для Марафон-Электро.")
        self.cwd = os.getcwd() # Получить текущее местоположение файла программы
        #self.resize(1500, 1300)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
  
  
        self.list_widget = QListWidget()
        
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
        self.btn_chooseFile.setText("Выбрать файл")

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
        self.setGeometry(500, 300, 800, 500)
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
                                   "Выбрать файл",  
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

        Parser.read(dPars, self.local_filename_choose)
        self.lfr1 = Parser.repack(dPars, dPars.grp, dPars.pro)
        QListWidget.clear(self.list_widget)
        self.list_widget.addItems(self.lfr1)
        self.combo.clear()
        self.combo.addItems(dPars.grp)
        self.statusBar().showMessage(str("Число участников - ") +
                                     str(dPars.increment) +
                                     str(" Записей в протоколе - ") +
                                     str(dPars.increment_pro))

class Parser:

    def __init__(self):

        self.lf = []
        self.kf = ''
        self.grp = []
        self.pro = []
        self.increment = 0
        self.increment_pro = 0
        self.grp_zag = []
        self.increment_grp = 0


    def read(self, file):

        self.increment_pro = 0
        self.increment_grp = 0
        self.increment = 0

        self.grp = []
        self.pro = []
        
        filename_grp_ext = file.rsplit('.', 1)[0] + '.grp'
        filename_pro_ext = file

        #Откроем файл групп
        file_open = open(filename_grp_ext, 'rb')

        self.grp_zag.append(file_open.read(1833))

        data_bytes = file_open.read(136)

        while data_bytes:
            #Не забудем проверить, запись это или нет
            self.grp.append(data_bytes)
            data_bytes = file_open.read(136)
            self.increment_grp += 1

        #Закроем уже не нужный файл
        file_open.close()

        #Откроем файл протокола
        file_open = open(filename_pro_ext, 'rb')
        
        
        data_bytes = []
        
        data_bytes = file_open.read(282)
        while data_bytes:
            #Не забудем проверить, запись это или нет
            if data_bytes[0] == 0:
                self.pro.append(data_bytes)
                self.increment_pro += 1
            data_bytes = file_open.read(282)


        #Закроем уже не нужный файл
        file_open.close()

    def parse_grp(self, data_byte): 
        M = 0
        tf = []
        L = []
        s = []   

        # data_byte[74] число участников в группе
        # data_byte[17] пол групп "м" или "ж", "ю" или "д"
        # data_byte[76] год рождения от
        # data_byte[78] год рождения до

        # Выделяем i байт имени группы из записи 15 байт
        L = [data_byte[1+i] for i in range(data_byte[0])]
        
        # Преобразуем list через bytes и метод join в string
        M = [bytes([x]) for x in L if x > 0]
        s = [x.decode('cp1251', 'replace') for x in M]
        s = ''.join([str(element) for element in s])
        if data_byte[0]<15:
            r=15-data_byte[0]
            for i in range(r):
                s=s+" " 
        #s = s+"\t"
        tf.append(s)
        return tf

    def parse_pro(self, data_byte):
        
        M = 0
        rez = [0, 0, 0, 0]
        tf = []
        C = (-1,)
        L = b''
        S = 0
        grp = 0
        s = ''
        

        # Разберем список участников из протокола. Не забудем проверить, запись это или нет
        if data_byte[0] == 0:

            # Выделяем стартовый номер
            S = [data_byte[8+i] for i in range(2)]
            M = bytes(S)
            M = struct.unpack('<h', M)
            C = M
            # В нулевой индекс закинем стартовый номер числом
            tf.append(C)  # tf = tf+s
            s = ''.join([str(element) for element in M])
            M = int(s)
            if M<100:
                s = s + " "
            if M<10:
                s = s + "  "
            s = s + "   "
            tf.append(s)

            # Выделяем группу
            S = data_byte[62]
            s = self.grp[S]
            grp = S
            s = ''.join(map(str, s))
            #s = str(S)
            s = s + "\t"
            tf.append(s)
            # Если сортировка по группе, то добавляем в нулевой индекс номер группы
            if w.sorted_rule==3:
                tf[0] = S

            # Выделяем i байт имени из записи 24 байт
            L = [data_byte[11+i] for i in range(data_byte[10])]
            # Преобразуем list через bytes и метод join в string
            M = [bytes([x]) for x in L if x > 0]
            s = [x.decode('cp1251', 'replace') for x in M]
            s = ''.join([str(element) for element in s])

            # Если сортировка по имени, то добавляем в нулевой индекс имя
            if w.sorted_rule==1:
                tf[0] = s

            s = s + "\t"
            tf.append(s)  # tf =   tf+"  \t"+s  #


            # Выделяем 41 байт наименования команды из записи
            L = [data_byte[166+i] for i in range(data_byte[165])]
            # Преобразуем list через bytes и метод join в string
            M = [bytes([x]) for x in L if x > 0]
            s = [x.decode('cp1251', 'replace') for x in M]
            s = ''.join([str(element) for element in s])
            s = s + "\t"
            tf.append(s)  # tf =  tf+"\t"+'\t'+'\t'+s  #

            # Выделяем год рождения
            S = [data_byte[216+i] for i in range(2)]
            M = bytes(S)
            M = struct.unpack('<H', M)
            s = ''.join([str(element) for element in M])
            s = s+"\t"
            tf.append(s)  # tf+"\t"+s
            M = 0

            # Выделяем результат
            S = [data_byte[232+i] for i in range(4)]
            M = bytes(S)
            M = struct.unpack('L', M)
            s = ''.join([str(element) for element in M])
            msec = int(s)

            # Если сортировка по результату, то добавляем в нулевой индекс абсолютный результат
            if w.sorted_rule==2:
                tf[0]=msec

            rez[0] = msec // 360000
            msec = msec % 360000
            rez[1] = msec // 6000
            msec = msec % 6000
            rez[2] = msec // 100
            msec = msec % 100
            rez[3] = msec

            s = ''

            if rez[0] > 9:
                s = s + str(rez[0])
            else:
                s = s + '0' + str(rez[0])

            if rez[1] > 9:
                s = s + ':' + str(rez[1])
            else:
                s = s+':0' + str(rez[1])

            if rez[2] > 9:
                s = s + ':' + str(rez[2])
            else:
                s = s+':0' + str(rez[2])

            if rez[3] > 9:
                s = s+',' + str(rez[3])
            else:
                s = s+',0' + str(rez[3])

            #s=s#+"\n"
            tf.append(s)

        else:  # Игнорируем удаленные и пустые записи
            return 0
        
        # Игнорируем группу, если выборка не по ней
        if ((w.group_rule != grp) and (w.group_rule!=0)):
            return 0

        if C == (-1,): 
            return 0
            
        return tf

    def repack(self, grp_buffer, pro_buffer):

        self.grp = []
        lf = []
        tf = 'Все'
        lf.append(tf)
        # Разберем список групп по названиям.
        for i in range(len(grp_buffer)):
            tf = Parser.parse_grp(self, grp_buffer[i])
            if tf == 0:
                continue
            tf = ''.join(map(str, tf))
            lf.append(tf)
        self.grp = lf

        lf = []

        # Разберем список участников.
        for i in range(len(pro_buffer)):
            tf = Parser.parse_pro(self, pro_buffer[i])
            if tf==0:
                continue
            self.increment += 1
            lf.append(tf) 
                      
        # Сортировка участников    
        lf = Parser.sort(self, lf)
    
        # Преобразуем списки участников в чистый текст.
        lf = [''.join(lf[i]) for i in range(len(lf))] 

        return lf
        
        #''.join(map(str, Pobj.lf[i]))
        #[Pobj.lf.append(Pobj.lf[i]) for i in range(len(Pobj.lf))]
        #Pobj.lf = ','.join(map(str, Pobj.lf))
        #lf=''.join([str(element) for element in lf])
        
        #kf = ''.join(map(str, lf))

        #print(kf)    
        #print("Total records = ", increment)

        #Сохраним получившийся список в текстовый файл
        #f = open('test.txt', 'w')
        #f.write(kf)
        #f.close()

    def sort(self, sorted_list):
        
        #Сортируем списки по нулевому полю, в зависимости от правила сортировки  
        lf = sorted(sorted_list)
        
        #Удаляем значения для сортировки 
        [(lf[i].pop(0)) for i in range(len(lf))]

        return lf

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
