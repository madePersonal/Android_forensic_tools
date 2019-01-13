# import pymysql
import subprocess
import sys
from pyand import ADB
from data import data
#
adb = ADB()
adb = ADB()
dev = adb.get_devices()
adb.set_target_by_id(0)
adb.get_target_device()
serial= adb.get_serialno()
#
# # con = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='andr_forensic_tools')
# # cur = con.cursor()
# #
# # cur.execute('SELECT directory.`name`, sub_directory.name FROM sub_directory, `directory` WHERE sub_directory.id_directory=directory.id_directory AND directory.name = "/cache/"')
# # new_dir_name = cur.fetchone()
# #
# # print(new_dir_name)
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
#
# text = adb.shell_command('ls / -l')
#
# print(creat_array(text))

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

#clean_db()

# cur.execute('SELECT directory.`name`, sub_directory.name FROM sub_directory, `directory` WHERE sub_directory.id_directory=directory.id_directory AND directory.name = "%s"'%(dir+u[0]))
        # new_dir_name = cur.fetchone()
        # new_dir.append(new_dir_name[0]+new_dir_name[1])
        #
        # for h in new_dir :
        #     insertToDB2(h[0])

# cur.execute('SELECT `id_directory` FROM directory WHERE name ="%s"'%(dir))
    # id= cur.fetchone()
    # for k in id :
    #     id_dir =k

import sqlite3
import hashlib
from data import data

try:
    con = sqlite3.connect("andr_forensic_tools.db")
    cur = con.cursor()
except Exception as e:
    print(e.message)



import time


def test():
    d = 1
    while True:
        d = d+1
        cur.execute('SELECT directory.`name`, sub_directory.name FROM sub_directory, `directory` WHERE sub_directory.id_directory and directory.id_directory=%s'%d)
        dir_name = cur.fetchall()
        for u in dir_name:
            print(u[0] + u[1])
        time.sleep(1)

def md5(file):
    hasher = hashlib.md5()
    with open(file, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()

def sha1(file):
    hasher = hashlib.sha1()
    with open(file, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()

data = data()
# ext =".usage"
# where = " WHERE directory.id_directory=file.id_directory AND file.name like'%"+ext+"%'"
# name = data.select_name_dir_subDir(3)
# for u in name:
#     print(u[0]+u[1])

#dir_name = data.select_name_dir_subDir(2)

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

def insertToDB2(dir):
    id_dir = ""
    data.insert_dir(dir)
    id=data.select_id_dir_by_name(dir)
    for k in id:
        id_dir = k[0]
        print(k)

    text = adb.shell_command('ls ' +dir+ ' -l')
    array = creat_array(text)
    print(array)

    a = len(array)
    if a > 1:
        n = 0
        for l in array:
            permmisison = array[n][0] #permisison berada pada indek ke 0
            if "d" == permmisison[:1]: #mencocokan kode pada huruf awal permisison (d berarti direktori)
                data.insert_sub_dir(id_dir,"/")
                print ("hai d")
            elif "-" == permmisison[:1]:#mencocokan kode pada huruf awal permisison (- berarti file)
                data.insert_file(id_dir, "/")
                print("hai -")
            if n < (a-2) :
                n = n + 1
            else:
                break
# print(data.select_all_data())
# insertToDB2("/acct/")
# text = adb.shell_command('ls ' +"/acct/"+ ' -l')
# array = creat_array(text)
# name = array[1][7]+"/"
# data.insert_sub_dir(2,name)
#data.insert_file(1, "haik")
data.clean_db()
# d=data.select_id_dir_by_name("/acct/")
# print(d)