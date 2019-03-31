import sqlite3
from sqlite3 import Error

class Data():
    __error = None
    __result = None

    def __init__(self, db):
        try:
            self.con = sqlite3.connect(db, check_same_thread = False)
            self.cur = self.con.cursor()
        except Error as e:
            print(e)

    def clean_db(self):
        try:
            self.cur.execute("DELETE FROM  file;")
            self.con.commit()
            self.cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='file';")
            self.con.commit()

            self.cur.execute("DELETE FROM  directory;")
            self.con.commit()
            self.cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='directory';")
            self.con.commit()
        except Error as e:
            self.__error = e
            return self.__error

    def create_tables(self):
        tb_directory ='CREATE TABLE "directory" ("id_directory"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "name"	TEXT)'
        tb_evidence ='CREATE TABLE "evidence" ("case_number" INTEGER, "examiner_name" TEXT, "description" TEXT, "note" TEXT)'
        tb_pull_log ='CREATE TABLE "pull_log" ("id_log" INTEGER PRIMARY KEY AUTOINCREMENT, "file" TEXT, "from" TEXT, "to" TEXT, "md5_source" TEXT, "sha1_source" TEXT, "date" TEXT )'
        tb_file = 'CREATE TABLE "file" ("id_file" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "id_directory"	INTEGER NOT NULL, "name" TEXT, "permision" TEXT, "date" TEXT, "Size" REAL)'
        try:
            self.cur.execute(tb_directory)
            self.cur.execute(tb_file)
            self.cur.execute(tb_evidence)
            self.cur.execute(tb_pull_log)
        except Error as e:
            self.__error = e
            return self.__error

    def insert_log_pull(self, file, from_path, to_path, md5_source, sha1_source, date):
        try:
            query = "NSERT INTO  pull_log (`file`,`from`, `to`, md5_source, sha1_source,`date` )VALUES ('%s','%s','%s','%s','%s','%s')"%(file, from_path, to_path, md5_source, sha1_source, date)
            self.cur.execute(query)
            self.con.commit()
        except Error as e:
            self.__error = e
            return self.__error

    def insert_evidence(self, case_number, examiner_name, description, note):
        try:
            query = "INSERT INTO evidence (case_number, examiner_name, description, note) VALUES ('%s','%s','%s','%s')"%(case_number, examiner_name, description, note)
            self.cur.execute(query)
            self.con.commit()
        except Error as e:
            self.__error = e
            return self.__error

    def select_evidence(self):
        try:
            self.cur.execute("SELECT * from evidence")
            self.__result = self.cur.fetchone()
            return self.__result
        except Error as e:
            print(e)

    def select_all_data(self, order):
        try:
            select = "SELECT directory.name as loc, directory.id_directory, file.name as file, file.permision, file.Size, file.date"
            frm = " FROM directory, file"
            where = " WHERE directory.id_directory=file.id_directory ORDER BY "+order+" DESC"
            self.cur.execute(select+frm+where)
            self.__result = self.cur.fetchall()
            return self.__result
        except Exception as e:
            self.__error = e.args[0]
            return self.__error

    def select_by_extention(self, ext, order):
        try:
            select = "SELECT directory.name as loc, directory.id_directory, file.name as file, file.permision, file.Size, file.date"
            frm = " FROM directory, file"
            where = " WHERE directory.id_directory=file.id_directory and file.name like'%"+ext+"%' ORDER BY "+order+" DESC"
            self.cur.execute(select+frm+where)
            self.__result = self.cur.fetchall()
            return self.__result
        except Exception as e:
            self.__error = e.args[0]
            return self.__error

    def insert_dir(self, dir):
        try:
            self.cur.execute('INSERT INTO `directory` (`name`) VALUES ("%s")' % (dir))
            self.con.commit()
        except Exception as e :
            self.__error=e.args[0]
            return  self.__error

    def insert_sub_dir(self, id_dir, name):
        try:
            self.cur.execute('INSERT INTO `sub_directory` (`id_directory`,`name`) VALUES (%s,"%s")' % (id_dir, name))
            self.con.commit()
        except Exception as e :
            self.__error=e.args[0]
            return self.__error

    def insert_file(self, id_dir, name, permision, date, size):
        try:
            self.cur.execute('INSERT INTO `file` (`id_directory`,`name`, `permision`, `date`, `size`) VALUES (%s,"%s", "%s", "%s", "%s")' % (id_dir, name, permision, date, size))
            self.con.commit()
        except Exception as e :
            self.__error=e.args[0]
            return self.__error

    def select_name_by_id_dir(self, id_dir):
        try:
            query = 'SELECT `name` FROM sub_directory WHERE id_directory =%s'%(id_dir)
            self.cur.execute(query)
            self.__result = self.cur.fetchall()
            return self.__result
        except Exception as e:
            self.__error = e.args[0]
            return self.__error

    def select_name_dir_subDir(self, id_dir):
        try:
            query = 'SELECT directory.`name`, sub_directory.name FROM sub_directory, `directory` WHERE sub_directory.id_directory=directory.id_directory and directory.id_directory=%s' %(id_dir)
            self.cur.execute(query)
            self.__result = self.cur.fetchall()
            return self.__result
        except Exception as e:
            self.__error = e.args[0]
            return self.__error

    def select_id_dir_by_name(self, name):
        try:
            query = 'SELECT `id_directory` FROM directory WHERE name ="%s"'%(name)
            self.cur.execute(query)
            self.__result = self.cur.fetchall()
            return self.__result
        except Exception as e:
            self.__error = e.args[0]
            return self.__error

    def search(self, key, order):
        try:
            select = "SELECT directory.name as loc, directory.id_directory, file.name as file, file.permision, file.Size, file.date"
            frm = " FROM directory, file"
            where = " WHERE directory.id_directory=file.id_directory AND file.name like'%"+key+"%'"+" OR file.date like'%"+key+"%'"+" OR directory.name like'%"+key+"%' GROUP BY id_file"+" ORDER BY "+order+" DESC"
            self.cur.execute(select+frm+where)
            self.__result = self.cur.fetchall()
            return self.__result
        except Exception as e:
            self.__error = e.args[0]
            return self.__error
