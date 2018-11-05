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

file=adb.run_cmd("shell ls sdcard/movies -l")

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

# print(creat_array(file))

print file


