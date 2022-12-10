#import os
import struct
#import sys


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

        file_grp = file.rsplit('.', 1)[0] + '.grp'

        # Создадим файл групп
        file_open = open(file_grp, 'x+b')

        grp=grp_zag+grp

        file_open.writelines(grp)

        # Закроем уже не нужный файл
        file_open.close()

    def save_pro(self, file, pro):

        # Создадим файл протокола
        file_open = open(file, 'w+b')

        #pro = grp_zag+grp

        file_open.write(pro) # writelines

        # Закроем уже не нужный файл
        file_open.close()

    def read_grp(self, file):

        self.increment_grp = 0
        self.grp_zag = []
        self.grp = []
        
        file_open = file.rsplit('.', 1)[0] + '.grp'
        #Откроем файл групп
        file_open = open(file_open, 'rb')

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

        increment_pro = 0
        
        pro = []

        #Откроем файл протокола
        file_open = open(file, 'rb')

        data_bytes = []
        prol = []

        data_bytes = file_open.read(282)
        while data_bytes:
            #Не забудем проверить запись участника. 0 - участник, все остальное технические записи и удаленные.
            if data_bytes[0] == 0:
                prol.append(increment_pro)
                prol.append(data_bytes)
                pro.append(prol) 
                prol=[]
            increment_pro += 1   
            data_bytes = file_open.read(282)
            

        #Закроем уже не нужный файл
        file_open.close()

        return pro, increment_pro

    def parse_grp(self, data_byte):
        M = 0
        tf = []
        L = []
        s = []
        W = b''

        # data_byte[20] число участников в группе
        # data_byte[17] пол групп "м" или "ж", "ю" или "д"
        # data_byte[76] год рождения от DWORD
        # data_byte[78] год рождения до DWORD
        # data_byte[18] признак результрующей группы #01 #F1
        # data_byte[27] номер результирующей группы

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
        # 01 признак результирующей записи, как и data_byte[27] = 255
        W = data_byte[18] 
        tf.append(W)
        #W = data_byte[20] # Число участников в группе 2 байта
        
        S = [data_byte[20+i] for i in range(2)]
        W = bytes(S)
        W = struct.unpack('<H', W)
        s = ''.join([str(element) for element in W])
        tf.append(s)
        W = int(s)
        tf.append(W)

        W = data_byte[27] # Номер группы к оторой относится как результирующей
        tf.append(W)
        W = data_byte[17] # пол: м, ж, ю, д
        if W > 33:
            #L= str (W)
            #M = L.encode()
            #W = W.to_bytes(1)
            W = struct.pack('B', W)
            s = W.decode('cp1251', 'replace')
            #s = ''.join([str(element) for element in s])
        else:
            M = str (W)
            #M = struct.unpack('<h', M)
            s = ''.join([str(element) for element in M])
            
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

        # Разберем список участников из протокола. 
        # Не забудем еще раз проверить, запись участника это или нет
        if data_byte[0] == 0:

            # Выделяем стартовый номер
            S = [data_byte[8+i] for i in range(2)]
            M = bytes(S)
            M = struct.unpack('<h', M)
            s = ''.join([str(element) for element in M])
            M = int(s)
                        
            # Игнорируем участника без стартового номера, если нам они не нужны
            if M == -1:                
                if view_rule != 1:  
                    return 0
                s = "   "                   
            else:
                if M < 100:
                    s = s + " "
                if M < 10:
                    s = s + " "       
                    
            # В нулевой индекс закинем стартовый номер числом. По умолчанию сортировка по нему.                    
            tf.append(M)  # tf = tf+s
            s = s + " "
            tf.append(s)

            # Выделяем группу
            grpr = data_byte[62]

            # Игнорируем участника, если выборка не по всем и это запись из группы "ошибки"
            if (group_rule != 1) and (grpr == 1):
                return 0
            if (group_rule == 1) and (grpr != 1):
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
            s = grp_d[grpr][0]
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
        tf = []
        tf.append('Все')
        tf.append(1)
        tf.append('0')
        tf.append(0)
        tf.append(255)
        tf.append('0')
        lf.append(tf)
        
        # Разберем список групп по названиям. Еще не разбирается в консолидирующих группах
        for i in range(len(grp_buffer)):
            tf = Parser.parse_grp(self, grp_buffer[i])
            if tf == 0:
                continue
            #tf = ''.join(map(str, tf))
            lf.append(tf)
        

        return lf

    def repack_pro(self, grp, pro_buffer, group_rule, view_rule):
        
        lf = []
        tf = []
        
        increment = 0

        # Разберем список участников. В начало всегда складывается байт индекса записи, берется из бинарной записи.
        for i in range (len(pro_buffer)): #x[0] for x in my_tuples
            tf = []
            buffer=pro_buffer[i][1]
            tf=Parser.parse_pro(self, grp, buffer, group_rule, view_rule)
            if tf == 0:
                continue
            increment += 1
            tf.insert(0,i)
            lf.append(tf)

        return lf, increment

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

