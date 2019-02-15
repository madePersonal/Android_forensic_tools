import time
from pyand import ADB
from threading import *
from textwrap import wrap
import wx
import sys


HEX_RESULT_ID = wx.NewId()
ERROR_RESULT_ID = wx.NewId()

def HEX_RESULT(win, func):
    win.Connect(-1, -1, HEX_RESULT_ID, func)

def ERROR_RESULT(win, func):
    win.Connect(-1, -1, ERROR_RESULT_ID, func)

class ErrorEvent(wx.PyEvent):
    def __init__(self, error):
        wx.PyEvent.__init__(self)
        self.SetEventType(ERROR_RESULT_ID)
        self.error = error

class HexEvent(wx.PyEvent):
    def __init__(self, hex, binary):
        wx.PyEvent.__init__(self)
        self.SetEventType(HEX_RESULT_ID)
        self.hex = hex
        self.binary = binary

class Hex(Thread):

    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.adb = ADB()

    def start_thread(self, func, *args):
        thread = Thread(target=func, args=args)
        thread.setDaemon(True)
        thread.start()

    def hex_sum(self, file):
        cmd = "cat '%s'"%file
        cat = self.adb.shell_command(cmd)
        cat_split = wrap(cat, 16)
        result = []
        for k in cat_split:
            hex = k.encode("hex")
            split = wrap(hex, 2)
            result.append(split)
        n = 0
        for g in result:
            wx.PostEvent(self._notify_window, HexEvent(g, unicode(cat_split[n],'utf-8', errors='replace')))
            n = n+1
            time.sleep(0.00001)

    def run_hex(self, file):
        self.start_thread(self.hex_sum, file)

    def error_handler(self, error):
        wx.PostEvent(self._notify_window, ErrorEvent(error))

