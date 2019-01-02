# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Sep 12 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
import sys
import wx
import wx.richtext
from adult import adult


###########################################################################
## Class MyFrame1
###########################################################################
class MyFrame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(700, 500), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        gSizer1 = wx.GridSizer(1, 2, 0, 0)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.scan_device = wx.Button(self, wx.ID_ANY, u"Scan devices", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.scan_device, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"devices"), wx.VERTICAL)

        self.deviceResult = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                     wx.DefaultSize,
                                                     0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        sbSizer2.Add(self.deviceResult, 1, wx.EXPAND, 5)

        bSizer3.Add(sbSizer2, 1, wx.EXPAND, 5)

        gSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        gSizer5 = wx.GridSizer(1, 3, 0, 0)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"ADB Shell :", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        gSizer5.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.input_command = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer5.Add(self.input_command, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.run_commands = wx.Button(self, wx.ID_ANY, u"Run", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer5.Add(self.run_commands, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(gSizer5, 0, 0, 5)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"command result"), wx.VERTICAL)

        self.commandsResult = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                       wx.DefaultSize,
                                                       0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        sbSizer1.Add(self.commandsResult, 1, wx.EXPAND, 5)

        bSizer1.Add(sbSizer1, 1, wx.EXPAND, 5)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"FIle"), wx.VERTICAL)

        self.list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        sbSizer3.Add(self.list, 10, wx.EXPAND, 5)

        bSizer1.Add(sbSizer3, 1, wx.EXPAND, 5)

        gSizer1.Add(bSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(gSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.scan_device.Bind(wx.EVT_BUTTON, self.scan_devices)
        self.run_commands.Bind(wx.EVT_BUTTON, self.run_command)

        self.list.InsertColumn(0, 'name', width=100)
        self.list.InsertColumn(1, 'runs', wx.LIST_FORMAT_RIGHT, 100)
        self.list.InsertColumn(2, 'wkts', wx.LIST_FORMAT_RIGHT, 100)


    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def scan_devices(self, event):
        # players = [['Tendulkar', '15000', '100'],['Dravid', '14000', '1'],
        #            ['Kumble', '1000', '700'],['KapilDev', '5000', '400'],
        #            ['Ganguly', '8000', '50']]
        # for i in players:
        #     index = self.list.InsertItem(sys.maxint, i[0])
        #     self.list.SetItem(index, 1, i[1])
        #     self.list.SetItem(index, 2, i[2])
        # event.Skip()
        # self.commandsResult.WriteText(str(index))

        adult(None).Show()


    def run_command(self, event):
        event.Skip()


if __name__ == '__main__' :
  app = wx.App()
  appFrame = MyFrame1(None).Show()
  app.MainLoop()

