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
        bSizer1.Add(self.listctrl, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # table header
        self.listctrl.InsertColumn(0, 'Byte', wx.LIST_FORMAT_LEFT,width=400)
        self.listctrl.InsertColumn(1, 'utf-8', wx.LIST_FORMAT_LEFT, 200)

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
        index=self.listctrl.InsertItem(sys.maxint, hex)
        self.listctrl.SetItem(index, 1, binary)

    def OnError(self, event):
        wx.MessageBox(str(event.error), 'Warning', wx.OK | wx.ICON_WARNING)

