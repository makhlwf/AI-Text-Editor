import wx

class OptionsDialog(wx.Dialog):
    def __init__(self, parent):
        super(OptionsDialog, self).__init__(parent, title="AI Text Editor")
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.radio_box = wx.RadioBox(
            self.panel, 
            label="Choose an option", 
            choices=["Fix Grammar", "Change Style", "Direct Instruction"],
            majorDimension=1, 
            style=wx.RA_SPECIFY_COLS
        )

        self.main_sizer.Add(self.radio_box, 0, wx.ALL, 10)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self.panel, wx.ID_OK, "OK")
        cancel_button = wx.Button(self.panel, wx.ID_CANCEL, "Cancel")
        btn_sizer.Add(ok_button, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_button, 0, wx.ALL, 5)
        self.main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.panel.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self)

    def get_choice(self):
        return self.radio_box.GetSelection()
