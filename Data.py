import sqlite3

class Data():
    __error = None
    __result = None

    def __init__(self):
        try:
            self.con = sqlite3.connect("andr_forensic_tools.db", check_same_thread = False)
            self.cur = self.con.cursor()
        except Exception as e:
            print(e.args[0])

    def clean_db(self):
        try:
            self.cur.execute("DELETE FROM sub_directory;")
            self.con.commit()
            self.cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='sub_directory';")
            self.con.commit()

            self.cur.execute("DELETE FROM  file;")
            self.con.commit()
            self.cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='file';")
            self.con.commit()

            self.cur.execute("DELETE FROM  directory;")
            self.con.commit()
            self.cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='directory';")
            self.con.commit()
        except Exception as e:
            self.__error = e.args[0]
            return self.__error

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
