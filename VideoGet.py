import cv2
from threading import *
class VideoGet:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, daemon=True).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True

    @staticmethod
    def putIterationsPerSec(frame, iterations_per_sec):
        cv2.rectangle(frame, (20, 30), (20+ 70, 30+40), (0, 255, 0), 2)
        cv2.putText(frame, f"{iterations_per_sec:.0f} iterations/sec",
                    (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        return frame