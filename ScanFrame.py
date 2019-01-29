import wx
from scan import *

class ScanFrame(wx.Frame):
    __adb = ADB()

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(450, 150), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        fgSizer2 = wx.FlexGridSizer(1, 2, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.label_scan_type = wx.StaticText(self, wx.ID_ANY, u"scan Type", wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_scan_type.Wrap(-1)
        fgSizer2.Add(self.label_scan_type, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        scan_type_choiceChoices = [u"full (/)", u"internal sdcard (/sdcard/)", u"eksternal sdcard (/storage/sdcard/))"]
        self.scan_type_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, scan_type_choiceChoices,
                                          0)
        self.scan_type_choice.SetSelection(0)
        fgSizer2.Add(self.scan_type_choice, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        bSizer1.Add(fgSizer2, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.status = wx.StaticText(self, wx.ID_ANY, u"SCAN", wx.DefaultPosition, wx.DefaultSize, 0)
        self.status.Wrap(-1)
        bSizer1.Add(self.status, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.prgsBar_scan = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        bSizer1.Add(self.prgsBar_scan, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

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
            dir = None
            type = self.scan_type_choice.GetCurrentSelection()
            self.status.SetLabel("Menghitung direktori, mohon tunggu..")
            if type == 0:
                dir = "/"
            elif type == 1:
                dir = "/sdcard/"
            elif type == 2:
                dir = "/storage/sdcard1/"
            self.worker = scanRecursive(self).run_scan(dir)

    def stop_scan(self, event):
        if self.worker:
            self.status.SetLabel("Stoped..")
            scanRecursive(self).abort()

    def OnResult(self, event):
        self.prgsBar_scan.SetRange(0)
        self.prgsBar_scan.SetRange(event.range)

    def OnProgress(self, event):
        r = float(self.prgsBar_scan.GetRange())
        v = float(event.val)
        p = (v/r)*100.0
        self.status.SetLabel(str(round(p,2))+"%")
        self.prgsBar_scan.SetValue(event.val)

    def OnError(self, event):
        scanRecursive(self).abort()
        wx.MessageBox(str(event.error), 'Warning', wx.OK | wx.ICON_WARNING)