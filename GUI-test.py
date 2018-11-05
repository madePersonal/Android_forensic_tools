# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Sep 12 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.richtext
from pyand import ADB, Fastboot
import json


###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1(wx.Frame):

    __device = None
    __deviceId = None
    __adb = ADB()

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

        self.m_genericDirCtrl2 = wx.GenericDirCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                   wx.DIRCTRL_3D_INTERNAL | wx.SUNKEN_BORDER, wx.EmptyString, 0)

        self.m_genericDirCtrl2.ShowHidden(False)
        sbSizer3.Add(self.m_genericDirCtrl2, 1, wx.EXPAND, 5)

        bSizer1.Add(sbSizer3, 1, wx.EXPAND, 5)

        gSizer1.Add(bSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(gSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.scan_device.Bind(wx.EVT_BUTTON, self.scan_devices)
        self.run_commands.Bind(wx.EVT_BUTTON, self.run_command)

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
            result = "Model :" + model + "\n" + "Devices :" + str(self.__device[0]) + "\n" + "Version :" + version + "\n" + "Serial No :" + serial
            self.deviceResult.WriteText(result)
        except:
            self.deviceResult.WriteText("[!] No Device/emulator found")
        event.Skip()

    def run_command(self, event):
        self.commandsResult.Clear()
        commands = self.input_command.GetValue()
        if not commands :
            self.commandsResult.WriteText("input some command !!")
        else:
            result = self.__adb.shell_command(commands)
            self.commandsResult.WriteText(result)
        self.m_genericDirCtrl2.SetPath("/Users/sartika/Documents")
        event.Skip()


if __name__ == '__main__' :
  app = wx.App()
  appFrame = MyFrame1(None).Show()
  app.MainLoop()

