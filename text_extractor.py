import win32gui
import win32api
import win32con
import win32process
import win32clipboard
import ctypes
import time
import uiautomation as auto


class TextExtractor:
    def __init__(self):
        # Set a short timeout for UIA searches to prevent freezing
        auto.SetGlobalSearchTimeout(0.25)

    def get_focused_text_and_hwnd(self):
        """
        Attempts to get text using 3 methods in order:
        1. UI Automation (Modern Apps: Chrome, VS Code)
        2. Legacy Win32 (Old Apps: Notepad, WinForms)
        3. Clipboard Simulation (Protected Apps: WhatsApp UWP, WinUI 3)
        """
        try:
            # --- Method 1: UI Automation (UWP/WPF/WinUI) ---
            text, hwnd = self._get_text_uia()
            if text:
                # We return dummy start/end (0,0) because UIA handles selection internally
                return text, hwnd, 0, 0

            # --- Method 2: Legacy Win32 API ---
            text, hwnd, start, end = self._get_text_win32()
            if text:
                return text, hwnd, start, end

            # --- Method 3: Clipboard Trick (The "Nuclear" Option) ---
            # Used for WhatsApp, modern Notepad, and apps that hide text.
            text, hwnd = self._get_text_clipboard_hack()
            if text:
                return text, hwnd, 0, 0

            return None, None, None, None

        except Exception as e:
            print(f"Error getting text: {e}")
            return None, None, None, None

    def set_text_in_control(self, hwnd, new_text, start_sel, end_sel):
        """
        Pasts text back. Handles both Legacy (WM_PASTE) and Modern (Ctrl+V) apps.
        """
        try:
            # 1. Backup Clipboard
            original_data = self._get_clipboard_data()

            # 2. Set new text to clipboard
            self._set_clipboard_data(new_text)

            # 3. Determine Paste Method
            # If we have valid selection indices from Win32, try legacy paste first
            legacy_success = False
            if hwnd and (start_sel != end_sel) and start_sel != 0:
                try:
                    win32api.SendMessage(hwnd, win32con.EM_SETSEL, start_sel, end_sel)
                    win32api.SendMessage(hwnd, win32con.WM_PASTE, 0, 0)
                    legacy_success = True
                except:
                    pass

            # 4. Universal Fallback: Simulate Ctrl+V
            # If legacy failed, or if we are in a UWP app (where indices are 0,0)
            if not legacy_success:
                # Bring window to front just in case
                if hwnd:
                    try:
                        if win32gui.GetForegroundWindow() != hwnd:
                            win32gui.SetForegroundWindow(hwnd)
                    except:
                        pass
                auto.SendKeys("{Ctrl}v")

            # 5. Restore Original Clipboard (after small delay for paste to consume)
            time.sleep(0.2)
            if original_data:
                self._set_clipboard_data(original_data)
            else:
                # Clear if it was empty
                try:
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.CloseClipboard()
                except:
                    pass

        except Exception as e:
            print(f"Error setting text: {e}")

    # --- INTERNAL HELPER METHODS ---

    def _get_text_uia(self):
        try:
            element = auto.GetFocusedControl()
            if not element:
                return None, None

            hwnd = element.NativeWindowHandle

            # Try TextPattern (Browsers, Word, Rich Text)
            txt_pattern = element.GetPattern(auto.PatternId.TextPattern)
            if txt_pattern:
                selection = txt_pattern.GetSelection()
                if selection:
                    return selection[0].GetText(-1), hwnd

            # Try ValuePattern (Simple Textboxes)
            val_pattern = element.GetPattern(auto.PatternId.ValuePattern)
            if val_pattern:
                return val_pattern.Value, hwnd

            return None, None
        except:
            return None, None

    def _get_text_win32(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)
            curr_thread = win32api.GetCurrentThreadId()

            # Attach thread to get focus info
            if curr_thread != thread_id:
                try:
                    win32process.AttachThreadInput(curr_thread, thread_id, True)
                    focused_hwnd = win32gui.GetFocus()
                    win32process.AttachThreadInput(curr_thread, thread_id, False)
                except:
                    focused_hwnd = None
            else:
                focused_hwnd = win32gui.GetFocus()

            if not focused_hwnd:
                return None, None, None, None

            # Get Selection
            sel = win32api.SendMessage(focused_hwnd, win32con.EM_GETSEL, 0, 0)
            start = sel & 0xFFFF
            end = sel >> 16

            # Get Text
            length = win32api.SendMessage(focused_hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
            if length > 0:
                buffer = ctypes.create_unicode_buffer(length + 1)
                win32api.SendMessage(
                    focused_hwnd, win32con.WM_GETTEXT, length + 1, buffer
                )
                text = buffer.value

                # Return only selected part if selection exists
                if start != end:
                    return text[start:end], focused_hwnd, start, end
                return text, focused_hwnd, 0, length

            return None, None, None, None
        except:
            return None, None, None, None

    def _get_text_clipboard_hack(self):
        try:
            hwnd = win32gui.GetForegroundWindow()

            # Backup
            old_data = self._get_clipboard_data()

            # Clear & Copy
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.CloseClipboard()
            except:
                return None, None

            auto.SendKeys("{Ctrl}c")

            # Wait for text to appear in clipboard
            found_text = None
            for _ in range(10):  # Max 0.2s wait
                time.sleep(0.02)
                try:
                    win32clipboard.OpenClipboard()
                    if win32clipboard.IsClipboardFormatAvailable(
                        win32con.CF_UNICODETEXT
                    ):
                        found_text = win32clipboard.GetClipboardData(
                            win32con.CF_UNICODETEXT
                        )
                        win32clipboard.CloseClipboard()
                        break
                    win32clipboard.CloseClipboard()
                except:
                    pass

            # Restore
            if old_data:
                self._set_clipboard_data(old_data)

            return found_text, hwnd
        except:
            return None, None

    def _get_clipboard_data(self):
        for _ in range(4):
            try:
                win32clipboard.OpenClipboard()
                data = None
                if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                    data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                return data
            except:
                time.sleep(0.02)
        return None

    def _set_clipboard_data(self, text):
        for _ in range(4):
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
                win32clipboard.CloseClipboard()
                return
            except:
                time.sleep(0.02)
