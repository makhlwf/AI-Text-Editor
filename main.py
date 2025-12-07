import wx
import wx.adv
import ui.settings_dialog
import ui.options_dialog
import ui.style_dialog
import ui.instruction_dialog
import hotkey_manager
from text_extractor import TextExtractor
from ai_handler import AIHandler
import threading
import os
import sys
import gettext
import locale
import config_manager

# Global variables for gettext
LOCALE_DIR = None
_ = None


def set_translation_globals(language):
    global LOCALE_DIR, _

    # Set the locale based on config
    try:
        locale.setlocale(locale.LC_ALL, language + ".UTF-8")
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, language)
        except locale.Error:
            print(f"Warning: Could not set locale to {language}")

    # Setup gettext
    LOCALE_DIR = resource_path("locales")
    translator = gettext.translation("messages", LOCALE_DIR, languages=[language])
    translator.install()
    _ = translator.gettext


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Initial setup of translation globals
config = config_manager.get_config()
set_translation_globals(config.get("language", "en"))


TRAY_TOOLTIP = _("AI Text Editor")
TRAY_ICON = resource_path("icon.png")


class MainApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None)
        self.taskBarIcon = TaskBarIcon(self.frame)
        self.hotkey_manager = hotkey_manager.HotkeyManager(self.on_hotkey)
        self.hotkey_manager.start()
        self.text_extractor = TextExtractor()
        self.ai_handler = AIHandler(_)
        return True

    def on_hotkey(self):
        # This is called from the keyboard listener thread.
        # We use wx.CallAfter to schedule the UI logic to run on the main thread.
        wx.CallAfter(self.run_main_sequence)

    def run_main_sequence(self):
        # This method runs on the main GUI thread.
        text, hwnd, start_sel, end_sel = self.text_extractor.get_focused_text_and_hwnd()
        if not text or not hwnd:
            self.taskBarIcon.ShowBalloon(
                _("AI Text Editor"), _("No text found in the focused window.")
            )
            return

        options_dialog = ui.options_dialog.OptionsDialog(self.frame, _)
        if options_dialog.ShowModal() != wx.ID_OK:
            options_dialog.Destroy()
            return

        choice = options_dialog.get_choice()
        options_dialog.Destroy()

        params = {
            "text": text,
            "hwnd": hwnd,
            "choice": choice,
            "start_sel": start_sel,
            "end_sel": end_sel,
        }

        if choice == 1:  # Change Style
            style_dialog = ui.style_dialog.StyleDialog(self.frame, _)
            if style_dialog.ShowModal() != wx.ID_OK:
                style_dialog.Destroy()
                return
            params["style"] = style_dialog.get_style()
            style_dialog.Destroy()

        elif choice == 2:  # Direct Instruction
            instruction_dialog = ui.instruction_dialog.InstructionDialog(self.frame, _)
            if instruction_dialog.ShowModal() != wx.ID_OK:
                instruction_dialog.Destroy()
                return
            params["instruction"] = instruction_dialog.get_instruction()
            instruction_dialog.Destroy()

        # All user input is gathered, now start the worker thread.
        threading.Thread(target=self.process_text_in_background, args=(params,)).start()

    def process_text_in_background(self, params):
        try:
            wx.CallAfter(self.show_processing_message)
            new_text = None
            choice = params["choice"]
            text = params["text"]
            hwnd = params["hwnd"]
            start_sel = params["start_sel"]
            end_sel = params["end_sel"]

            print(f"--- Sending to AI ---\n{text}\n---------------------")

            if choice == 0:  # Fix Grammar
                new_text = self.ai_handler.fix_grammar(text)
            elif choice == 1:  # Change Style
                new_text = self.ai_handler.change_style(text, params["style"])
            elif choice == 2:  # Direct Instruction
                new_text = self.ai_handler.direct_instruction(
                    text, params["instruction"]
                )

            print(f"--- Received from AI ---\n{new_text}\n----------------------")

            if new_text:
                wx.CallAfter(
                    self.text_extractor.set_text_in_control,
                    hwnd,
                    new_text,
                    start_sel,
                    end_sel,
                )
        except Exception as e:
            print(f"Error in background thread: {e}")
        finally:
            wx.CallAfter(self.hide_processing_message)

    def show_processing_message(self):
        self.progress_dialog = wx.ProgressDialog(
            _("Processing..."),
            _("Please wait."),
            style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE,
        )
        self.progress_dialog.Pulse()

    def hide_processing_message(self):
        if hasattr(self, "progress_dialog") and self.progress_dialog:
            self.progress_dialog.Destroy()


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(wx.ID_ABOUT, _("Settings"))
        menu.AppendSeparator()
        menu.Append(wx.ID_EXIT, _("Exit"))
        self.Bind(wx.EVT_MENU, self.on_settings, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path, wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print("Tray icon left-clicked.")

    def on_settings(self, event):
        settings_dialog = ui.settings_dialog.SettingsDialog(self.frame, _)
        if settings_dialog.ShowModal() == wx.ID_OK:
            app = wx.GetApp()
            app.hotkey_manager.stop()
            app.hotkey_manager = hotkey_manager.HotkeyManager(app.on_hotkey)
            app.hotkey_manager.start()
            app.ai_handler = AIHandler(_)

            # Reload translations and update UI if language changed
            new_config = config_manager.get_config()
            if new_config["language"] != config["language"]:
                set_translation_globals(new_config["language"])
                # Re-create the main frame or update all translatable strings
                # For simplicity, we'll recreate the entire app for now.
                wx.MessageBox(
                    _(
                        "Language changed. Please restart the application for full effect."
                    ),
                    _("Restart Required"),
                    wx.OK | wx.ICON_INFORMATION,
                )
                self.frame.Close()
        settings_dialog.Destroy()

    def on_exit(self, event):
        wx.GetApp().hotkey_manager.stop()
        wx.CallAfter(self.Destroy)
        self.frame.Close()


if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()
