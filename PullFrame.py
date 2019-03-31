import wx
from Pull import *
import ActiveProject

class PullFrame(wx.Frame):

    def __init__(self, parent, file):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="pull file", pos=wx.DefaultPosition,
                          size=wx.Size(400, 200), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.file = file
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"destination"), wx.VERTICAL)

        self.dir_picker = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition,
                                           wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
        sbSizer2.Add(self.dir_picker, 0, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(sbSizer2, 0, wx.EXPAND, 5)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer1.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.prgs_bar = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        bSizer1.Add(self.prgs_bar, 0, wx.ALL | wx.EXPAND, 5)

        self.btn_save = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.btn_save, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.btn_save.Bind(wx.EVT_BUTTON, self.save_file)

        #Connect Event pull
        RESULT(self, self.OnResult)
        ERROR(self, self.OnError)
        PROGRESS(self, self.OnProgress)

    def __del__(self):
        pass

    def save_file(self, event):
        dir = self.dir_picker.GetPath()
        print(ActiveProject.project)
        if dir =="" or dir ==" ":
            wx.MessageBox("directory belum ditentukan", 'Warning', wx.OK | wx.ICON_WARNING)
        else:
            Pull(self).runPullFile(self.file, dir)
        event.Skip()

    def OnProgress(self, event):
        self.prgs_bar.SetValue(event.progress)
        self.m_staticText1.SetLabel(event.stat)

    def OnResult(self, event):
        self.prgs_bar.SetRange(event.val)

    def OnError(self, event):
        wx.MessageBox(event.error, 'Warning', wx.OK | wx.ICON_WARNING)


