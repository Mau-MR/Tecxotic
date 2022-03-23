import cv2
import  pyshine as ps #  pip3 install pyshine==0.0.9
from multiprocessing import Process
from threading import Thread
import sys
HTML="""
<html>
<head>
<title>PyShine Live Streaming</title>
</head>

<body>
<center><h1> PyShine Live Streaming Multiple videos </h1></center>
<center><img src="http://192.168.50.22:9000/stream.mjpg" width='360' height='240' autoplay playsinline></center>
<br>
<center><img src="http://192.168.50.22:9001/stream.mjpg" width='360' height='240' autoplay playsinline></center>
</body>
</html>
"""
def main1():
    try:
        StreamProps = ps.StreamProps
        StreamProps.set_Page(StreamProps,HTML)
        address = ('192.168.50.22',9000) # Enter your IP address
        StreamProps.set_Mode(StreamProps,'cv2')
        capture = cv2.VideoCapture(0) # replace 0 (webcam id) with the path of your .mp4 video file
        capture.set(cv2.CAP_PROP_BUFFERSIZE,4)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH,320)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
        capture.set(cv2.CAP_PROP_FPS,30)
        StreamProps.set_Capture(StreamProps,capture)
        StreamProps.set_Quality(StreamProps,90)
        server = ps.Streamer(address,StreamProps)
        print('Server started at','http://'+address[0]+':'+str(address[1]))
        server.serve_forever()
        print('done')
        
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()

def main2():
    try:
        StreamProps = ps.StreamProps
        StreamProps.set_Page(StreamProps,HTML)
        address = ('192.168.50.22',9001) # Enter your IP address
        StreamProps.set_Mode(StreamProps,'cv2')
        capture = cv2.VideoCapture(1) # replace 1 (webcam id) with the path of your .mp4 for video file
        capture.set(cv2.CAP_PROP_BUFFERSIZE,4)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH,320)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
        capture.set(cv2.CAP_PROP_FPS,30)
        StreamProps.set_Capture(StreamProps,capture)
        StreamProps.set_Quality(StreamProps,90)
        server = ps.Streamer(address,StreamProps)
        print('Server started at','http://'+address[0]+':'+str(address[1]))
        server.serve_forever()
        print('done')
        
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()        
     
     
     
     


   
def test_main(tar):
    selector = {
        0 : main1,
        1 : main2
    }
    t = Thread(target=selector[tar])
    t.start()
    
    
    
if __name__=='__main__':
    p1 = Process(target=test_main, args=(0,))
    p1.start()
    p2 = Process(target=test_main, args=(1,))
    p2.start()