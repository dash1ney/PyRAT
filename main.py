from handler import Handler
from server import Server
import threading

if __name__ == '__main__':
    server = Server('192.168.0.105', 4444)
    handler = Handler()

    server_thread = threading.Thread(target=server.start)
    select_thread = threading.Thread(target=handler.handle, args=[server])

    server_thread.start()
    select_thread.start()

    server_thread.join()
    select_thread.join()
