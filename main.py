from data import data
import wx.lib.newevent
from threading import *
import time
import sys

DATA_RESULT_ID = wx.NewId()
RANGE_RESULT_ID = wx.NewId()
PROGRESS_RESULT_ID = wx.NewId()
ERROR_RESULT_ID = wx.NewId()

def PROGRESS_RESULT(win, func):
    win.Connect(-1, -1, PROGRESS_RESULT_ID, func)

def RANGE_RESULT(win, func):
    win.Connect(-1, -1, RANGE_RESULT_ID, func)

def ERROR_RESULT(win, func):
    win.Connect(-1, -1, ERROR_RESULT_ID, func)

def DATA_RESULT(win, func):
    win.Connect(-1, -1, DATA_RESULT_ID, func)


class ProgressEvent(wx.PyEvent):
    def __init__(self, val):
        wx.PyEvent.__init__(self)
        self.SetEventType(PROGRESS_RESULT_ID)
        self.val = val

class DataEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(DATA_RESULT_ID)
        self.data = data

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

class main(Thread):
    __progress_value = 1

    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0

    def update_progress(self):
        self.__progress_value=self.__progress_value+1
        wx.PostEvent(self._notify_window, ProgressEvent(self.__progress_value))

    def start_thread(self, func, *args):
        thread = Thread(target=func, args=args)
        thread.setDaemon(True)
        thread.start()

    def view_all_data(self):
        d = data().select_all_data()
        l = len(d)
        if l !=0:
            wx.PostEvent(self._notify_window, RangeEvent(l))
            h = 0
            for i in d:
                wx.PostEvent(self._notify_window, DataEvent(d[h]))
                h = h+1
                self.update_progress()
                time.sleep(0.0005)
        else:
            self.error_handler("data kosong")

    def view_data_by_ext(self, arg):
        d = data().select_by_extention(arg)
        l = len(d)
        if l!=0:
            wx.PostEvent(self._notify_window, RangeEvent(l))
            h=0
            for i in d:
                wx.PostEvent(self._notify_window, DataEvent(d[h]))
                h = h+1
                self.update_progress()
                time.sleep(0.0005)
        else:
            self.error_handler("data Kosong")

    def error_handler(self, error):
        wx.PostEvent(self._notify_window, ErrorEvent(error))

    def runSelectAll(self):
        self.start_thread(self.view_all_data)

    def runSelectByExt(self, ext):
        self.start_thread(self.view_data_by_ext, ext)