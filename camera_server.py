import cv2
import  pyshine as ps #  pip3 install pyshine==0.0.9
from copy import deepcopy
from multiprocessing import Process
from threading import Thread
HTML="""
<html>
<body>
<center><img src="http://192.168.50.22:9000/stream.mjpg" width='1280' height='960' autoplay playsinline></center>
<center><img src="http://192.168.50.22:9001/stream.mjpg" width='1280' height='960' autoplay playsinline></center>
</body>
</html>
"""

def main1(IP,PORT, CAM):
    StreamProps = ps.StreamProps
    StreamProps.set_Page(StreamProps,HTML)
    address = (IP,PORT) # Enter your IP address
    StreamProps.set_Mode(StreamProps,'cv2')
    capture = cv2.VideoCapture(CAM,cv2.CAP_DSHOW)
    capture.set(cv2.CAP_PROP_BUFFERSIZE,4)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,960)
    capture.set(cv2.CAP_PROP_FPS,30)
    StreamProps.set_Capture(StreamProps,capture)
    StreamProps.set_Quality(StreamProps,90)
    # try:
    server = ps.Streamer(address,StreamProps)
    print('Server started at','http://'+address[0]+':'+str(address[1])+" from device:"+str(CAM))
    server.serve_forever()
    # except Exception as e:
    #     capture.release()
    #     server.socket.close()
    #     print("==================ERROR: ",e)



    
    
if __name__=='__main__':
    t1 = Process(target=main1, args=('192.168.50.22', 9000, 0,))
    t1.start()
    t2 = Process(target=main1, args=('192.168.50.22', 9001, 1,))
    t2.start()
    t2 = Process(target=main1, args=('192.168.50.22', 9002, 2,))
    t2.start()


    # main(capture)
    # showWebcam(capture)
