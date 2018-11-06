from pyand import ADB, Fastboot
import pymysql
import re
import json
import array as arr
import numpy
adb = ADB()
dev = adb.get_devices()
adb.set_target_by_id(0)
adb.get_target_device()
serial= adb.get_serialno()
asu = {}
n = 0
j = 0

con = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='andr_forensic_tools')
cur = con.cursor()

# line = file.split('\n')
# y = (str(line[3]).split(' '))
# # hasil =" ".join(line)
# y.remove('')
# print(y)

# def read_line(string):
#     n =0
#     asu ={}
#     line = string.split("\n")
#     for l in line:
#         asu[n] = line[n]
#         re = arr.array(str(asu[n]).split(''))
#         n = n + 1
#     print(re[0])

def creat_array(text):
    n= 0
    o = []
    line = text.split("\n")
    for l in line:
        y = (str(line[n]).split(" "))
        h = filter(None, y)
        if '->' in h:
            h.remove('->')
        o.append(h)

        n = n + 1
    del o[0]
    return o

def insertToDB():
    dir = " / "
    id_dir=""
    cur.execute('INSERT INTO `directory` (`name`) VALUES ("%s")' % (dir))
    con.commit()

    cur.execute('SELECT `id_directory` FROM directory WHERE name ="%s"'%(dir))
    id= cur.fetchone()
    for k in id :
        id_dir =k

    text = adb.shell_command('ls' +dir+ '-l')
    array=creat_array(text)

    a = len(array)
    if a > 1 :
        n = 0
        for l in array:
            permmisison = array[n][0] #permisison berada pada indek ke 0
            if "d" == permmisison[:1]: #mencocokan kode pada huruf awal permisison
                cur.execute('INSERT INTO `sub_directory` (`id_directory`,`name`) VALUES (%s,"%s")'%(id_dir,array[n][7]+"/"))
                con.commit()
            elif "-" == permmisison[:1]:
                cur.execute('INSERT INTO `file` (`id_sub_directory`,`nama`) VALUES (%s,"%s")' % (id_dir, array[n][7]))
                con.commit()
            if n < (a-2) :
                n = n + 1
            else:
                break
        cur.execute('SELECT `name` FROM `sub_directory` WHERE id_direcory =%s' %(id_dir))
        dir_name = cur.fetchall()
        for u in dir_name:
            insertToDB2(dir+u)

def insertToDB2(dir):
    sub_dir = ""
    id_dir = None
    cur.execute('INSERT INTO `directory` (`name`) VALUES ("%s")' % (dir))
    con.commit()

    text = adb.shell_command('ls' + dir + '-l')
    array = creat_array(text)

    a = len(array)
    if a > 1:
        n = 0
        for l in array:
            permmisison = array[n][0]  # permisison berada pada indek ke 0
            if "d" == permmisison[:1]:  # mencocokan kode pada huruf awal permisison
                cur.execute('INSERT INTO `sub_directory` (`id_directory`,`nama`) VALUES (%s,"%s")' % (
                id_dir, array[n][7] + "/"))
                con.commit()
            elif "-" == permmisison[:1]:
                cur.execute('INSERT INTO `file` (`id_directory`,`nama`) VALUES (%s,"%s")' % (id_dir, array[n][7]))
                con.commit()
            if n < (a - 2):
                n = n + 1
            else:
                break

insertToDB()










print insertToDB()




