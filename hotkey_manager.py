import keyboard
import threading
import config_manager

class HotkeyManager(threading.Thread):
    def __init__(self, callback):
        super(HotkeyManager, self).__init__()
        self.callback = callback
        self.daemon = True
        self.config = config_manager.get_config()
        self._stop_event = threading.Event()

    def run(self):
        shortcut = self.config.get('shortcut', 'ctrl+alt+x')
        keyboard.add_hotkey(shortcut, self.callback)
        self._stop_event.wait()

    def stop(self):
        keyboard.remove_all_hotkeys()
        self._stop_event.set()
