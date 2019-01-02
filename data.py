import sqlite3

class data(object):
    __error = None
    __result = None
    try:
        con = sqlite3.connect("andr_forensic_tools.db")
        cur = con.cursor()
    except Exception as e:
        print(e.message)

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

    def select_all_data(self):
        try:
            query = "SELECT * FROM directory, file WHERE directory.id_directory=file.id_directory"
            self.cur.execute(query)
            self.__result = self.cur.fetchall()
            return self.__result
        except Exception as e:
            self.__error = e.args[0]
            return self.__error

