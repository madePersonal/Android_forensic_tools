from Data import Data
import wx.lib.newevent
from threading import *
import time
from PyAndroid import ADB
import sys
import ActiveProject

DATA_RESULT_ID = wx.NewId()
RANGE_RESULT_ID = wx.NewId()
PROGRESS_RESULT_ID = wx.NewId()
ERROR_RESULT_ID = wx.NewId()
HASH_RESULT_ID = wx.NewId()
PROJECT_RESULT_ID = wx.NewId()

def PROGRESS_RESULT(win, func):
    win.Connect(-1, -1, PROGRESS_RESULT_ID, func)

def RANGE_RESULT(win, func):
    win.Connect(-1, -1, RANGE_RESULT_ID, func)

def ERROR_RESULT(win, func):
    win.Connect(-1, -1, ERROR_RESULT_ID, func)

def DATA_RESULT(win, func):
    win.Connect(-1, -1, DATA_RESULT_ID, func)

def HASH_RESULT(win, func):
    win.Connect(-1, -1, HASH_RESULT_ID, func)

def PROJECT_RESULT(win, func):
    win.Connect(-1, -1, PROJECT_RESULT_ID, func)


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

class HashEvent(wx.PyEvent):
    def __init__(self, hash):
        wx.PyEvent.__init__(self)
        self.SetEventType(HASH_RESULT_ID)
        self.hash = hash

class ProjectEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(PROJECT_RESULT_ID)
        self.data = data

class Main(Thread):
    __progress_value = 0

    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.adb=ADB()
        try:
            self.data=Data(ActiveProject.active_project())
        except Exception as e:
            self.error_handler("no project opened")

    def update_progress(self):
        self.__progress_value=self.__progress_value+1
        wx.PostEvent(self._notify_window, ProgressEvent(self.__progress_value))

    def start_thread(self, func, *args):
        thread = Thread(target=func, args=args)
        thread.setDaemon(True)
        thread.start()

    def view_all_data(self, args):
        d = self.data.select_all_data(args)
        l = len(d)
        print(l)
        if l !=0:
            wx.PostEvent(self._notify_window, RangeEvent(l))
            for i in d:
                wx.PostEvent(self._notify_window, DataEvent(i))
                self.update_progress()
                time.sleep(0.0005)
        else:
            self.error_handler("data kosong")

    def view_data_by_ext(self, ext, order):
        d = self.data.select_by_extention(ext, order)
        l = len(d)
        if l!=0:
            wx.PostEvent(self._notify_window, RangeEvent(l))
            for i in d:
                wx.PostEvent(self._notify_window, DataEvent(i))
                self.update_progress()
                time.sleep(0.0005)
        else:
            self.error_handler("data Kosong")

    def view_log_pull(self):
        d = self.data.select_pull_log()
        l = len(d)
        if l != 0:
            for i in d:
                wx.PostEvent(self._notify_window, DataEvent(i))
                time.sleep(0.0005)
        else:
            self.error_handler("data Kosong")

    def search_data(self, key, order):
        d = self.data.search(key, order)
        l = len(d)
        if l != 0:
            wx.PostEvent(self._notify_window, RangeEvent(l))
            for i in d:
                wx.PostEvent(self._notify_window, DataEvent(i))
                self.update_progress()
                time.sleep(0.0005)
        else:
            self.error_handler("data Kosong")

    def hash_file(self, file):
        result=[]
        cmd5="md5sum -b '%s'" % file
        cmdsha1="sha1sum -b '%s'" % file
        try:
            md5 = self.adb.shell_command(cmd5)
            sha1 = self.adb.shell_command(cmdsha1)
            result.append(md5)
            result.append(sha1)
            result.append(file)
            wx.PostEvent(self._notify_window, HashEvent(result))
        except Exception as e:
            self.error_handler(e.args[0])

    def view_project_info(self):
        d = self.data.select_evidence()
        wx.PostEvent(self._notify_window, ProjectEvent(d))


    def error_handler(self, error):
        wx.PostEvent(self._notify_window, ErrorEvent(error))

    def runSelectAll(self, order):
        self.__progress_value=0
        self.start_thread(self.view_all_data, order)

    def runHashFile(self, file):
        self.start_thread(self.hash_file, file)

    def runViewProject(self):
        self.start_thread(self.view_project_info)

    def runSelectByExt(self, ext, order):
        self.__progress_value = 0
        self.start_thread(self.view_data_by_ext, ext, order)

    def runSearchData(self, key, order):
        self.__progress_value = 0
        self.start_thread(self.search_data, key, order)

    def runViewLogPull(self):
        self.start_thread(self.view_log_pull)
