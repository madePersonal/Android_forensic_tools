from data import data
import wx
import wx.lib.newevent
from pyand import ADB, Fastboot
from threading import *

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, val):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.val = val

class thread(Thread):
    __data = data()
    __adb = ADB()
    __progress_value = 1
    def __init__(self, notify_window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def updateProgress(self):
        self.__progress_value=self.__progress_value+1
        wx.PostEvent(self._notify_window, ResultEvent(self.__progress_value))

    def run(self):
        self.insertToDB("/vendor")

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1

    def creat_array(self, text):
        n = 0
        o = []
        line = text.split("\n")
        for l in line:
            y = (str(line[n]).split(" "))
            h = filter(None, y)
            if '->' in h:
                h.remove('->')
            o.append(h)
            n = n + 1
        del o[0]
        return o

    def insertToDB(self, dir):
        self.__data.insert_dir(dir)
        id_dir = 1
        text = self.__adb.shell_command('ls '+dir+' -l')
        array = self.creat_array(text)

        a = len(array)
        if a > 1:
            n = 0
            for l in array:
                permmisison = array[n][0]  # permisison berada pada indek ke 0
                if "d" == permmisison[:1]:  # mencocokan kode pada huruf awal permisison (d berarti direktori)
                    self.__data.insert_sub_dir(id_dir, array[n][7] + "/")
                    self.updateProgress()
                elif "-" == permmisison[:1]:  # mencocokan kode pada huruf awal permisison (- berarti file)
                    self.__data.insert_file(id_dir, array[n][7])
                    self.updateProgress()
                if n < (a - 2):
                    n = n + 1
                else:
                    break

            dir_name = self.__data.select_name_by_id_dir(id_dir)
            for u in dir_name:
                self.insertToDB2(dir + u[0])

            while True:
                id_dir = id_dir + 1
                dir_name = self.__data.select_name_dir_subDir(id_dir)
                try:
                    for u in dir_name:
                        self.insertToDB2(u[0] + u[1])
                except Exception as e:
                    print(e.args[0])
                    break

    def insertToDB2(self, dir):
        id_dir = ""
        self.__data.insert_dir(dir)
        id = self.__data.select_id_dir_by_name(dir)
        for k in id:
            id_dir = k[0]

        text = self.__adb.shell_command('ls ' + dir + ' -l')
        array = self.creat_array(text)

        a = len(array)
        if a > 1:
            n = 0
            for l in array:
                permmisison = array[n][0]  # permisison berada pada indek ke 0
                if "d" == permmisison[:1]:  # mencocokan kode pada huruf awal permisison (d berarti direktori)
                    self.__data.insert_sub_dir(id_dir, array[n][7] + "/")
                    self.updateProgress()
                elif "-" == permmisison[:1]:  # mencocokan kode pada huruf awal permisison (- berarti file)
                    self.__data.insert_file(id_dir, array[n][7])
                    self.updateProgress()
                if n < (a - 2):
                    n = n + 1
                else:
                    break


class scan(wx.Frame):
    __adb = ADB()
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(450, 150), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"Scan Progress", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer1.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.prgsBar_scan = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        bSizer1.Add(self.prgsBar_scan, 0, wx.ALL | wx.EXPAND, 5)

        self.btn_startScan = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.btn_startScan, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Set up event handler for any worker thread results
        EVT_RESULT(self, self.OnResult)

        # And indicate we don't have a worker thread yet
        self.worker = None

        # Connect Events
        self.btn_startScan.Bind(wx.EVT_BUTTON, self.start_scan)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def start_scan(self, event):
        try:
            self.__adb.get_devices()
            self.__adb.set_target_by_id(0)
        except Exception as e:
            print(e.args[0])
        try:
            text = self.__adb.shell_command("ls /vendor -R -l")
            jml = self.count_array(text)
            self.prgsBar_scan.SetRange(jml)
        except Exception as e:
            print(e.args[0])

        if not self.worker:
            self.worker = thread(self)
        self.worker = None


    def count_array(self, text):
        n = 0
        o = []
        line = text.split("\n")
        for l in line:
            y = (str(line[n]).split(" "))
            h = filter(None, y)
            if '->' in h:
                h.remove('->')
            o.append(h)
            n = n + 1
        del o[0]
        del o[0]
        j = len(o)
        j = j-1
        return j

    def OnResult(self, event):
        self.prgsBar_scan.SetValue(event.val)

