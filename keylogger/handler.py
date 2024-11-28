import keyboard


class Handler:
    def __init__(self) -> None:
        self.shift = False
        self.key = None

    def shift_handler(self, event: keyboard.KeyboardEvent) -> None:
        if event.name == 'shift':
            if event.event_type == keyboard.KEY_DOWN:
                self.shift = True
            else:
                self.shift = False

    def main_handler(self, event: keyboard.KeyboardEvent) -> None:
        if event.event_type == keyboard.KEY_DOWN:
            self.key = event.name
