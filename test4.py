from pyand import ADB
from data import data

adb = ADB()
dev = adb.get_devices()
adb.set_target_by_id(0)
data = data()

text = adb.shell_command("ls /vendor -R -l")

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
        if lengt >=1 and lengt!=2:
            result.append(array[n])  # menghapus araay yang kosong
        n = n+1
    return result

cmd_result = create_array(text)
arr = clean_array(cmd_result)

def count_file(array):
    n = 0
    result = []
    for i in array:
        per = array[n][0]
        if per[:1] == "-" or per[:1] == "d":
            result.append(array[n])
        n = n + 1
    return result

def insert_to_db(array):
    n = 0
    result = []
    for i in array:
        per = array[n][0]
        if per.endswith(":"):
            id_dir=None
            data.insert_dir(array[n][0])
            id=data.select_id_dir_by_name(array[n][0])
            id_dir=id[0][0]
        elif per[:1] == "-":
            data.insert_file(id_dir, array[n][7])
        n = n + 1

# # hasil = insert_to_db(arr)
# # hasil2 = count_file(arr)
clean = clean_array(arr)
b=0
for l in clean :
    print(clean[b])
    b=b+1
# insert_to_db(arr)
