from threading import *
from pyand import ADB
import wx

RESULT_ID = wx.NewId()
ERROR_ID = wx.NewId()

def RESULT(win, func):
    win.Connect(-1, -1, RESULT_ID, func)

def ERROR(win, func):
    win.Connect(-1, -1, ERROR_ID, func)

class ResultEvent(wx.PyEvent):
    def __init__(self, val):
        wx.PyEvent.__init__(self)
        self.SetEventType(RESULT_ID)
        self.val = val

class ErrorEvent(wx.PyEvent):
    def __init__(self, error):
        wx.PyEvent.__init__(self)
        self.SetEventType(ERROR_ID)
        self.error = error

class Pull(Thread):

    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.adb = ADB()


    def start_thread(self, func, *args):
        thread = Thread(target=func, args=args)
        thread.setDaemon(True)
        thread.start()

    def pull_file(self, file, dir):
        cmd =["pull", "%s"%file,"%s"%dir]
        result = self.adb.run_cmd(cmd)
        if "error" in result:
            self.errorHandler(result)
        else:
            wx.PostEvent(self._notify_window, ResultEvent("sucessfuly"))

    def runPullFile(self, file, dir):
        self.start_thread(self.pull_file, file, dir)

    def errorHandler(self, error):
        wx.PostEvent(self._notify_window, ErrorEvent(error))
