import sys
import os
from PyQt5.QtWidgets import *

class MainForm(QWidget):
    def __init__(self, name = 'MainForm'):
        super(MainForm,self).__init__()
        self.setWindowTitle(name)
        self.cwd = os.getcwd() # Получить текущее местоположение файла программы
        self.resize(300,200)   # Установить размер окна
        # btn 1
        self.btn_chooseDir = QPushButton(self)  
        self.btn_chooseDir.setObjectName("btn_chooseDir")  
        self.btn_chooseDir.setText("Выберите папку")


        # btn 2
        self.btn_chooseFile = QPushButton(self)  
        self.btn_chooseFile.setObjectName("btn_chooseFile")  
        self.btn_chooseFile.setText("Выбрать файл")



        # btn 3
        self.btn_chooseMutiFile = QPushButton(self)  
        self.btn_chooseMutiFile.setObjectName("btn_chooseMutiFile")  
        self.btn_chooseMutiFile.setText("Выбор нескольких файлов")



        # btn 4
        self.btn_saveFile = QPushButton(self)  
        self.btn_saveFile.setObjectName("btn_saveFile")  
        self.btn_saveFile.setText("Сохранение файла")

        # Установить макет
        layout = QVBoxLayout()
        layout.addWidget(self.btn_chooseDir)
        layout.addWidget(self.btn_chooseFile)
        layout.addWidget(self.btn_chooseMutiFile)
        layout.addWidget(self.btn_saveFile)
        self.setLayout(layout)


        # Установить сигнал
        self.btn_chooseDir.clicked.connect(self.slot_btn_chooseDir)
        self.btn_chooseFile.clicked.connect(self.slot_btn_chooseFile)
        self.btn_chooseMutiFile.clicked.connect(self.slot_btn_chooseMutiFile)
        self.btn_saveFile.clicked.connect(self.slot_btn_saveFile)



    def slot_btn_chooseDir(self):
        dir_choose = QFileDialog.getExistingDirectory(self,  
                                    "Выберите папку",  
                                    self.cwd) # Начальный путь

        if dir_choose == "":
            print("\ nОтменить выбор")
            return

        print("\ nВы выбрали папку:")
        print(dir_choose)


    def slot_btn_chooseFile(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,  
                                    "Выбрать файл",  
                                    self.cwd, # Начальный путь 
                                    "All Files (*);;Text Files (*.txt)")   # Установить фильтрацию расширений файлов, через двойную точку с запятой

        if fileName_choose == "":
            print("\ nОтменить выбор")
            return

        print("\ nВы выбрали файл:")
        print(fileName_choose)
        print("Тип фильтра файлов:",filetype)


    def slot_btn_chooseMutiFile(self):
        files, filetype = QFileDialog.getOpenFileNames(self,  
                                    "Выбор нескольких файлов",  
                                    self.cwd, # Начальный путь 
                                    "All Files (*);;PDF Files (*.pdf);;Text Files (*.txt)")  

        if len(files) == 0:
            print("\ nОтменить выбор")
            return

        print("\ nВы выбрали файл:")
        for file in files:
            print(file)
        print("Тип фильтра файлов:",filetype)


    def slot_btn_saveFile(self):
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,  
                                    "Сохранение файла",  
                                    self.cwd, # Начальный путь 
                                    "All Files (*);;Text Files (*.txt)")  

        if fileName_choose == "":
            print("\ nОтменить выбор")
            return

        print("\ nФайл, который вы выбрали для сохранения:")
        print(fileName_choose)
        print("Тип фильтра файлов:",filetype)

if __name__=="__main__":
    app = QApplication(sys.argv)
    mainForm = MainForm('Проверить QFileDialog')
    mainForm.show()
    sys.exit(app.exec_())