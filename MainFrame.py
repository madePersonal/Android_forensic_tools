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
from pyand import *
from ScanFrame import ScanFrame
from main import *
import wx.lib.newevent

class MainFrame(wx.Frame):
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
        sbSizer1.Add(self.btn_detectDevice, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.btn_scan = wx.Button(self, wx.ID_ANY, u"Scan", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer1.Add(self.btn_scan, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.btn_viewData = wx.Button(self, wx.ID_ANY, u"tampilkan data", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer1.Add(self.btn_viewData, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.progress_bar = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        sbSizer1.Add(self.progress_bar, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.RIGHT | wx.LEFT, 5)

        self.view_progress = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.view_progress.Wrap(-1)
        sbSizer1.Add(self.view_progress, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

        gSizer1.Add(sbSizer1, 1, wx.EXPAND, 5)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"device info"), wx.VERTICAL)

        self.txtview_deviceInfo = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                           wx.DefaultSize,
                                                           0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        sbSizer3.Add(self.txtview_deviceInfo, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 5)

        gSizer1.Add(sbSizer3, 1, wx.EXPAND, 5)

        bSizer1.Add(gSizer1, 1, wx.EXPAND, 5)

        file_extChoices = [u"all file", u"MP4", u"MP3", u"PDF", u"doc", u"MKV", u"log"]
        self.file_ext = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, file_extChoices, 0)
        self.file_ext.SetSelection(0)
        bSizer1.Add(self.file_ext, 0, wx.ALL, 5)

        self.listFile = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        bSizer1.Add(self.listFile, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.menubar1 = wx.MenuBar(0)
        self.SetMenuBar(self.menubar1)

        self.Centre(wx.BOTH)

        self.worker = None

        # table header
        self.listFile.InsertColumn(0, 'lokasi', width=250)
        self.listFile.InsertColumn(1, 'file', wx.LIST_FORMAT_CENTER, 150)
        self.listFile.InsertColumn(2, 'permission', wx.LIST_FORMAT_CENTER, 150)
        self.listFile.InsertColumn(3, 'size', wx.LIST_FORMAT_CENTER, 150)
        self.listFile.InsertColumn(4, 'date', wx.LIST_FORMAT_CENTER, 150)

        # Connect Events
        self.btn_detectDevice.Bind(wx.EVT_BUTTON, self.detect_device)
        self.btn_scan.Bind(wx.EVT_BUTTON, self.show_scan)
        self.btn_viewData.Bind(wx.EVT_BUTTON, self.view_all_data)
        self.file_ext.Bind(wx.EVT_CHOICE, self.view_data_by_ext)

        DATA_RESULT(self, self.ParsingData)
        RANGE_RESULT(self, self.OnResult)
        PROGRESS_RESULT(self, self.OnProgress)
        ERROR_RESULT(self, self.OnError)

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

    def show_scan(self, event):
        ScanFrame(None).Show()

    def view_data_by_ext(self, event):
        self.listFile.DeleteAllItems()
        d=self.file_ext.GetStringSelection()
        main(self).runSelectByExt(ext=d)

    def view_all_data(self, event):
        if not self.worker:
            self.listFile.DeleteAllItems()
            self.worker = main(self).runSelectAll()

    def ParsingData(self, event):
        data = event.data
        index=self.listFile.InsertItem(sys.maxint, data[0])
        self.listFile.SetItem(index, 1, str(data[2]))
        self.listFile.SetItem(index, 2, str(data[3]))
        self.listFile.SetItem(index, 3, str(data[4]))
        self.listFile.SetItem(index, 4, str(data[5]))

    def OnResult(self, event):
        self.progress_bar.ClearBackground()
        self.progress_bar.SetRange(event.range)

    def OnProgress(self, event):
        r = self.progress_bar.GetRange()
        v = event.val
        p = (float(v)/float(r))*float(100)
        self.view_progress.SetLabel(str(round(p, 1))+"%")
        self.progress_bar.SetValue(event.val)

    def OnError(self, event):
        wx.MessageBox(str(event.error), 'Warning', wx.OK | wx.ICON_WARNING)

if __name__ == '__main__' :
  app = wx.App(False)
  appFrame = MainFrame(None).Show()
  app.MainLoop()
