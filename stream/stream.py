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

    def start(self, srv_ip: str, srv_data_port: int):
        exit = False

        while not exit:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.connect((srv_ip, srv_data_port))

                self.camera = Camera()

                for frame in self.camera.video():
                    try:
                        sock.sendall(frame)
                    except Exception as e:
                        print(e)
                        self.camera.cap.release()
                        exit = True
                        break
            except:
                sock.close()
                continue

    def receive(self, local_ip: str, local_data_port: int):
        self.receiver = Receiver()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((local_ip, local_data_port))
        sock.listen(1)

        while True:
            vic, addr = sock.accept()

            for frame in self.receiver.video_recv(sock=vic):
                cv2.imshow("Stream", frame)

            sock.close()
            break
