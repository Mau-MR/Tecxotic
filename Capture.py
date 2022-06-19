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
        except Exception as e:
            print("Error in Capture.py: Unable to open capture", str(e))

    #TODO: HANDLE THE ERROR WITH NO FRAME
    def get_frame(self):
        return self.cap.read()

    def release(self):
        self.cap.release()