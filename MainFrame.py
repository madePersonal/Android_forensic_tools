import sys
import wx
import wx.richtext
from pyand import ADB
from ScanFrame import ScanFrame
from Main import Main, PROJECT_RESULT, HASH_RESULT, DATA_RESULT, ERROR_RESULT, RANGE_RESULT, PROGRESS_RESULT
from PullFrame import PullFrame
from HexFrame import HexFrame
from OpenProjectDialog import OpenProjectDialog, OPEN_RESULT
from PullLogFrame import PullLogFrame
import wx.lib.newevent
import wx.lib.mixins.listctrl as listmix
from NewProjectFrame import NewProjectFrame, P_RESULT
import ActiveProject

class MainFrame(wx.Frame):
    __adb = ADB()

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="andr list and pull file demo - MD Sartika (15074)", pos=wx.DefaultPosition,
                          size=wx.Size(800, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL | wx.FRAME_SHAPED)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        gSizer1 = wx.GridSizer(1, 3, 0, 0)

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

        sbSizer31 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"project info"), wx.VERTICAL)

        self.textview_projectinfo = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                             wx.DefaultSize,
                                                             0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        sbSizer31.Add(self.textview_projectinfo, 1, wx.EXPAND | wx.ALL, 5)

        gSizer1.Add(sbSizer31, 1, wx.EXPAND, 5)

        bSizer1.Add(gSizer1, 1, wx.EXPAND, 5)

        fgSizer1 = wx.FlexGridSizer(1, 6, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.label_file_type = wx.StaticText(self, wx.ID_ANY, u"file type", wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_file_type.Wrap(-1)
        fgSizer1.Add(self.label_file_type, 0, wx.ALL, 5)

        file_extChoices = [u"all file", u"MP4", u"MP3", u"PDF", u"doc", u"MKV", u"log"]
        self.file_ext = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, file_extChoices, 0)
        self.file_ext.SetSelection(0)
        fgSizer1.Add(self.file_ext, 0, wx.ALL, 5)

        self.label_short_by = wx.StaticText(self, wx.ID_ANY, u"short by", wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_short_by.Wrap(-1)
        fgSizer1.Add(self.label_short_by, 0, wx.ALL, 5)

        shortBy_choiceChoices = [u"size", u"date"]
        self.shortBy_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, shortBy_choiceChoices, 0)
        self.shortBy_choice.SetSelection(0)
        fgSizer1.Add(self.shortBy_choice, 0, wx.ALL, 5)

        self.txtctrl_search = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.txtctrl_search, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.btn_search = wx.Button(self, wx.ID_ANY, u"search", wx.Point(-1, -1), wx.DefaultSize, wx.BU_RIGHT)
        fgSizer1.Add(self.btn_search, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        bSizer1.Add(fgSizer1, 0, wx.EXPAND, 5)

        self.listFile = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        bSizer1.Add(self.listFile, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        self.worker = None

        #klik kanan menu
        ID_MENU1 = wx.NewId()
        ID_MENU2 = wx.NewId()
        ID_MENU3 = wx.NewId()
        self.menu=wx.Menu()
        self.menu.Append(ID_MENU1, "Checksum")
        self.menu.Append(ID_MENU2, "Pull")
        self.menu.Append(ID_MENU3, "view Hex")

        #menu bar
        NEW_PROJECT_ID = wx.NewId()
        LOAD_PROJECT_ID = wx.NewId()
        VIEW_LOG_PULL_ID = wx.NewId()
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        viewMenu = wx.Menu()
        newProjectItem = fileMenu.Append(NEW_PROJECT_ID, "New project")
        openProjectItem = fileMenu.Append(LOAD_PROJECT_ID, "Open project")
        viewPullLogItem = viewMenu.Append(VIEW_LOG_PULL_ID, "View pull log")
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(viewMenu, "&View")
        self.SetMenuBar(menuBar)

        # table header
        self.listFile.InsertColumn(0, 'lokasi', width=290)
        self.listFile.InsertColumn(1, 'file', wx.LIST_FORMAT_CENTER, 200)
        self.listFile.InsertColumn(2, 'permission', wx.LIST_FORMAT_CENTER, 100)
        self.listFile.InsertColumn(3, 'size', wx.LIST_FORMAT_CENTER, 100)
        self.listFile.InsertColumn(4, 'date', wx.LIST_FORMAT_CENTER, 100)

        # Connect Events
        self.btn_detectDevice.Bind(wx.EVT_BUTTON, self.detect_device)
        self.btn_scan.Bind(wx.EVT_BUTTON, self.show_scan)
        self.btn_viewData.Bind(wx.EVT_BUTTON, self.view_all_data)
        self.file_ext.Bind(wx.EVT_CHOICE, self.view_data_by_ext)
        self.btn_search.Bind(wx.EVT_BUTTON, self.search_data)
        self.listFile.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.item_right_click)

        self.Bind(wx.EVT_MENU, self.view_hash, id=ID_MENU1)
        self.Bind(wx.EVT_MENU, self.pull_file, id=ID_MENU2)
        self.Bind(wx.EVT_MENU, self.hex_sum, id=ID_MENU3)

        # connect event menubar
        self.Bind(wx.EVT_MENU, self.show_new_project, newProjectItem)
        self.Bind(wx.EVT_MENU, self.open_project, openProjectItem)
        self.Bind(wx.EVT_MENU, self.view_log_pull, viewPullLogItem)

        #connect event main class
        DATA_RESULT(self, self.ParsingData)
        RANGE_RESULT(self, self.OnResult)
        PROGRESS_RESULT(self, self.OnProgress)
        ERROR_RESULT(self, self.OnError)
        HASH_RESULT(self, self.OnHashResult)
        PROJECT_RESULT(self, self.view_project)

        # connect even new_project class
        P_RESULT(self, self.load_project)

        #connect event Open_project class
        OPEN_RESULT(self, self.load_project)

    def __del__(self):
        pass

    def detect_device(self, event):
        self.txtview_deviceInfo.Clear()
        try:
            device = self.__adb.get_devices()
            self.__adb.set_target_by_id(0)
            bn = '"'+"'"+'" '
            # imei_cmd = "service call iphonesubinfo 1 | awk -F "+bn+"'{print $2}'"+"|"+ "sed '1 d' "+"|"+" tr -d "+"'.'"+"|" +" awk"+ " '{print}'"+" ORS="
            # test = "'adb shell service call iphonesubinfo 1 | awk -F' "+"'%s'"%bn+" ''{print $2}''"
            # tust = ["service call iphonesubinfo 1 | awk -F %s"%bn ," '{print $2}'"]
            device_manufaktur = self.__adb.shell_command("getprop | grep ro.product.manufacturer")
            and_version = self.__adb.shell_command("getprop | grep version.release")
            model = self.__adb.shell_command("getprop | grep model")
            name = self.__adb.shell_command("getprop | grep market.name")
            product = self.__adb.shell_command("getprop | grep product.name")
            brand = self.__adb.shell_command("getprop | grep brand")
            build_id = self.__adb.shell_command("getprop | grep build.id")
            serial = self.__adb.shell_command("getprop | grep ro.serial")
            operator = self.__adb.shell_command("getprop | grep operatorname")
            # IMEI = self.__adb.shell_command(tust)
            # print(tust)

            result = device_manufaktur+model+and_version+name+brand+build_id+serial+product+operator
            self.txtview_deviceInfo.WriteText(result)
        except:
            self.txtview_deviceInfo.WriteText("[!] No Device/emulator found")
        event.Skip()

    #fungsi-fungsi untuk mebuat project dan menampilkan project
    def view_project(self, event):
        self.textview_projectinfo.Clear()
        case_number = "Case Number :"+str(event.data[0])+"\n"
        examiner = "Examiner \t:"+event.data[1]+"\n"
        des = "Description \t:"+event.data[2]+"\n"
        note = "Note \t\t:"+event.data[3]
        self.textview_projectinfo.WriteText(case_number+examiner+des+note)
        event.Skip()

    def load_project(self, event):
        main = Main(self)
        main.runViewProject()
        event.Skip()

    def show_new_project(self, event):
        new_project = NewProjectFrame(wx.GetApp().TopWindow, self)
        new_project.Show()
        event.Skip()

    def open_project(self, event):
        open_project = OpenProjectDialog(wx.GetApp().TopWindow, self)
        open_project.Show()
        event.Skip()
    # fungsi-fungsi untuk mebuat project dan menampilkan project (end)

    def show_scan(self, event):
        scan = ScanFrame(wx.GetApp().TopWindow)
        scan.Show()
        event.Skip()

    def view_data_by_ext(self, event):
        self.listFile.DeleteAllItems()
        d=self.file_ext.GetStringSelection()
        order = self.short_by()
        Main(self).runSelectByExt(ext=d, order=order)
        event.Skip()

    def view_log_pull(self, event):
        pull = PullLogFrame(wx.GetApp().TopWindow)
        pull.Show()
        event.Skip()

    def short_by(self):
        key = self.shortBy_choice.GetCurrentSelection()
        if key == 0:
            key="file.size"
        elif key == 1:
            key = "file.date"
        return key

    def view_all_data(self, event):
        if not self.worker:
            order = self.short_by()
            self.listFile.DeleteAllItems()
            self.worker = Main(self).runSelectAll(order)
        event.Skip()

    def search_data(self, event):
        self.listFile.DeleteAllItems()
        text = self.txtctrl_search.GetValue()
        order = self.short_by()
        if text !=" " and text!="":
            Main(self).runSearchData(text, order)
        event.Skip()

    def item_right_click(self, event):
        self.PopupMenu(self.menu)
        event.Skip()

    def view_hash(self, event):
        row = self.listFile.GetFocusedItem()
        name = self.listFile.GetItem(itemIdx=row, col=1).GetText()
        loc = self.listFile.GetItem(itemIdx=row, col=0).GetText()
        file = loc.replace(":", "/")+name
        main = Main(self)
        main.runHashFile(file)
        event.Skip()

    def pull_file(self, event):
        count = self.listFile.GetSelectedItemCount()
        first = self.listFile.GetFirstSelected()
        files =[]
        i=0
        for i in range(count):
            rows = first+i
            bit = []
            i = i+1
            name = self.listFile.GetItem(itemIdx=rows, col=1).GetText()
            loc = self.listFile.GetItem(itemIdx=rows, col=0).GetText()
            file = loc.replace(":", "/") + name
            bit.append(file)
            bit.append(name)
            bit.append(loc)
            files.append(bit)
        pull = PullFrame(wx.GetApp().TopWindow, files)
        pull.Show()
        event.Skip()

    def hex_sum(self, event):
        row = self.listFile.GetFocusedItem()
        name = self.listFile.GetItem(itemIdx=row, col=1).GetText()
        loc = self.listFile.GetItem(itemIdx=row, col=0).GetText()
        file = loc.replace(":", "/") + name
        hex = HexFrame(wx.GetApp().TopWindow, file)
        hex.Show(True)
        event.Skip()

    def ParsingData(self, event):
        data = event.data
        index=self.listFile.InsertItem(sys.maxint, data[0])
        self.listFile.SetItem(index, 1, str(data[2]))
        self.listFile.SetItem(index, 2, str(data[3]))
        self.listFile.SetItem(index, 3, str(data[4]))
        self.listFile.SetItem(index, 4, str(data[5]))
        event.Skip()

    def OnResult(self, event):
        self.progress_bar.SetRange(0)
        self.progress_bar.SetRange(event.range)
        self.range = self.progress_bar.GetRange()

    def OnHashResult(self, event):
        dialog = wx.RichMessageDialog(self, "file: "+event.hash[2]+"\n\n"+"md5: "+event.hash[0]+"sha1: "+event.hash[1],"file hash")
        dialog.ShowModal()

    def OnProgress(self, event):
        r = float(self.range)
        v = float(event.val)
        p =v/r*100.0
        self.view_progress.SetLabel(str(round(p, 1))+"%")
        self.progress_bar.SetValue(event.val)

    def OnError(self, event):
        wx.MessageBox(str(event.error), 'Warning', wx.OK | wx.ICON_WARNING)

class MainApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = MainApp()
    app.MainLoop()