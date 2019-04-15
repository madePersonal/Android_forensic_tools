from threading import *
import time
from datetime import datetime
from pyand import ADB
from Data import Data
import ActiveProject
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
        self.data = Data(ActiveProject.active_project())
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
            cmd =["pull", "%s"%file[0],"%s"%dir]
            cmd5 = "md5sum -b '%s'" % file[0]
            cmdsha1 = "sha1sum -b '%s'" % file[0]
            resultpull = self.adb.run_cmd(cmd)
            resultmd5 = self.adb.shell_command(cmd5)
            resultsha1 = self.adb.shell_command(cmdsha1)

            if "error" in resultpull and resultmd5 and resultsha1:
                self.errorHandler(resultpull)
                break
            else:
                wx.PostEvent(self._notify_window, ProgressEvent(prgs_value, "%s dari %s file"%(prgs_value, count)))
                self.data.insert_log_pull(file[1], file[2], dir, resultmd5, resultsha1, datetime.utcnow())
            prgs_value = prgs_value+1
            time.sleep(0.001)

    def runPullFile(self, file, dir):
        self.start_thread(self.pull_file, file, dir)

    def errorHandler(self, error):
        wx.PostEvent(self._notify_window, ErrorEvent(error))
