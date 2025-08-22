import wx
import config_manager

class SettingsDialog(wx.Dialog):
    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent, title="Settings")
        self.config = config_manager.get_config()

        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        api_key_label = wx.StaticText(self.panel, label="Gemini API Key:")
        self.api_key_ctrl = wx.TextCtrl(self.panel, value=self.config.get('api_key', ''), style=wx.TE_PASSWORD)
        shortcut_label = wx.StaticText(self.panel, label="Shortcut:")
        self.shortcut_ctrl = wx.TextCtrl(self.panel, value=self.config.get('shortcut', 'ctrl+alt+x'))

        self.main_sizer.Add(api_key_label, 0, wx.ALL, 5)
        self.main_sizer.Add(self.api_key_ctrl, 0, wx.EXPAND|wx.ALL, 5)
        self.main_sizer.Add(shortcut_label, 0, wx.ALL, 5)
        self.main_sizer.Add(self.shortcut_ctrl, 0, wx.EXPAND|wx.ALL, 5)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self.panel, wx.ID_OK, "OK")
        cancel_button = wx.Button(self.panel, wx.ID_CANCEL, "Cancel")
        btn_sizer.Add(ok_button, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_button, 0, wx.ALL, 5)
        self.main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.panel.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self)

        self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)

    def on_ok(self, event):
        self.config['api_key'] = self.api_key_ctrl.GetValue()
        self.config['shortcut'] = self.shortcut_ctrl.GetValue()
        config_manager.save_config(self.config)
        self.EndModal(wx.ID_OK)
