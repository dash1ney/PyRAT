import pygetwindow as gw


class WindowChecker:
    def __init__(self):
        self.current_window = str(gw.getActiveWindow().title)
        self.previous_window = self.current_window

    def switch_window(self):
        return self.current_window != self.previous_window

    def check_window(self):
        self.previous_window = self.current_window
        self.current_window = str(gw.getActiveWindow().title)
