import wx
import ActiveProject


PROJECT_OPEN_ID = wx.NewId()

def OPEN_RESULT(win, func):
    win.Connect(-1, -1, PROJECT_OPEN_ID, func)

class OpenProjectEvent(wx.PyEvent):
    def __init__(self):
        wx.PyEvent.__init__(self)
        self.SetEventType(PROJECT_OPEN_ID)

class OpenProjectDialog(wx.Dialog):

    def __init__(self, parent, notifay_window):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="open Project", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self._notifay_window = notifay_window
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.file_picker = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a file", u".db",
                                             wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        bSizer1.Add(self.file_picker, 0, wx.ALL, 5)

        self.btn_open = wx.Button(self, wx.ID_ANY, u"Open", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.btn_open, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        bSizer1.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.btn_open.Bind(wx.EVT_BUTTON, self.open_file)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def open_file(self, event):
        try:
            ActiveProject.init(self.file_picker.GetPath())
            wx.PostEvent(self._notifay_window, OpenProjectEvent())
        finally:
            self.Close()
        event.Skip()