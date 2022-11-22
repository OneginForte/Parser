import codecs
import struct
import string
import operator

# Открыть бинарный протокол для чтения
f_pro = open('Весенний кросс 3.pro', 'rb')
s = ''
M = 0
lf = []
rez = [0,0,0,0]

# Получить 282 байт записи из бинарного файла
data_byte = f_pro.read(282)
increment = 0

while data_byte:
    tf = []
    C=(-1,)
    L=b''
    S=b''
    #Не забудем проверить, запись это или нет    
    if data_byte[0]==0: 
       
        # Выделяем стартовый номер
        S = [data_byte[8+i] for i in range(2)]
        M=bytes(S)
        M=struct.unpack('<h', M)
        C=M
        s = ''.join([str(element) for element in M])
        tf.append(C) #tf = tf+s
        s=s+"\t"
        tf.append(s)

        # Выделяем 24 байт имени из записи
        L = [data_byte[11+i] for i in range(24)]
        # Преобразуем list через bytes и метод join в string
        M=[bytes([x]) for x in L if x>0]
        s=[x.decode('cp1251','replace') for x in M]
        s = ''.join([str(element) for element in s])
        s=s+"\t"
        tf.append(s) #tf =   tf+"  \t"+s  #

        # Выделяем 41 байт наименования команды из записи
        L = [data_byte[166+i] for i in range(41)]
        # Преобразуем list через bytes и метод join в string
        M=[bytes([x]) for x in L if x>0]
        s=[x.decode('cp1251','replace') for x in M]
        s = ''.join([str(element) for element in s])
        s=s+"\t"       
        tf.append(s) #tf =  tf+"\t"+'\t'+'\t'+s  #
        
        # Выделяем год рождения
        S = [data_byte[216+i] for i in range(2)]
        M = bytes(S)
        M = struct.unpack('<H', M)
        s = ''.join([str(element) for element in M])
        s=s+"\t"
        tf.append(s) #tf+"\t"+s  
        M=0

        # Выделяем результат
        S = [data_byte[232+i] for i in range(4)]
        M = bytes(S)
        M = struct.unpack('L', M)
        s = ''.join([str(element) for element in M])
        msec = int(s)
        rez[0] = msec // 360000
        msec = msec%360000
        rez[1] = msec // 6000
        msec =  msec%6000
        rez[2] = msec // 100
        msec = msec%100
        rez[3] = msec
  
        s=''

        if rez[0]> 9:  
            s= s + str(rez[0])
        else:
            s = s+ '0' + str(rez[0])

        if rez[1] > 9:
            s = s+ ':'+ str(rez[1])
        else:
            s = s+':0' + str(rez[1])

        if rez[2] > 9:
            s = s+ ':' + str(rez[2])
        else:
            s = s+':0' + str(rez[2])

        if rez[3] > 9:
            s = s+',' + str(rez[3])
        else:
            s = s+',0' + str(rez[3])
        s=s+"\n"
        tf.append(s) #  # 
        s = ''
 

    data_byte = f_pro.read(282)
    #Игнорируем удаленные и пустые записи
    if C == (-1,): 
        continue
    lf.append(tf)
    increment += 1
 
#Закроем уже не нужный протокол
f_pro.close()

    
#Сортируем списки по номеру участников листов и преобразуем все в чистый текст   
lf = sorted(lf) 
[(lf[i].pop(0)) for i in range(len(lf))]
lf = [''.join(map(str, lf[i])) for i in range(len(lf))]
lf = ''.join(map(str, lf))


print(lf)    
print("Total records = ", increment)

#Сохраним получившийся список в текстовый файл
f = open('test.txt', 'w')
f.write(lf)
f.close()

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
