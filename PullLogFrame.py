import wx
import wx.richtext
from Main import DATA_RESULT, Main

class PullLogFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Pull log", pos=wx.DefaultPosition,
                          size=wx.Size(450, 500), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 73, 90, 90, False, wx.EmptyString))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_richText1 = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                    0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        self.m_richText1.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 76, 90, 90, False, wx.EmptyString))

        bSizer1.Add(self.m_richText1, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)
        DATA_RESULT(self, self.view_log)

        Main(self).runViewLogPull()

    def __del__(self):
        pass

    def view_log(self, event):
        file = "File \t:%s\n"%event.data[1]
        From = "From \t:%s\n"%event.data[2]
        to = "To \t\t:%s\n"%event.data[3]
        md5 = "MD5 \t:%s"%event.data[4]
        sha1 = "SHA1 \t:%s"%event.data[5]
        Date = "Date \t:%s\n"%event.data[6]
        line = "===================================================\n\n"
        self.m_richText1.WriteText(file+From+to+md5+sha1+Date+line)


