
import wx
from Data import Data
import ActiveProject
from Main import Main


class NewProjectFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(450, 330), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Project"), wx.VERTICAL)

        gSizer1 = wx.GridSizer(2, 2, 0, 0)

        self.m_statictext1 = wx.StaticText(self, wx.ID_ANY, u"project name", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_statictext1.Wrap(-1)
        gSizer1.Add(self.m_statictext1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.text_project_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.text_project_name, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"where", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        gSizer1.Add(self.m_staticText4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.dir_picker = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition,
                                           wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
        gSizer1.Add(self.dir_picker, 1, wx.EXPAND, 5)

        sbSizer2.Add(gSizer1, 1, wx.EXPAND, 5)

        bSizer1.Add(sbSizer2, 0, wx.EXPAND, 5)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Evidence"), wx.VERTICAL)

        gSizer2 = wx.GridSizer(4, 2, 0, 0)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"Case number", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        gSizer2.Add(self.m_staticText5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.text_case_number = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.text_case_number, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"Examiner name", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        gSizer2.Add(self.m_staticText6, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.text_examiner_name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.text_examiner_name, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        gSizer2.Add(self.m_staticText7, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.text_description = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.text_description, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"Notes", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)
        gSizer2.Add(self.m_staticText8, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.text_notes = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.text_notes, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer3.Add(gSizer2, 0, wx.EXPAND, 5)

        bSizer1.Add(sbSizer3, 0, wx.EXPAND, 5)

        self.btn_save_project = wx.Button(self, wx.ID_ANY, u"save", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.btn_save_project, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.btn_save_project.Bind(wx.EVT_BUTTON, self.save_project)

    def __del__(self):
        pass

    def save_project(self, event):
        project_name = self.text_project_name.GetValue()
        where = self.dir_picker.GetPath()
        case_number = self.text_case_number.GetValue()
        examiner = self.text_examiner_name.GetValue()
        description = self.text_description.GetValue()
        note = self.text_notes.GetValue()

        if project_name == "":
            wx.MessageBox("Project name canot empty", 'warning', wx.OK | wx.ICON_WARNING)
        elif where == "":
            wx.MessageBox("Where canot empty", 'warning', wx.OK | wx.ICON_WARNING)
        elif case_number =="":
            wx.MessageBox("Case number canot empty", 'warning', wx.OK | wx.ICON_WARNING)
        elif examiner =="":
            wx.MessageBox("Examiner name canot empty", 'warning', wx.OK | wx.ICON_WARNING)
        elif description == "":
            wx.MessageBox("Description canot empty", 'warning', wx.OK | wx.ICON_WARNING)
        elif note == "":
            wx.MessageBox("Note canot empty", 'warning', wx.OK | wx.ICON_WARNING)
        else:
            try:
                data = Data(where+"/"+project_name+".db")
                data.create_tables()

                data.insert_evidence(case_number,examiner,description, note)
                ActiveProject.init(where+"/"+project_name+".db")
                Main(self).runViewProject()
            except Exception as e:
                print e

            finally:
                self.Destroy()

        event.Skip()


