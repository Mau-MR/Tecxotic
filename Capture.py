import sys

import cv2
class Capture:
    def __init__(self, source=0):
        try:
            cap = cv2.VideoCapture(source)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap = cap
            ret, frame = self.cap.read()
            if not ret:
                raise Exception('Could not get frame of capture', source)
        except Exception as e:
            print("Error in Capture.py: ", str(e))
            sys.exit(0)
            return
        print("Sucessfully opened capture with id", source)


    #TODO: HANDLE THE ERROR WITH NO FRAME
    def get_frame(self):
        return self.cap.read()

    def release(self):
        self.cap.release()