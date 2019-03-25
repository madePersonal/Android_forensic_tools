import wx
from Pull import *

class PullFrame(wx.Frame):

    def __init__(self, parent, file):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="pull file", pos=wx.DefaultPosition,
                          size=wx.Size(400, 350), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.file = file
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"evidence"), wx.VERTICAL)

        gSizer2 = wx.GridSizer(4, 2, 0, 0)

        self.case_number = wx.StaticText(self, wx.ID_ANY, u"Case number", wx.DefaultPosition, wx.DefaultSize, 0)
        self.case_number.Wrap(-1)
        gSizer2.Add(self.case_number, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.text_case_number = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.text_case_number, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

        self.description = wx.StaticText(self, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, 0)
        self.description.Wrap(-1)
        gSizer2.Add(self.description, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.text_description = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.text_description, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, u"Examiner", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)
        gSizer2.Add(self.m_staticText12, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.text_examiner = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.text_examiner, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

        self.notes = wx.StaticText(self, wx.ID_ANY, u"Notes", wx.DefaultPosition, wx.DefaultSize, 0)
        self.notes.Wrap(-1)
        gSizer2.Add(self.notes, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.text_note = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.text_note, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

        sbSizer1.Add(gSizer2, 1, wx.EXPAND, 5)

        bSizer1.Add(sbSizer1, 1, wx.EXPAND, 5)

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
        examiner = self.text_examiner.GetValue()
        case_number = self.text_case_number.GetValue()
        description = self.text_description.GetValue()
        notes = self.text_note.GetValue()

        if dir =="" or dir ==" ":
            wx.MessageBox("directory belum ditentukan", 'Warning', wx.OK | wx.ICON_WARNING)
        elif examiner == "":
            wx.MessageBox("Examiner canot empty", 'Warning', wx.OK | wx.ICON_WARNING)
        elif case_number == "":
            wx.MessageBox("Case number canot empty", 'Warning', wx.OK | wx.ICON_WARNING)
        elif description == "":
            wx.MessageBox("Description canot empty", 'Warning', wx.OK | wx.ICON_WARNING)
        elif notes == "":
            wx.MessageBox("Notes canot empty", 'Warning', wx.OK | wx.ICON_WARNING)
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


