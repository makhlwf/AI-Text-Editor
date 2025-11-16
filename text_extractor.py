import win32gui
import win32api
import win32con
import win32process
import ctypes
import win32clipboard
import time


class TextExtractor:
    def get_focused_text_and_hwnd(self):
        try:
            foreground_window_handle = win32gui.GetForegroundWindow()
            result = win32process.GetWindowThreadProcessId(foreground_window_handle)
            if isinstance(result, (tuple, list)):
                foreground_thread_id = result[0]
            else:
                foreground_thread_id = result
            current_thread_id = win32api.GetCurrentThreadId()

            win32process.AttachThreadInput(
                current_thread_id, foreground_thread_id, True
            )
            focused_ctrl_hwnd = win32gui.GetFocus()
            win32process.AttachThreadInput(
                current_thread_id, foreground_thread_id, False
            )

            if not focused_ctrl_hwnd:
                return None, None, None, None

            # Get selection info
            sel = win32api.SendMessage(focused_ctrl_hwnd, win32con.EM_GETSEL, 0, 0)
            start_sel = sel & 0xFFFF
            end_sel = sel >> 16

            text = None
            if start_sel != end_sel:  # Text is selected
                buff_len = win32api.SendMessage(
                    focused_ctrl_hwnd, win32con.WM_GETTEXTLENGTH, 0, 0
                )
                if buff_len > 0:
                    buffer = ctypes.create_unicode_buffer(buff_len + 1)
                    win32api.SendMessage(
                        focused_ctrl_hwnd, win32con.WM_GETTEXT, buff_len + 1, buffer
                    )
                    text = buffer.value[start_sel:end_sel]
                return text, focused_ctrl_hwnd, start_sel, end_sel
            else:  # No text selected, get full text
                full_text = self.get_full_text(focused_ctrl_hwnd)
                if full_text:
                    return full_text, focused_ctrl_hwnd, 0, len(full_text)
                return None, None, None, None

        except Exception as e:
            print(f"Error getting text: {e}")
            return None, None, None, None

    def get_selected_text(self, hwnd):
        buff_len = win32api.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
        if buff_len > 0:
            sel = win32api.SendMessage(hwnd, win32con.EM_GETSEL, 0, 0)
            start = sel & 0xFFFF
            end = sel >> 16
            if start != end:
                buffer = ctypes.create_unicode_buffer(buff_len + 1)
                win32api.SendMessage(hwnd, win32con.WM_GETTEXT, buff_len + 1, buffer)
                return buffer.value[start:end]
        return None

    def get_full_text(self, hwnd):
        buff_len = win32api.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
        if buff_len > 0:
            buffer = ctypes.create_unicode_buffer(buff_len + 1)
            win32api.SendMessage(hwnd, win32con.WM_GETTEXT, buff_len + 1, buffer)
            return buffer.value
        return None

    def set_text_in_control(self, hwnd, new_text, start_sel, end_sel):
        try:
            if not hwnd:
                return

            # 1. Save original clipboard content
            original_clipboard_content = None
            try:
                win32clipboard.OpenClipboard()
                if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                    original_clipboard_content = win32clipboard.GetClipboardData(
                        win32con.CF_UNICODETEXT
                    )
            finally:
                win32clipboard.CloseClipboard()

            # 2. Set new text to clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, new_text)
            win32clipboard.CloseClipboard()

            # 3. Explicitly set selection before pasting
            win32api.SendMessage(hwnd, win32con.EM_SETSEL, start_sel, end_sel)

            # 4. Send Paste command
            win32api.SendMessage(hwnd, win32con.WM_PASTE, 0, 0)

            # 5. Restore original clipboard content (with a small delay)
            time.sleep(0.1)
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                if original_clipboard_content is not None:
                    win32clipboard.SetClipboardData(
                        win32con.CF_UNICODETEXT, original_clipboard_content
                    )
            finally:
                win32clipboard.CloseClipboard()

        except Exception as e:
            print(f"Error setting text: {e}")
