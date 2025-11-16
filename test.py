import wx
import main


class TestFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Test Target", size=(300, 200))
        self.panel = wx.Panel(self)
        self.text_ctrl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text_ctrl, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        self.text_ctrl.SetValue("This is some test text.")


class TestApp(wx.App):
    def OnInit(self):
        self.main_app = main.MainApp()
        self.main_app.OnInit()

        self.test_frame = TestFrame()
        self.test_frame.Show()

        # Give the frame time to appear and get focus
        wx.CallLater(1000, self.run_test)
        return True

    def run_test(self):
        print("--- Running Test ---")
        try:
            # 1. Simulate hotkey press and call process_text directly
            print("Simulating hotkey press...")
            text_to_process = self.test_frame.text_ctrl.GetValue()
            # For this test, we will simulate the "Fix Grammar" option (choice=0)
            self.main_app.process_text(text_to_process, 0)

            # 2. Check the text in the control after the operation
            wx.CallLater(5000, self.check_result)  # Wait for AI response

        except Exception as e:
            print(f"An error occurred during the test: {e}")
            self.test_frame.Close()
            wx.GetApp().Exit()

    def check_result(self):
        print("--- Checking Result ---")
        final_text = self.test_frame.text_ctrl.GetValue()
        print(f"Final text in control: {final_text}")
        self.test_frame.Close()
        self.main_app.taskBarIcon.on_exit(None)
        wx.GetApp().Exit()


if __name__ == "__main__":
    print("Please ensure you have set your Gemini API key in the settings.")
    app = TestApp()
    app.MainLoop()
