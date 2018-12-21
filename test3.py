# import pymysql
# from pyand import ADB
#
# adb = ADB()
# adb = ADB()
# dev = adb.get_devices()
# adb.set_target_by_id(0)
# adb.get_target_device()
# serial= adb.get_serialno()
#
# # con = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='andr_forensic_tools')
# # cur = con.cursor()
# #
# # cur.execute('SELECT directory.`name`, sub_directory.name FROM sub_directory, `directory` WHERE sub_directory.id_directory=directory.id_directory AND directory.name = "/cache/"')
# # new_dir_name = cur.fetchone()
# #
# # print(new_dir_name)
# def creat_array(text):
#     n= 0
#     o = []
#     line = text.split("\n")
#     for l in line:
#         y = (str(line[n]).split(" "))
#         h = filter(None, y)
#         if '->' in h:
#             h.remove('->')
#         o.append(h)
#         n = n + 1
#     del o[0]
#     return o
#
# text = adb.shell_command('ls / -l')
#
# print(creat_array(text))
import sqlite3
import hashlib

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

print (md5("videoplayback.mp4"))
print (md5("file/videoplayback.mp4"))

print(sha1("566-1191-1-PB.pdf"))
print(sha1("file/566-1191-1-PB.pdf"))
