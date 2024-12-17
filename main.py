from threading import Thread
import cv2
from mtcnn import MTCNN
from VideoGet import VideoGet
from VideoShow import VideoShow
from CountsperSec import CountsPerSec
import queue
detector = MTCNN()

def threadVideoGet(source=0):
    video_getter = VideoGet(source).start()
    cps = CountsPerSec().start()
    while True:
        if cv2.waitKey(1) == ord("q") or video_getter.stopped:
            video_getter.stop()
            break
        frame = video_getter.frame
        frame = VideoGet.putIterationsPerSec(frame, cps.countsPerSec())
        cv2.imshow("Video", frame)
        cps.increment()

def faceDetectionThread(input_queue, output_queue):
    while True:
        if not input_queue.empty():
            frame = input_queue.get()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = detector.detect_faces(rgb_frame)
            for face in faces:
                x, y, width, height = face['box']
                # print(x,y,"in")
                cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 255), 2)
            output_queue.put(frame)

def threadBoth(source=0):
    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()
    input_queue = queue.Queue()
    output_queue = queue.Queue()
    detection_thread = Thread(target=faceDetectionThread,daemon=True, args=(input_queue, output_queue))
    detection_thread.start()
    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break
        frame = video_getter.frame
        input_queue.put(frame)
        if not output_queue.empty():
            frame = output_queue.get()
        frame = VideoGet.putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()
threadBoth()