import wx


class StyleDialog(wx.Dialog):
    def __init__(self, parent, _):
        self._ = _
        super(StyleDialog, self).__init__(parent, title=self._("Change Style"))
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.radio_box = wx.RadioBox(
            self.panel,
            label=self._("Choose a style"),
            choices=[
                self._("Formal"),
                self._("Casual"),
                self._("Professional"),
                self._("Creative"),
                self._("Polite"),
                self._("Funny"),
                self._("Social post"),
            ],
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS,
        )

        self.main_sizer.Add(self.radio_box, 0, wx.ALL, 10)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self.panel, wx.ID_OK, self._("OK"))
        cancel_button = wx.Button(self.panel, wx.ID_CANCEL, self._("Cancel"))
        btn_sizer.Add(ok_button, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_button, 0, wx.ALL, 5)
        self.main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.panel.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self)

    def get_style(self):
        return self.radio_box.GetStringSelection()
