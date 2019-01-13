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
from data import data


###########################################################################
## Class MyFrame1
###########################################################################

class Main(wx.Frame):
    __adb = ADB()
    __data = data()

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(800, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        gSizer1 = wx.GridSizer(1, 2, 0, 0)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Action"), wx.VERTICAL)

        self.btn_detectDevice = wx.Button(self, wx.ID_ANY, u"detect device", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer1.Add(self.btn_detectDevice, 0, wx.ALL | wx.EXPAND, 5)

        self.btn_fullScan = wx.Button(self, wx.ID_ANY, u"Full scan", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer1.Add(self.btn_fullScan, 0, wx.ALL | wx.EXPAND, 5)

        self.btn_sdcardScan = wx.Button(self, wx.ID_ANY, u"sdcard scan", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer1.Add(self.btn_sdcardScan, 0, wx.ALL | wx.EXPAND, 5)

        gSizer1.Add(sbSizer1, 1, wx.EXPAND, 5)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"device info"), wx.VERTICAL)

        self.txtview_deviceInfo = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                           wx.DefaultSize,
                                                           0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        sbSizer3.Add(self.txtview_deviceInfo, 1, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

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
        self.listFile.InsertColumn(0, 'lokasi', width=150)
        self.listFile.InsertColumn(1, 'file', wx.LIST_FORMAT_CENTER, 150)
        self.listFile.InsertColumn(2, 'permission', wx.LIST_FORMAT_CENTER, 150)
        self.listFile.InsertColumn(3, 'size', wx.LIST_FORMAT_CENTER, 150)
        self.listFile.InsertColumn(4, 'date', wx.LIST_FORMAT_CENTER, 150)

        # Connect Events
        self.btn_detectDevice.Bind(wx.EVT_BUTTON, self.detect_device)
        self.btn_fullScan.Bind(wx.EVT_BUTTON, self.full_scan)
        self.btn_sdcardScan.Bind(wx.EVT_BUTTON, self.sdcard_scan)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def detect_device(self, event):
        self.txtview_deviceInfo.Clear()
        try:
            device = self.__adb.get_devices()
            self.__adb.set_target_by_id(0)

            device_manufaktur = self.__adb.shell_command("getprop | grep manufacturer")
            and_version = self.__adb.shell_command("getprop | grep version.release")
            model = self.__adb.shell_command("getprop | grep model")
            name = self.__adb.shell_command("getprop | grep name")
            brand = self.__adb.shell_command("getprop | grep brand")
            build_id = self.__adb.shell_command("getprop | grep build.id")
            serial = self.__adb.shell_command("getprop | grep ro.serial")

            result = device_manufaktur+model+and_version+name+brand+build_id+serial
            self.txtview_deviceInfo.WriteText(result)
        except:
            self.txtview_deviceInfo.WriteText("[!] No Device/emulator found")
        event.Skip()

    def full_scan(self, event):
        data = self.__data.select_all_data()
        for i in data:
            index = self.listFile.InsertItem(sys.maxint, i[0])
            self.listFile.SetItem(index, 1, str(i[2]))
            self.listFile.SetItem(index, 2, i[2])
            # self.listFile.SetItem(index, 3, i[4])
            # self.listFile.SetItem(index, 4, i[5])
        event.Skip()

    def sdcard_scan(self, event):
        event.Skip()

if __name__ == '__main__' :
  app = wx.App()
  appFrame = Main(None).Show()
  app.MainLoop()