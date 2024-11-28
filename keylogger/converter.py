from threading import Thread
from win32api import GetKeyboardLayout

language_codes = {'0x409': 'en', '0x419': 'ru'}
current_layout = None

special_keys = {
    'enter': '\n',
    'tab': '\t',
    'space': ' ',
    'shift': ''
}

en = "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~@#$^&|'
ru = "йцукенгшщзхъфывапролджэячсмитьбю.ё"'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё"№;:?/'
en_dict = dict(zip(map(ord, en), ru))
ru_dict = dict(zip(map(ord, ru), en))


def get_layout() -> str:
    global current_layout
    layout = language_codes[hex(GetKeyboardLayout() & 0xFFFF)]

    current_layout = layout
    return layout


layout_thread = Thread(target=get_layout)


class Converter:
    def __init__(self) -> None:
        self.initial_layout = get_layout()
        self.en_dict = en_dict
        self.ru_dict = ru_dict

    def convert(self, shift: bool, key: str) -> str:
        global layout_thread, special_keys

        if not layout_thread.is_alive():
            layout_thread = Thread(target=get_layout)
            layout_thread.start()
            layout_thread.join()

        if key in special_keys:
            return special_keys[key]

        if len(key) > 1:
            return f'[{key}]'

        if shift and key.isalpha():
            key = key.upper()

        if self.initial_layout != current_layout:
            if self.initial_layout == 'ru':
                key = key.translate(self.ru_dict)
            else:
                key = key.translate(self.en_dict)

        return key
