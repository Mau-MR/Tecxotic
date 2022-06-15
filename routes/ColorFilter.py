import cv2
import numpy as np

hr1H = 12
lr2H = 155
lrS = 50
lrV = 45
def processImage(capture, normalFrame):
    global hr1H, lr2H, lrS, lrV
    while True:
      ret, frame = capture.read()
      
      hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      low_red1 = np.array([0, lrS, lrV], np.uint8)
      high_red1 = np.array([hr1H, 255, 255], np.uint8)
      low_red2 =np.array([lr2H, lrS, lrV], np.uint8)
      high_red2=np.array([179, 255, 255], np.uint8)

      maskRed1 = cv2.inRange(hsv_frame, low_red1, high_red1)
      maskRed2 = cv2.inRange(hsv_frame, low_red2, high_red2)
      red_mask = cv2.add(maskRed1, maskRed2)
      
      contours,hierarchy = cv2.findContours(red_mask,1,cv2.CHAIN_APPROX_NONE)
      c = None
      if len(contours) > 0:
          c = max(contours,key=cv2.contourArea)
          M = cv2.moments(c)
          """
          if M["m00"] != 0:
              cx = int(M['m10']/M['m00'])
              cy = int(M['m01']/M['m00'])
              print("CX: " + str(cx) +  "CY: " + str(cy))
              if cx>= 120:
                  print("Turn Right")
              if cx < 120 and cx >40:
                  print("ON TRACK")
              if cx <= 40:
                  print("Turn Left")
              cv2.circle(frame,(cx,cy),5,(255,255,255),-1)
              """
      cv2.drawContours(frame,c,-1,(0,255,0),1)

      if ret:
        if normalFrame:
          (flag, encodedImage) = cv2.imencode(".jpg", frame)
        else:
          (flag, encodedImage) = cv2.imencode(".jpg", red_mask) 
        if not flag:
            continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
