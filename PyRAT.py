from handler import Handler
from server import Server
from cfg import cfg
import threading

if __name__ == '__main__':
    server = Server(cfg.local_ip, cfg.local_port)
    handler = Handler()

    server_thread = threading.Thread(target=server.start)
    select_thread = threading.Thread(target=handler.handle, args=[server])

    server_thread.start()
    select_thread.start()

    server_thread.join()
    select_thread.join()
