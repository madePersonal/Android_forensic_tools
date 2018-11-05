from pyand import ADB, Fastboot
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

file=adb.shell_command('ls /acct/uid -l')

# line = file.split('\n')
# y = (str(line[3]).split(' '))
# # hasil =" ".join(line)
# y.remove('')
# print(y)

def read_line(string):
    n =0
    asu ={}
    line = string.split("\n")
    for l in line:
        asu[n] = line[n]
        re = arr.array(str(asu[n]).split(''))
        n = n + 1
    print(re[0])

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
    result =[]
    array=creat_array(file)
    a = len(array)
    if a > 1 :
        n = 0
        for l in array:
            permmisison = array[n][0]
            if "d" in permmisison:
                result.append(array[n][7])
            if n < (a-2) :
                n = n + 1
            else:
                break
    return result

print insertToDB()




