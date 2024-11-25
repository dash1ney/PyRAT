import threading
import time

from handler import Handler
from server import Server

BUFSIZE: int = 8192
ENCODING: str = 'cp866'

if __name__ == '__main__':
    server = Server('192.168.0.105', 4444)
    handler = Handler()

    server_thread = threading.Thread(target=server.start)
    select_thread = threading.Thread(target=handler.handle, args=[server])

    server_thread.start()
    time.sleep(1)
    select_thread.start()

    server_thread.join()
    select_thread.join()
