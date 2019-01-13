from pyand import ADB, Fastboot
from data import data
data = data()
try:
    adb = ADB()
    dev = adb.get_devices()
    adb.set_target_by_id(0)
except Exception as e:
    print(e.args[0])

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

    data.insert_dir(dir)
    id_dir = 1
    text = adb.shell_command('ls '+dir+' -l')
    array=creat_array(text)

    a = len(array)
    if a > 1 :
        n = 0
        for l in array:
            permmisison = array[n][0] #permisison berada pada indek ke 0
            if "d" == permmisison[:1]: #mencocokan kode pada huruf awal permisison (d berarti direktori)
                data.insert_sub_dir(id_dir, array[n][7]+"/")
            elif "-" == permmisison[:1]:#mencocokan kode pada huruf awal permisison (- berarti file)
                data.insert_file(id_dir, array[n][7])
            if n < (a-2) :
                n = n + 1
            else:
                break

        dir_name = data.select_name_by_id_dir(id_dir)
        for u in dir_name:
            insertToDB2(dir+u[0])

        while True :
            id_dir = id_dir+1
            dir_name = data.select_name_dir_subDir(id_dir)
            try :
                for u in dir_name:
                    insertToDB2(u[0]+u[1])
                    print("pemanggilan proses 2")
            except Exception as e:
                print(e.args[0])
                break



def insertToDB2(dir):
    id_dir = ""
    data.insert_dir(dir)
    id=data.select_id_dir_by_name(dir)
    for k in id:
        id_dir = k[0]

    text = adb.shell_command('ls '+dir+' -l')
    array = creat_array(text)
    a = len(array)
    if a > 1:
        n = 0
        for l in array:
            permmisison = array[n][0] #permisison berada pada indek ke 0
            if "d" == permmisison[:1]: #mencocokan kode pada huruf awal permisison (d berarti direktori)
                data.insert_sub_dir(id_dir, array[n][7]+"/")
            elif "-" == permmisison[:1]:#mencocokan kode pada huruf awal permisison (- berarti file)
                data.insert_file(id_dir, array[n][7])
            if n < (a-2) :
                n = n + 1
            else:
                break

insertToDB("/")
#data.clean_db()







