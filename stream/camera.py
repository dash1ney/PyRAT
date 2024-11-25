import cv2, pickle, struct


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def photo(self):
        ret, frame = self.cap.read()

        if not ret:
            return None

        dump = pickle.dumps(frame)
        frame = struct.pack("L", len(dump)) + dump

        return frame

    def video(self):
        while self.cap.isOpened():
            frame = self.photo()

            if not frame:
                break

            yield frame

        self.cap.release()
