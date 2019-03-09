# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Sep 12 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
import sys
from Hex import *
import wx

###########################################################################
## Class HexFrame
###########################################################################



class HexFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition,
                          size=wx.Size(600, 700), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.file = title

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        self.bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.progress_label = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.progress_label.Wrap(-1)
        self.bSizer1.Add(self.progress_label, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.progress_bar = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.bSizer1.Add(self.progress_bar, 0, wx.ALL | wx.EXPAND, 5)

        self.listctrl = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        self.listctrl.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 76, 90, 90, False, wx.EmptyString))

        self.bSizer1.Add(self.listctrl, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)


        # table header
        width = 25
        align = wx.LIST_FORMAT_CENTRE
        self.listctrl.InsertColumn(0, wx.EmptyString, align,width)
        self.listctrl.InsertColumn(1, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(2, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(3, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(4, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(5, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(6, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(7, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(8, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(9, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(10, wx.EmptyString, align,width)
        self.listctrl.InsertColumn(11, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(12, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(13, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(14, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(15, wx.EmptyString, align, width)
        self.listctrl.InsertColumn(16, wx.EmptyString, wx.LIST_FORMAT_LEFT, 200)

        # Connect Event pull
        HEX_RESULT(self, self.ParsingData)
        ERROR_RESULT(self, self.OnError)
        RANGE_RESULT(self, self.set_range)
        PROGRESS_RESULT(self, self.OnProgress)

        #run hex
        hex = Hex(self, self.file)
        hex.run_hex()

    def __del__(self):
        pass

    def ParsingData(self, event):
        hex = event.hex
        binary = event.binary
        index=self.listctrl.InsertItem(sys.maxint, str(hex[0]).upper())
        self.listctrl.SetItem(index, 1, str(hex[1]).upper())
        self.listctrl.SetItem(index, 2, str(hex[2]).upper())
        self.listctrl.SetItem(index, 3, str(hex[3]).upper())
        self.listctrl.SetItem(index, 4, str(hex[4]).upper())
        self.listctrl.SetItem(index, 5, str(hex[5]).upper())
        self.listctrl.SetItem(index, 6, str(hex[6]).upper())
        self.listctrl.SetItem(index, 7, str(hex[7]).upper())
        self.listctrl.SetItem(index, 8, str(hex[8]).upper())
        self.listctrl.SetItem(index, 9, str(hex[9]).upper())
        self.listctrl.SetItem(index, 10, str(hex[10]).upper())
        self.listctrl.SetItem(index, 11, str(hex[11]).upper())
        self.listctrl.SetItem(index, 12, str(hex[12]).upper())
        self.listctrl.SetItem(index, 13, str(hex[13]).upper())
        self.listctrl.SetItem(index, 14, str(hex[14]).upper())
        self.listctrl.SetItem(index, 15, str(hex[15]).upper())
        self.listctrl.SetItem(index, 16, binary)

    def set_range(self, event):
        self.progress_bar.SetRange(event.range)
        self.range=self.progress_bar.GetRange()

    def OnProgress(self, event):
        r = float(self.range)
        v = float(event.progress)
        p = v/r*100.0

        self.progress_label.SetLabel(str(round(p, 1)) + "%")
        self.progress_bar.SetValue(event.progress)
        if p == 100.0:
            self.progress_label.Hide()
            self.progress_bar.Hide()
            self.FitInside()

    def OnError(self, event):
        wx.MessageBox(str(event.error), 'Warning', wx.OK | wx.ICON_WARNING)