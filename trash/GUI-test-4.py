# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep 12 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.richtext


###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(800, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        gSizer1 = wx.GridSizer(1, 2, 0, 0)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Action"), wx.VERTICAL)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"detect device", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer1.Add(self.m_button3, 0, wx.ALL | wx.EXPAND, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"Full scan", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer1.Add(self.m_button1, 0, wx.ALL | wx.EXPAND, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"sdcard scan", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer1.Add(self.m_button2, 0, wx.ALL | wx.EXPAND, 5)

        gSizer1.Add(sbSizer1, 1, wx.EXPAND, 5)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"device info"), wx.VERTICAL)

        self.m_richText1 = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                    0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        sbSizer3.Add(self.m_richText1, 1, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        gSizer1.Add(sbSizer3, 1, wx.EXPAND, 5)

        bSizer1.Add(gSizer1, 1, wx.EXPAND, 5)

        m_choice2Choices = [u"all file", u"MP4", u"MP3", u"PDF", u"doc", u"MKV"]
        self.m_choice2 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0)
        self.m_choice2.SetSelection(0)
        bSizer1.Add(self.m_choice2, 0, wx.ALL, 5)

        self.listFile = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        bSizer1.Add(self.listFile, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)
        # table header
        self.listFile.InsertColumn(0, 'name', width=100)
        self.listFile.InsertColumn(1, 'last modifay', wx.LIST_FORMAT_CENTER, 100)
        self.listFile.InsertColumn(2, 'size', wx.LIST_FORMAT_CENTER, 100)
        self.listFile.InsertColumn(3, 'owner', wx.LIST_FORMAT_CENTER, 100)
        self.listFile.InsertColumn(4, 'permission', wx.LIST_FORMAT_CENTER, 100)

    def __del__(self):
        pass


if __name__ == '__main__' :
  app = wx.App()
  appFrame = MyFrame1(None).Show()
  app.MainLoop()