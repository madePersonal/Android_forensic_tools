from data import data
import wx.lib.newevent
from pyand import ADB, Fastboot
from threading import *
import sys

PROGRESS_RESULT_ID = wx.NewId()
RANGE_RESULT_ID = wx.NewId()
ERROR_RESULT_ID = wx.NewId()

def PROGRESS_RESULT(win, func):
    win.Connect(-1, -1, PROGRESS_RESULT_ID, func)

def RANGE_RESULT(win, func):
    win.Connect(-1, -1, RANGE_RESULT_ID, func)

def ERROR_RESULT(win, func):
    win.Connect(-1, -1, ERROR_RESULT_ID, func)

class ProgressEvent(wx.PyEvent):
    def __init__(self, val):
        wx.PyEvent.__init__(self)
        self.SetEventType(PROGRESS_RESULT_ID)
        self.val = val

class RangeEvent(wx.PyEvent):
    def __init__(self, range):
        wx.PyEvent.__init__(self)
        self.SetEventType(RANGE_RESULT_ID)
        self.range = range

class ErrorEvent(wx.PyEvent):
    def __init__(self, error):
        wx.PyEvent.__init__(self)
        self.SetEventType(ERROR_RESULT_ID)
        self.error = error

class scanRecursive(Thread):
    __progress_value = -1

    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0

    def star_thread(self, func, *args):
        thread = Thread(target=func, args=args)
        thread.setDaemon(True)
        thread.start()

    def run_scan(self, dir):
        self.star_thread(self.scan, dir)

    def scan(self, dir):
        try:
            ADB().get_devices()
            ADB().set_target_by_id(0)
        except Exception as e:
            self.errorHandler(e.args[0])

        cmd_result = ADB().shell_command("ls "+dir+" -lR")
        if self._want_abort:
            sys.exit()
        array = self.create_array(cmd_result)
        if self._want_abort:
            sys.exit()
        arr = self.clean_array(array)
        if self._want_abort:
            sys.exit()
        range = self.count_file(arr)
        print(range)
        if self._want_abort:
            sys.exit()
        wx.PostEvent(self._notify_window, RangeEvent(range))
        self.insert_to_db(arr)

    def updateProgress(self):
        self.__progress_value=self.__progress_value+1
        print(self.__progress_value)
        wx.PostEvent(self._notify_window, ProgressEvent(self.__progress_value))

    def errorHandler(self, error):
        wx.PostEvent(self._notify_window, ErrorEvent(error))

    def count_file(self, array):
        try:
            n = 0
            result = []
            for i in array:
                per = array[n][0]
                if per[:1] == "-" or per[:1] == "d":
                    result.append(array[n])
                n = n + 1

                if self._want_abort:
                    break
            return len(result)
        except Exception as e:
            self.errorHandler(e.args[0])

    def insert_to_db(self, array):
        n = 0
        try:
            for i in array:
                name =[]
                per = array[n][0]
                if per[:1]=="/":
                    id_dir = None
                    dir = " ".join(str(x) for x in array[n]) #mennghubungkan nama directory yang berisi spasi
                    data().insert_dir(dir)
                    id = data().select_id_dir_by_name(dir)
                    self.updateProgress()
                elif per[:1] == "-":
                    id_dir = id[0][0]
                    if len(array[n]) > 8:  # jika nama file berisi spasi
                        j = 7
                        while j <= len(array[n]) - 1:
                            name.append(array[n][j])
                            j = j + 1
                        na = name
                        u = " ".join(str(x) for x in na)
                        data().insert_file(id_dir, u, array[n][0], array[n][5], array[n][4])
                        print("file masuk")
                        self.updateProgress()
                    else:
                        data().insert_file(id_dir, array[n][-1], array[n][0], array[n][5], array[n][4])
                        print("file masuk")
                        self.updateProgress()
                n = n + 1
                if self._want_abort:
                    break
        except Exception as e:
            self.errorHandler(e.args[0])

    def create_array(self, text):
        n = 0
        o = []
        try:
            line = text.split("\n")
            for l in line:
                y = (str(line[n]).split(" "))
                h = filter(None, y)
                if '->' in h:
                    h.remove('->')
                o.append(h)
                n = n + 1
                if self._want_abort:
                    break
            return o
        except Exception as e:
            self.errorHandler(e.args[0])

    def clean_array(self, array):
        n = 0
        result = []
        try:
            for i in array:
                lengt = len(array[n])
                if lengt!=0:
                    per = array[n][0]
                    if lengt >= 1 and per!="total" and per!="ls:":#menghilangkan array yang kosong dan kata "total"
                        result.append(array[n])
                n = n + 1
                if self._want_abort:
                    break
            return result
        except Exception as e:
            self.errorHandler(e.args[0])

    def abort(self):
        self._want_abort = 1


