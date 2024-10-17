import cv2


def screenshot():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    for _ in range(30):
        cap.read()

    ret, frame = cap.read()
    cv2.imwrite("screen.png", frame)

    cap.release()
