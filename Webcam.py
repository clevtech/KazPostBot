import cv2


class Webcam:
    def __init__(self, width=300, height=150):
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(3, width)
        self.video_capture.set(4, height)
        res, frame = self.video_capture.read()
        if not res:
            raise BufferError('Camera connection problem')
        self.width = frame.shape[1]
        self.height = frame.shape[0]

    def get_current_frame(self):
        return self.video_capture.read()[1][self.height / 2 - 9 : self.height / 2 + 8, 15 : self.width - 60]

