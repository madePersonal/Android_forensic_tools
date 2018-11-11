import pymysql

con = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='andr_forensic_tools')
cur = con.cursor()

cur.execute('SELECT `name` FROM `sub_directory` WHERE id_directory =1')
dir_name = cur.fetchall()
filter(None, dir_name)

print dir_name[0][0]

# dir = "/acct/"
#
# print('ls ' + dir +' -l')