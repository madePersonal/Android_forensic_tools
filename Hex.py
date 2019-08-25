import time
from PyAndroid import ADB
from threading import *
import re
import wx
import sys


HEX_RESULT_ID = wx.NewId()
ERROR_RESULT_ID = wx.NewId()
RANGE_ID = wx.NewId()
PROGRESS_ID = wx.NewId()

def HEX_RESULT(win, func):
    win.Connect(-1, -1, HEX_RESULT_ID, func)

def RANGE_RESULT(win, func):
    win.Connect(-1, -1, RANGE_ID, func)

def ERROR_RESULT(win, func):
    win.Connect(-1, -1, ERROR_RESULT_ID, func)

def PROGRESS_RESULT(win, func):
    win.Connect(-1, -1, PROGRESS_ID, func)

class ErrorEvent(wx.PyEvent):
    def __init__(self, error):
        wx.PyEvent.__init__(self)
        self.SetEventType(ERROR_RESULT_ID)
        self.error = error

class ProgressEvent(wx.PyEvent):
    def __init__(self, progress):
        wx.PyEvent.__init__(self)
        self.SetEventType(PROGRESS_ID)
        self.progress = progress

class HexEvent(wx.PyEvent):
    def __init__(self, hex, binary):
        wx.PyEvent.__init__(self)
        self.SetEventType(HEX_RESULT_ID)
        self.hex = hex
        self.binary = binary

class RangeEvent(wx.PyEvent):
    def __init__(self, range):
        wx.PyEvent.__init__(self)
        self.SetEventType(RANGE_ID)
        self.range = range

class Hex(Thread):
    _progress_value = 0

    def __init__(self, notify_window, file):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.file = file
        self.adb = ADB()

    def start_thread(self, func):
        thread = Thread(target=func)
        thread.setDaemon(True)
        thread.start()

    def update_progress(self):
        self._progress_value = self._progress_value + 1
        wx.PostEvent(self._notify_window, ProgressEvent(self._progress_value))

    def run_hex(self):
        self._progress_value=0
        self.start_thread(self.hex)

    def hex(self):
        cmd = "cat '%s'"%self.file
        cat = self.adb.shell_command(cmd)
        if "error" in cat:
            self.error_handler(cat)
        else:
            cat_split = re.findall("................", cat)
            result = []
            for k in cat_split:
                hex = k.encode("hex")
                split = re.findall("..", hex)
                result.append(split)
            wx.PostEvent(self._notify_window, RangeEvent(len(result)))
            n = 0
            for g in result:
                wx.PostEvent(self._notify_window, HexEvent(g, unicode(cat_split[n],'utf-8', errors='replace')))
                self.update_progress()
                n = n + 1
                time.sleep(0.01)

    def error_handler(self, error):
        wx.PostEvent(self._notify_window, ErrorEvent(error))

    def abort(self):
        self._want_abort = 1

