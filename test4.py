from pyand import ADB
from data import data

adb = ADB()
data =data()
try:
    adb.get_devices()
    adb.set_target_by_id(0)
except Exception as e:
    print(e.args[0])

text = adb.shell_command("ls /sdcard/ -laRt")

def create_array(text):
    n = 0
    o = []
    line = text.split("\n")
    for l in line:
        y = (str(line[n]).split(" "))
        h = filter(None, y)
        if '->' in h:
            h.remove('->')
        o.append(h)
        n = n + 1
    return o

def clean_array(array):
    n = 0
    result = []
    for i in array:
        lengt = len(array[n])
        if lengt!=0:
            per = array[n][0]
            if lengt >=1 and lengt!=2 and per!= "ls:":
                result.append(array[n])  # menghapus araay yang kosong
        n = n+1
    return result

# cmd_result = create_array(text)
# arr = clean_array(cmd_result)

def count_file(array):
    n = 0
    result = []
    for i in array:
        per = array[n][0]
        if per[:1] == "-" or per[:1] == "d":
            result.append(array[n])
        n = n + 1
    return len(result)

def insert_to_db(array):
    n = 0
    for i in array:
        name = []
        per = array[n][0]
        if per.endswith(":"):
            id_dir=None
            data.insert_dir(array[n][0])
            id=data.select_id_dir_by_name(array[n][-1])
        elif per[:1] == "-":
            id_dir = id[0][0]
            if len(array[n])>8: #jika nama file berisi spasi
                j = 7
                while j <= len(array[n])-1:
                    name.append(array[n][j])
                    j = j + 1
                na = name
                u = " ".join(str(x) for x in na)
                data.insert_file(id_dir, u, array[n][0], array[n][5], array[n][4])
            else:
                db = data.insert_file(id_dir, array[n][-1], array[n][0], array[n][5], array[n][4])
                print(db)
        n = n + 1

d = create_array(text)
r = clean_array(d)
insert_to_db(r)

# # # c = count_file(r)
# h =0
# name=[]
# for i in r :
#     name=[]
#     l = len(r[h])
#     if l > 8:
#         j = 7
#         while j <= l-1:
#             # sub=None
#             # sub = r[h][j]
#             # name = name+sub
#             name.append(r[h][j])
#             j = j + 1
#             # print(name)
#         n = name
#         u = " ".join(str(x) for x in n)
#         print(u)
#         # print(r[h][7]+" "+r[h][8])
#     h=h+1

# print(c)