import pymysql

con = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='andr_forensic_tools')
cur = con.cursor()

cur.execute('SELECT directory.name, sub_directory.name FROM `sub_directory`, directory WHERE sub_directory.id_directory=directory.id_directory AND directory.name = "/acct/"')

dir_name = cur.fetchall()

print dir_name[0][0]

# dir = "/acct/"
#
# print('ls ' + dir +' -l')