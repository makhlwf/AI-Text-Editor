import wx

class InstructionDialog(wx.Dialog):
    def __init__(self, parent):
        super(InstructionDialog, self).__init__(parent, title="Direct Instruction")
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        instruction_label = wx.StaticText(self.panel, label="Enter your instruction:")
        self.instruction_ctrl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)

        self.main_sizer.Add(instruction_label, 0, wx.ALL, 5)
        self.main_sizer.Add(self.instruction_ctrl, 1, wx.EXPAND|wx.ALL, 5)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self.panel, wx.ID_OK, "OK")
        cancel_button = wx.Button(self.panel, wx.ID_CANCEL, "Cancel")
        btn_sizer.Add(ok_button, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_button, 0, wx.ALL, 5)
        self.main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.panel.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self)

    def get_instruction(self):
        return self.instruction_ctrl.GetValue()
