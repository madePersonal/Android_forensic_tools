import pymysql
from pyand import ADB

adb = ADB()
adb = ADB()
dev = adb.get_devices()
adb.set_target_by_id(0)
adb.get_target_device()
serial= adb.get_serialno()

# con = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='andr_forensic_tools')
# cur = con.cursor()
#
# cur.execute('SELECT directory.`name`, sub_directory.name FROM sub_directory, `directory` WHERE sub_directory.id_directory=directory.id_directory AND directory.name = "/cache/"')
# new_dir_name = cur.fetchone()
#
# print(new_dir_name)
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

text = adb.shell_command('ls / -l')

print(creat_array(text))