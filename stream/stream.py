import cv2
import socket
from stream.camera import Camera
from stream.receiver import Receiver

BUFSIZE: int = 8192
ENCODING: str = 'cp866'


class Stream:
    def __init__(self):
        self.camera = None
        self.receiver = None
        self.sock = None

    def start(self):
        exit = False

        while not exit:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.connect(('192.168.0.105', 5555))

                self.camera = Camera()

                for frame in self.camera.video():
                    try:
                        sock.sendall(frame)
                    except:
                        self.camera.cap.release()
                        exit = True
                        break
            except Exception as e:
                sock.close()
                continue

    def receive(self):
        self.receiver = Receiver()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('192.168.0.105', 5555))
        sock.listen()

        while True:
            vic, addr = sock.accept()

            for frame in self.receiver.video_recv(sock=vic):
                cv2.imshow("Stream", frame)

            sock.close()
            break
