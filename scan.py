from data import data
import wx
import wx.lib.newevent
from pyand import ADB, Fastboot
from threading import *

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
    __progress_value = 1

    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.start()

    def run(self):
        try:
            ADB().get_devices()
            if not ADB().set_target_by_id(0):
                self.errorHandler("no device found in list")
        except Exception as e:
            self.errorHandler(e.args[0])

        cmd_result = ADB().shell_command("ls /vendor -R -l")
        array = self.create_array(cmd_result)
        arr = self.clean_array(array)
        range = self.count_file(arr)
        wx.PostEvent(self._notify_window, RangeEvent(range))
        self.insert_to_db(arr)

    def updateProgress(self):
        self.__progress_value=self.__progress_value+1
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
            return len(result)
        except Exception as e:
            self.errorHandler(e.args[0])

    def insert_to_db(self, array):
        n = 0
        try:
            for i in array:
                per = array[n][0]
                if per.endswith(":"):
                    id_dir = None
                    data().insert_dir(array[n][-1])
                    id = data().select_id_dir_by_name(array[n][-1])
                    id_dir = id
                    self.updateProgress()
                elif per[:1] == "-":
                    db=data().insert_file(id_dir, array[n][-1])
                    self.updateProgress()
                    self.errorHandler(db)
                n = n + 1
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
            return o
        except Exception as e:
            self.errorHandler(e.args[0])

    def clean_array(self, array):
        n = 0
        result = []
        try:
            for i in array:
                lengt = len(array[n])
                if lengt >= 1 and lengt != 2:#menghilangkan array yang kosong dan kata "total"
                    result.append(array[n])
                n = n + 1
            return result
        except Exception as e:
            self.errorHandler(e.args[0])

    def abort(self):
        self._want_abort = 1

class scan(wx.Frame):
    __adb = ADB()

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(450, 150), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.status = wx.StaticText(self, wx.ID_ANY, u"Scan Progress", wx.DefaultPosition, wx.DefaultSize, 0)
        self.status.Wrap(-1)
        bSizer1.Add(self.status, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.prgsBar_scan = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        bSizer1.Add(self.prgsBar_scan, 0, wx.ALL | wx.EXPAND, 5)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        self.btn_startScan = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.btn_startScan, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.btn_stop_scan = wx.Button(self, wx.ID_ANY, u"stop", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.btn_stop_scan, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer1.Add(gSizer1, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        RANGE_RESULT(self, self.OnResult)
        PROGRESS_RESULT(self, self.OnProgress)
        ERROR_RESULT(self, self.OnError)

        # And indicate we don't have a worker thread yet
        self.worker = None

        # Connect Events
        self.btn_startScan.Bind(wx.EVT_BUTTON, self.start_scan)
        self.btn_stop_scan.Bind(wx.EVT_BUTTON, self.stop_scan)


    def __del__(self):
        pass

    def start_scan(self, event):
        if not self.worker:
            self.worker = scanRecursive(self)

    def stop_scan(self, event):
        if self.worker:
            self.worker.abort()

    def OnResult(self, event):
        self.status.SetLabel("Menghitung direktori, mohon tunggu..")
        self.prgsBar_scan.SetRange(event.range)

    def OnProgress(self, event):
        self.status.SetLabel("Memasukan data ke DB..")
        self.prgsBar_scan.SetValue(event.val)

    def OnError(self, event):
        self.worker.abort()
        wx.MessageBox(str(event.error), 'Warning', wx.OK | wx.ICON_WARNING)


