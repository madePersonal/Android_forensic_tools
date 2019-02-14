import wx
from Pull import *

class PullFrame(wx.Frame):

    def __init__(self, parent, file):
        self.file=file
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="pull file", pos=wx.DefaultPosition,
                          size=wx.Size(350, 125), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.dir_picker = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition,
                                           wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
        bSizer1.Add(self.dir_picker, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, " ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer1.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.btn_save = wx.Button(self, wx.ID_ANY, u"save", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.btn_save, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.btn_save.Bind(wx.EVT_BUTTON, self.save_file)

        #Connect Event pull
        RESULT(self, self.OnResult)
        ERROR(self, self.OnError)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def save_file(self, event):
        dir = self.dir_picker.GetPath()
        if dir =="" or dir ==" ":
            wx.MessageBox("directory belum ditentukan", 'Warning', wx.OK | wx.ICON_WARNING)
        else:
            self.m_staticText1.SetLabel("copying..")
            Pull(self).runPullFile(self.file, dir)
        event.Skip()

    def OnResult(self, event):
        self.m_staticText1.SetLabel(event.val)

    def OnError(self, event):
        wx.MessageBox(event.error, 'Warning', wx.OK | wx.ICON_WARNING)


