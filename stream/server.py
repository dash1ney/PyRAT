import socket, cv2, pickle, struct, imutils

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_address = ('127.0.0.1', 5555)
server.bind(socket_address)
server.listen()

print("Listening at:", socket_address)

while True:
    client, addr = server.accept()
    print('Got connection from:', addr)

    if client:
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()

            dump = pickle.dumps(frame)
            client.sendall(struct.pack("Q", len(dump)) + dump)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
