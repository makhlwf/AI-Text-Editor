import wx
import config_manager


class SettingsDialog(wx.Dialog):
    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent, title="Settings")
        self.config = config_manager.get_config()

        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        # AI Provider
        provider_label = wx.StaticText(self.panel, label="AI Provider:")
        self.provider_combo = wx.ComboBox(
            self.panel,
            choices=["gemini", "ollama"],
            value=self.config.get("ai_provider", "gemini"),
            style=wx.CB_READONLY,
        )
        self.main_sizer.Add(provider_label, 0, wx.ALL, 5)
        self.main_sizer.Add(self.provider_combo, 0, wx.EXPAND | wx.ALL, 5)

        # Gemini Settings
        self.gemini_settings_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self.panel, label="Gemini Settings"), wx.VERTICAL
        )
        api_key_label = wx.StaticText(self.panel, label="Gemini API Key:")
        self.api_key_ctrl = wx.TextCtrl(
            self.panel, value=self.config.get("api_key", ""), style=wx.TE_PASSWORD
        )
        model_label = wx.StaticText(self.panel, label="Model:")
        self.model_ctrl = wx.TextCtrl(
            self.panel, value=self.config.get("model", "gemini-pro")
        )
        self.gemini_settings_sizer.Add(api_key_label, 0, wx.ALL, 5)
        self.gemini_settings_sizer.Add(self.api_key_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        self.gemini_settings_sizer.Add(model_label, 0, wx.ALL, 5)
        self.gemini_settings_sizer.Add(self.model_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.gemini_settings_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Ollama Settings
        self.ollama_settings_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self.panel, label="Ollama Settings"), wx.VERTICAL
        )
        ollama_model_label = wx.StaticText(self.panel, label="Model:")
        self.ollama_model_ctrl = wx.TextCtrl(
            self.panel, value=self.config.get("ollama_model", "gemma3")
        )
        self.ollama_settings_sizer.Add(ollama_model_label, 0, wx.ALL, 5)
        self.ollama_settings_sizer.Add(self.ollama_model_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.ollama_settings_sizer, 0, wx.EXPAND | wx.ALL, 5)

        shortcut_label = wx.StaticText(self.panel, label="Shortcut:")
        self.shortcut_ctrl = wx.TextCtrl(
            self.panel, value=self.config.get("shortcut", "ctrl+alt+x")
        )
        self.main_sizer.Add(shortcut_label, 0, wx.ALL, 5)
        self.main_sizer.Add(self.shortcut_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self.panel, wx.ID_OK, "OK")
        cancel_button = wx.Button(self.panel, wx.ID_CANCEL, "Cancel")
        btn_sizer.Add(ok_button, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_button, 0, wx.ALL, 5)
        self.main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.panel.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self)

        self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)
        self.Bind(wx.EVT_COMBOBOX, self.on_provider_changed, self.provider_combo)
        self.update_provider_settings()

    def on_provider_changed(self, event):
        self.update_provider_settings()

    def update_provider_settings(self):
        provider = self.provider_combo.GetValue()
        self.gemini_settings_sizer.GetStaticBox().Show(provider == "gemini")
        self.ollama_settings_sizer.GetStaticBox().Show(provider == "ollama")
        self.panel.Layout()
        self.main_sizer.Fit(self)

    def on_ok(self, event):
        self.config["ai_provider"] = self.provider_combo.GetValue()
        self.config["api_key"] = self.api_key_ctrl.GetValue()
        self.config["model"] = self.model_ctrl.GetValue()
        self.config["ollama_model"] = self.ollama_model_ctrl.GetValue()
        self.config["shortcut"] = self.shortcut_ctrl.GetValue()
        config_manager.save_config(self.config)
        self.EndModal(wx.ID_OK)
