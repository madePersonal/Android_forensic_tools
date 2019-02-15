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

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.listctrl = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        # self.listctrl.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 73, 90, 90, False, wx.EmptyString, wx.FONTENCODING_UTF8))
        bSizer1.Add(self.listctrl, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
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

        #run hex
        hex = Hex(self)
        hex.run_hex(title)

    def __del__(self):
        pass

    def ParsingData(self, event):
        hex = event.hex
        binary = event.binary
        index=self.listctrl.InsertItem(sys.maxint, hex[0])
        self.listctrl.SetItem(index, 1, hex[1])
        self.listctrl.SetItem(index, 2, hex[2])
        self.listctrl.SetItem(index, 3, hex[3])
        self.listctrl.SetItem(index, 4, hex[4])
        self.listctrl.SetItem(index, 5, hex[5])
        self.listctrl.SetItem(index, 6, hex[6])
        self.listctrl.SetItem(index, 7, hex[7])
        self.listctrl.SetItem(index, 8, hex[8])
        self.listctrl.SetItem(index, 9, hex[9])
        self.listctrl.SetItem(index, 10, hex[10])
        self.listctrl.SetItem(index, 11, hex[11])
        self.listctrl.SetItem(index, 12, hex[12])
        self.listctrl.SetItem(index, 13, hex[13])
        self.listctrl.SetItem(index, 14, hex[14])
        self.listctrl.SetItem(index, 15, hex[15])
        self.listctrl.SetItem(index, 16, binary)

    def OnError(self, event):
        wx.MessageBox(str(event.error), 'Warning', wx.OK | wx.ICON_WARNING)
