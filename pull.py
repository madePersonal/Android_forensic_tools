from threading import *
from pyand import ADB
import wx

RESULT_ID = wx.NewId()

def RESULT(win, func):
    win.Connect(-1, -1, RESULT_ID, func)

class pull(Thread):

    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0

    def start_thread(self, func, *args):
        thread = Thread(target=func, args=args)
        thread.setDaemon(True)
        thread.start()

    def pull_file(self, file, dir):
        cmd = "adb pull '%s' '%s' "%(file, dir)
        ADB().run_cmd(cmd)
