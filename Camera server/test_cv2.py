import cv2 as cv

vcap = cv.VideoCapture('http://10.49.182.166:9000/stream.mjpg')

def run():
    while(True):
        # Capture frame-by-frame
        ret, frame = vcap.read()
        #print cap.isOpened(), ret
        if frame is not None:
            # Display the resulting frame
            cv.imshow('frame',frame)
            # Press q to close the video windows before it ends if you want
            if cv.waitKey(22) & 0xFF == ord('q'):
                break
        else:
            print ("Frame is None")
            break

    # When everything done, release the capture
    vcap.release()
    cv.destroyAllWindows()
    print ("Video stop")



if __name__=='__main__':
    while True:
        try:
            run()
        except:
            pass