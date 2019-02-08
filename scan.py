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

    def start_thread(self, func, *args):
        thread = Thread(target=func, args=args)
        thread.setDaemon(True)
        thread.start()

    def run_scan(self, dir):
        self.start_thread(self.scan, dir)

    def scan(self, dir):
        try:
            ADB().get_devices()
            ADB().set_target_by_id(0)
        except Exception as e:
            self.errorHandler(e.args[0])

        cmd_result = ADB().shell_command("ls "+dir+" -lR")
        if "error: no devices/emulators found" in cmd_result:
            self.errorHandler("no devices/emulators found")
            sys.exit()
        if self._want_abort:
            sys.exit()
        array = self.create_array(cmd_result)
        if self._want_abort:
            sys.exit()
        arr = self.clean_array(array)
        if self._want_abort:
            sys.exit()
        range = self.count_file(arr)
        if self._want_abort:
            sys.exit()
        wx.PostEvent(self._notify_window, RangeEvent(range))
        self.insert_to_db(arr)

    def updateProgress(self):
        self.__progress_value=self.__progress_value+1
        wx.PostEvent(self._notify_window, ProgressEvent(self.__progress_value))

    def errorHandler(self, error):
        wx.PostEvent(self._notify_window, ErrorEvent(error))

    def count_file(self, array):
        try:
            result = []
            for arr in array:
                per = arr[0]
                if per[:1] == "-" or per[:1] == "d":
                    result.append(arr)
                if self._want_abort:
                    break
            return len(result)
        except Exception as e:
            self.errorHandler(e.args[0])

    def insert_to_db(self, array):
        try:
            for arr in array:
                name =[]
                per = arr[0]
                if per[:1]=="/":
                    id_dir = None
                    dir = " ".join(str(x) for x in arr) #mennghubungkan nama directory yang berisi spasi
                    data().insert_dir(dir)
                    id = data().select_id_dir_by_name(dir)
                    print("dir masuk")
                    self.updateProgress()
                elif per[:1] == "-":
                    id_dir = id[0][0]
                    if len(arr) > 8:  # jika nama file berisi spasi
                        j = 7
                        while j <= len(arr) - 1:
                            name.append(arr[j])
                            j = j + 1
                        na = name
                        u = " ".join(str(x) for x in na)
                        data().insert_file(id_dir, u, arr[0], arr[5], arr[4])
                        print("file masuk")
                        self.updateProgress()
                    else:
                        data().insert_file(id_dir, arr[-1], arr[0], arr[5], arr[4])
                        print("file masuk")
                        self.updateProgress()
                if self._want_abort:
                    break
        except Exception as e:
            self.errorHandler(e.args[0])

    def create_array(self, text):
        o = []
        try:
            line = text.split("\n")
            for l in line:
                y = (str(l).split(" "))
                h = filter(None, y)
                if '->' in h:
                    h.remove('->')
                o.append(h)
                if self._want_abort:
                    break
            return o
        except Exception as e:
            self.errorHandler(e.args[0])

    def clean_array(self, array):
        result = []
        try:
            for arr in array:
                lengt = len(arr)
                if lengt!=0:
                    per = arr[0]
                    if lengt >= 1 and per!="total" and per!="ls:":#menghilangkan array yang kosong dan kata "total"
                        result.append(arr)
                if self._want_abort:
                    break
            return result
        except Exception as e:
            self.errorHandler(e.args[0])

    def abort(self):
        self._want_abort = 1


