from threading import *

import time
from pyand import ADB
import wx

RESULT_ID = wx.NewId()
ERROR_ID = wx.NewId()
PROGRESS_ID = wx.NewId()

def RESULT(win, func):
    win.Connect(-1, -1, RESULT_ID, func)

def PROGRESS(win, func):
    win.Connect(-1, -1, PROGRESS_ID, func)

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

class ProgressEvent(wx.PyEvent):
    def __init__(self, progress, stat):
        wx.PyEvent.__init__(self)
        self.SetEventType(PROGRESS_ID)
        self.progress = progress
        self.stat = stat

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

    def pull_file(self, files, dir):
        count = len(files)
        wx.PostEvent(self._notify_window, ResultEvent(count))
        prgs_value = 1

        for file in files:
            cmd =["pull", "%s"%file,"%s"%dir]
            result = self.adb.run_cmd(cmd)
            if "error" in result:
                self.errorHandler(result)
                break
            else:
                wx.PostEvent(self._notify_window, ProgressEvent(prgs_value, "%s dari %s file"%(prgs_value, count)))
            prgs_value = prgs_value+1
            time.sleep(0.001)

    def runPullFile(self, file, dir):
        self.start_thread(self.pull_file, file, dir)

    def errorHandler(self, error):
        wx.PostEvent(self._notify_window, ErrorEvent(error))
