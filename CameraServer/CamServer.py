from time import sleep
import cv2
import  pyshine as ps #  pip3 install pyshine==0.0.9
from copy import deepcopy
from multiprocessing import Process
from threading import Thread
import sys
import psutil
from Constants import *
HTML="""
<html>
<body>
<center><img src="http://"""+IP_ADDRESS+""":"""+str(PORT_CAM1)+"""/stream.mjpg" autoplay playsinline ></center>
<center><img src="http://"""+IP_ADDRESS+""":"""+str(PORT_CAM2)+"""/stream.mjpg" autoplay playsinline ></center>
</body>
</html>
"""

def main1(IP,PORT, CAM):
    StreamProps = ps.StreamProps
    StreamProps.set_Page(StreamProps,HTML)
    address = (IP,PORT) # Enter your IP address
    StreamProps.set_Mode(StreamProps,'cv2') 
    capture = cv2.VideoCapture(CAM)
    #capture = cv2.VideoCapture(CAM,cv2.CAP_DSHOW)
    capture.set(cv2.CAP_PROP_BUFFERSIZE,1)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH,320)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
    capture.set(cv2.CAP_PROP_FPS,30)
    StreamProps.set_Capture(StreamProps,capture)
    StreamProps.set_Quality(StreamProps,90)
    server = None
    try:
        server = ps.Streamer(address,StreamProps)
        print('Server started at','http://'+address[0]+':'+str(address[1])+" from device:"+str(CAM))
        server.serve_forever()
    except Exception as e:
        capture.release()
        server.socket.close()
    #     print("==================ERROR: ",e)


t1 = None
t2 = None
server_started = False
def run():
    global server_started, t1, t2
    try:
        if server_started == False:
            t1 = Process(target=main1, args=(IP_ADDRESS, PORT_CAM1, 0,))
            t1.start()
            server_started = True
    except:
        pass
def restart():
    global server_started
    print(f"Restarting camera server...")
    t = psutil.Process(t1.pid)
    t.terminate()
    server_started = False
    run()   
    
    
if __name__=='__main__':
    from time import sleep
    run()
    sleep(15)
    restart()
