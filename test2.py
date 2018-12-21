from pyand import ADB, Fastboot
import sqlite3

adb = ADB()
dev = adb.get_devices()
adb.set_target_by_id(0)
adb.get_target_device()
serial= adb.get_serialno()
asu = {}
n = 0
j = 0

already_dir = []

# con = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='andr_forensic_tools')
# cur = con.cursor()
try:
    con = sqlite3.connect("andr_forensic_tools.db")
    cur = con.cursor()
except Exception as e:
    print(e.message)

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

def clean_db():
    try:
        cur.execute("DELETE FROM sub_directory;")
        con.commit()
        cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='sub_directory';")
        con.commit()

        cur.execute("DELETE FROM  file;")
        con.commit()
        cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='file';")
        con.commit()

        cur.execute("DELETE FROM  directory;")
        con.commit()
        cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='directory';")
        con.commit()
    except Exception as e:
        print("clean DB error :"+e.args[0])




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

def insertToDB(dir):
    id_dir=1

    cur.execute('INSERT INTO `directory` (`name`) VALUES ("%s")' % (dir))
    con.commit()

    # cur.execute('SELECT `id_directory` FROM directory WHERE name ="%s"'%(dir))
    # id= cur.fetchone()
    # for k in id :
    #     id_dir =k

    text = adb.shell_command('ls '+dir+' -l')
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
                cur.execute('INSERT INTO `file` (`id_directory`,`name`) VALUES (%s,"%s")' % (id_dir, array[n][7]))
                con.commit()
            if n < (a-2) :
                n = n + 1
            else:
                break
        cur.execute('SELECT `name` FROM sub_directory WHERE id_directory =%s' %(id_dir))
        dir_name = cur.fetchall()
        for u in dir_name:
            insertToDB2(dir+u[0])

        while True :
            id_dir = id_dir+1
            try :
                cur.execute('SELECT directory.`name`, sub_directory.name FROM sub_directory, `directory` WHERE sub_directory.id_directory and directory.id_directory=%s' %(id_dir))
                dir_name = cur.fetchall()
                for u in dir_name:
                    insertToDB2(u[0]+u[1])
            except Exception as e:
                print(e.args[0])
                break


def insertToDB2(dir):
    id_dir = ""
    cur.execute('INSERT INTO `directory` (`name`) VALUES ("%s")' % (dir))
    con.commit()

    cur.execute('SELECT `id_directory` FROM directory WHERE name ="%s"' % (dir))
    id = cur.fetchone()
    for k in id:
        id_dir = k

    text = adb.shell_command('ls ' +dir+ ' -l')
    array = creat_array(text)

    a = len(array)
    if a > 1:
        n = 0
        for l in array:
            permmisison = array[n][0]  # permisison berada pada indek ke 0
            if "d" == permmisison[:1]:  # mencocokan kode pada huruf awal permisison
                cur.execute('INSERT INTO `sub_directory` (`id_directory`,`name`) VALUES (%s,"%s")' % (id_dir, array[n][7] + "/"))
                con.commit()
            elif "-" == permmisison[:1]:
                cur.execute('INSERT INTO `file` (`id_directory`,`name`) VALUES (%s,"%s")' % (id_dir, array[n][7]))
                con.commit()
            if n < (a - 2):
                n = n + 1
            else:
                break


insertToDB("/")

#clean_db()

# cur.execute('SELECT directory.`name`, sub_directory.name FROM sub_directory, `directory` WHERE sub_directory.id_directory=directory.id_directory AND directory.name = "%s"'%(dir+u[0]))
        # new_dir_name = cur.fetchone()
        # new_dir.append(new_dir_name[0]+new_dir_name[1])
        #
        # for h in new_dir :
        #     insertToDB2(h[0])



