import os
import struct
import sys


class Parser:

    def __init__(self):

        self.lf = []
        self.kf = ''
        self.grp_zag = []
        self.grp = []
        self.pro = []
        self.increment = 0
        self.increment_grp = 0
        self.increment_pro = 0

    def save_grp(self, file, grp_zag, grp):

        self.increment_grp = 0

        # Создадим файл групп
        file_open = open(file, 'x+b')

        grp=grp_zag+grp

        file_open.writelines(grp)

        # Закроем уже не нужный файл
        file_open.close()

    def read_grp(self, file):

        self.increment_grp = 0
        self.grp_zag = []
        self.grp = []

        #Откроем файл групп
        file_open = open(file, 'rb')

        self.grp_zag.append(file_open.read(1833))

        data_bytes = file_open.read(136)

        while data_bytes:
            #Не забудем проверить, запись это или нет
            self.grp.append(data_bytes)
            data_bytes = file_open.read(136)
            self.increment_grp += 1

        #Закроем уже не нужный файл
        file_open.close()

        return self.grp_zag, self.grp, self.increment_grp

    def read_pro(self, file):

        self.increment_pro = 0
        
        pro = []

        #Откроем файл протокола
        file_open = open(file, 'rb')

        data_bytes = []

        data_bytes = file_open.read(282)
        while data_bytes:
            #Не забудем проверить, запись это или нет
            if data_bytes[0] == 0:
                pro.append(data_bytes)
                self.increment_pro += 1
            data_bytes = file_open.read(282)

        #Закроем уже не нужный файл
        file_open.close()

        return pro, self.increment_pro

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
        if data_byte[0] < 15:
            r = 15-data_byte[0]
            for i in range(r):
                s = s+" "
        #s = s+"\t"
        tf.append(s)
        return tf

    def parse_pro(self, grp_d, data_byte, group_rule, view_rule):

        M = 0
        rez = [0, 0, 0, 0]
        tf = []
        C = (-1,)
        L = b''
        S = 0
        grpr = 0
        s = ''

        # Разберем список участников из протокола. Не забудем проверить, запись это или нет
        if data_byte[0] == 0:

            # Выделяем стартовый номер
            S = [data_byte[8+i] for i in range(2)]
            M = bytes(S)
            M = struct.unpack('<h', M)
            C = M
            s = ''.join([str(element) for element in M])
            M = int(s)
                        
            # Игнорируем участника без стартового номера, если нам они не нужны
            if C == (-1,):                
                if view_rule != 1:  
                    return 0
                s = "   "                   
            else:
                if M < 100:
                    s = s + " "
                if M < 10:
                    s = s + " "       
                    
            # В нулевой индекс закинем стартовый номер числом. По умолчанию сортировка по нему.                    
            tf.append(C)  # tf = tf+s
            s = s + " "
            tf.append(s)

            # Выделяем группу
            grpr = data_byte[62]

            # Игнорируем участника, если выборка не всем и это запись из группы "ошибки"
            if (group_rule == 0) and (grpr == 1):
                return 0

            # Добавляем номер группы, для последующей сортировки
            tf.append(grpr)

            # Выделяем data_byte[10] байт имени участника из записи 24 байт
            L = [data_byte[11+i] for i in range(data_byte[10])]
            # Преобразуем list через bytes и метод join в string
            M = [bytes([x]) for x in L if x > 0]
            s = [x.decode('cp1251', 'replace') for x in M]
            s = ''.join([str(element) for element in s])
            s = s + "\t"
            if data_byte[10]<16:
                s = s + "\t"  
            tf.append(s)  # tf =   tf+"  \t"+s  #

            # Выделяем data_byte[165] (до 41) байт наименования команды из записи
            L = [data_byte[166+i] for i in range(data_byte[165])]
            # Преобразуем list через bytes и метод join в string
            M = [bytes([x]) for x in L if x > 0]
            s = [x.decode('cp1251', 'replace') for x in M]
            s = ''.join([str(element) for element in s])
            if data_byte[165]<10:
                 s = s + "\t"  
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

            # Добавим группу после года рождения
            s = grp_d[grpr]
            s = ''.join(map(str, s))
            #s = str(S)
            s = s + " "
            tf.append(s)

            # Выделяем результат
            S = [data_byte[232+i] for i in range(4)]
            M = bytes(S)
            M = struct.unpack('L', M)
            s = ''.join([str(element) for element in M])
            msec = int(s)

                
            # Для сортировки по результату добавим результат в абсолютном значении
            tf.append(msec)  
                
            if msec!=4294967295:
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
                rez[2] = 0
                rez[3] = 0


            s = " "

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

        return tf

    def repack_grp(self, grp_buffer):

        lf = []
        # Нулевая группа все вместе.
        tf = 'Все'
        lf.append(tf)
        
        # Разберем список групп по названиям. Еще не разбирается в консолидирующих группах
        for i in range(len(grp_buffer)):
            tf = Parser.parse_grp(self, grp_buffer[i])
            if tf == 0:
                continue
            tf = ''.join(map(str, tf))
            lf.append(tf)

        return lf

    def repack_pro(self, grp, pro_buffer, group_rule, view_rule):
        
        lf = []
        self.increment = 0

        # Разберем список участников.
        for i in range(len(pro_buffer)):
            tf = Parser.parse_pro(self, grp, pro_buffer[i], group_rule, view_rule)
            if tf == 0:
                continue
            self.increment += 1
            lf.append(tf)

        return lf, self.increment

    def sort(self, sorted_list):

        #Сортируем списки по нулевому полю, в зависимости от правила сортировки
        lf = sorted(sorted_list)

        #Удаляем значения для сортировки
        [(lf[i].pop(0)) for i in range(len(lf))]

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

