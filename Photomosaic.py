import cv2

images=[]

def photomosaic(capture):
    _, frame = capture.get_frame()
    images.append(frame)
    return frame


def create_photomosaic():
    global images
    if len(images) < 8:
        return Exception("Not enough images")
    for index, val in enumerate(images): #
        images[index] = cv2.resize(val, (200,200))
    stack1=cv2.hconcat([images[0],images[1],images[2],images[3]])
    stack2=cv2.hconcat([images[4],images[5],images[6],images[7]])
    stack3=cv2.vconcat([stack1,stack2])
    return stack3
