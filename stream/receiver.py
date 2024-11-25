from socket import socket

import cv2, pickle, struct

BUFSIZE: int = 8192
ENCODING: str = 'cp866'


class Receiver:
    def __init__(self):
        pass

    @staticmethod
    def video_recv(sock: socket):
        data = b""
        payload_size = struct.calcsize("L")

        while True:
            while len(data) < payload_size:
                data += sock.recv(BUFSIZE)

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += sock.recv(BUFSIZE)

            dump = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(dump)

            yield frame

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        cv2.destroyAllWindows()
