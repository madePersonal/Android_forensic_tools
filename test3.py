from pyand import ADB, Fastboot
import re
import json
import array as arr
import numpy


buah = "mangga jeruk nanas salak\n122 133 43 12"
bagi_buah = buah.split("\n")
test = ['drwxrwx---', '', '6', 'system', 'cache', '', '', '', '', '4096', '2018-05-06', '12:24', 'cache']
g = ['as', '', 'er']
# if '' in g:
#     test.remove('')
hasil = filter(None, g)
print(hasil)
# n = 0
# o = []
# # g = " ".join(y)
# for i in bagi_buah:
#     y = (str(bagi_buah[n]).split(" "))
#     o.append(y)
#     n = n + 1
#
# print(o)