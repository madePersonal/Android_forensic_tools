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
from pyand import ADB, Fastboot


###########################################################################
## Class MyFrame1
###########################################################################

class adult(wx.Frame):

    __device = None
    __deviceId = None
    __adb = ADB()

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(700, 500), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        gSizer1 = wx.GridSizer(1, 2, 0, 0)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.scanDevices = wx.Button(self, wx.ID_ANY, u"Scan devices", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.scanDevices, 0, wx.ALL | wx.EXPAND, 5)

        self.deviceResult = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                     wx.DefaultSize,
                                                     0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        bSizer2.Add(self.deviceResult, 1, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        gSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        fgSizer2 = wx.FlexGridSizer(1, 2, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.runCommand = wx.Button(self, wx.ID_ANY, u"Run", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.runCommand, 0, wx.ALL, 5)

        self.commandInput = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.commandInput, 0, wx.ALL, 5)

        bSizer3.Add(fgSizer2, 0, wx.EXPAND, 5)

        self.commandResult = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                      wx.DefaultSize,
                                                      0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        bSizer3.Add(self.commandResult, 1, wx.EXPAND | wx.ALL, 5)

        gSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        bSizer1.Add(gSizer1, 1, wx.EXPAND, 5)

        self.listFile = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        bSizer1.Add(self.listFile, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.scanDevices.Bind(wx.EVT_BUTTON, self.scan_devices)
        self.runCommand.Bind(wx.EVT_BUTTON, self.run_command)
        # table header
        self.listFile.InsertColumn(0, 'file', width=100)
        self.listFile.InsertColumn(1, 'last modifay', wx.LIST_FORMAT_CENTER, 100)
        self.listFile.InsertColumn(2, 'size', wx.LIST_FORMAT_CENTER, 100)
        self.listFile.InsertColumn(3, 'owner', wx.LIST_FORMAT_CENTER, 100)
        self.listFile.InsertColumn(4, 'permission', wx.LIST_FORMAT_CENTER, 100)


    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def scan_devices(self, event):
        self.deviceResult.Clear()
        try:
            self.__device = self.__adb.get_devices()
            self.__adb.set_target_by_id(0)
            model = self.__adb.get_model()
            version = self.__adb.get_version()
            serial = self.__adb.get_serialno()
            result = "Model :" + model + "\n" + "Devices :" + str(
                self.__device[0]) + "\n" + "Version :" + version + "\n" + "Serial No :" + serial
            self.deviceResult.WriteText(result)
        except:
            self.deviceResult.WriteText("[!] No Device/emulator found")
        event.Skip()

    def run_command(self, event):
        self.commandResult.Clear()
        commands = self.commandInput.GetValue()
        if not commands:
            self.commandResult.WriteText("input some command !!")
        else:
            self.__adb.run_cmd("adb shell")
            result = self.__adb.run_cmd(commands)

            self.commandResult.WriteText(result)
            array = self.creat_array(result)
            for i in array:
                index = self.listFile.InsertStringItem(sys.maxint, i[7])
                self.listFile.SetStringItem(index, 1, i[5]+" "+i[6])
                self.listFile.SetStringItem(index, 2, i[4])
                self.listFile.SetStringItem(index, 3, i[3])
                self.listFile.SetStringItem(index, 4, i[0])
        event.Skip()

    def creat_array(self, text):
        n = 0
        o = []
        line = text.split("\n")
        for l in line:
            y = (str(line[n]).split(" "))
            h = filter(None, y)
            if '->' in h:
                h.remove('->')
            o.append(h)
            n = n + 1
        del o[0]
        return o
