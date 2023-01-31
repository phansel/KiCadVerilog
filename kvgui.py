#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.4 on Thu Jan 19 15:20:46 2023
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
import os.path
try:
    from . import KiCadVerilog
except:
    import KiCadVerilog

import webbrowser

def launch():
    kvapp = KVApp(0)
    kvapp.MainLoop()
# end wxGlade


class KVUI(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: KVUI.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((602, 405))
        self.SetTitle("KiCad To Verilog Generator")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_3, 0, wx.EXPAND, 0)

        label_1 = wx.StaticText(self, wx.ID_ANY, "Input Netlist File:")
        label_1.SetMinSize((102, 16))
        sizer_3.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.netlist_file_field = wx.TextCtrl(self, wx.ID_ANY, "")
        sizer_3.Add(self.netlist_file_field, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.netlist_browse = wx.Button(self, wx.ID_ANY, "Browse...")
        sizer_3.Add(self.netlist_browse, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_4, 0, wx.EXPAND, 0)

        label_2 = wx.StaticText(self, wx.ID_ANY, "Output Verilog File:")
        label_2.SetMinSize((102, 16))
        sizer_4.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.verilog_file_field = wx.TextCtrl(self, wx.ID_ANY, "")
        sizer_4.Add(self.verilog_file_field, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.verilog_browse = wx.Button(self, wx.ID_ANY, "Browse...")
        sizer_4.Add(self.verilog_browse, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        sizer_5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Results:"), wx.VERTICAL)
        sizer_1.Add(sizer_5, 1, wx.ALL | wx.EXPAND, 7)

        self.results_text = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_MULTILINE | wx.TE_READONLY)
        sizer_5.Add(self.results_text, 1, wx.EXPAND, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALL, 4)

        self.button_GENERATE = wx.Button(self, wx.ID_ANY, "Generate Verilog")
        sizer_2.Add(self.button_GENERATE, 0, wx.ALL, 10)

        self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
        sizer_2.AddButton(self.button_CANCEL)

        self.button_HELP = wx.Button(self, wx.ID_HELP, "")
        sizer_2.AddButton(self.button_HELP)

        sizer_2.Realize()

        self.SetSizer(sizer_1)

        self.SetEscapeId(self.button_CANCEL.GetId())

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.on_netlist_browse, self.netlist_browse)
        self.Bind(wx.EVT_BUTTON, self.on_verilog_browse, self.verilog_browse)
        self.Bind(wx.EVT_BUTTON, self.on_generate, self.button_GENERATE)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.button_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.on_help, self.button_HELP)
        # end wxGlade

    def on_netlist_browse(self, event):  # wxGlade: KVUI.<event_handler>
        with wx.FileDialog(self, "Select Netlist File", wildcard="Netlist files (*.net)|*.net",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() != wx.ID_CANCEL:
                pathname = fileDialog.GetPath()
                self.netlist_file_field.SetValue(pathname)

    def on_verilog_browse(self, event):  # wxGlade: KVUI.<event_handler>
        with wx.FileDialog(self, "Select Verilog File", wildcard="Verilog files (*.v)|*.v",
                       style=wx.FD_SAVE) as fileDialog:

            if fileDialog.ShowModal() != wx.ID_CANCEL:
                pathname = fileDialog.GetPath()
                self.verilog_file_field.SetValue(pathname)

    def on_generate(self, event):  # wxGlade: KVUI.<event_handler>
        if os.path.exists(self.verilog_file_field.GetValue()):
            result = wx.MessageBox('The Verilog output file already exists. Do you want to overwrite it?', \
                'Confirm Overwrite', \
                wx.YES_NO | wx.ICON_QUESTION)
        else:
            result = wx.YES

        if result == wx.YES:
            with wx.BusyCursor():
                self.results_text.SetValue('')
                try:
                    log = KiCadVerilog.main(['-i', self.netlist_file_field.GetValue(), '-o', self.verilog_file_field.GetValue()])
                except Exception as e:
                    log = str(e)

                for message in log:
                    self.results_text.write(message + '\n')
                self.button_CANCEL.SetLabel('Close')

    def on_cancel(self, event):  # wxGlade: KVUI.<event_handler>
        event.Skip()

    def on_help(self, event):  # wxGlade: KVUI.<event_handler>
        webbrowser.open('https://github.com/galacticstudios/KiCadVerilog/blob/main/README.md')

# end of class KVUI

class KVApp(wx.App):
    def OnInit(self):
        self.dialog = KVUI(None, wx.ID_ANY, "")
        self.SetTopWindow(self.dialog)
        self.dialog.ShowModal()
        self.dialog.Destroy()
        return True

# end of class KVApp

if __name__ == "__main__":
    kvapp = KVApp(0)
    kvapp.MainLoop()
