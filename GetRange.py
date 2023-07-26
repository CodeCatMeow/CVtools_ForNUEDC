import cv2
import numpy as np


def nothing(x):
    pass


def CaptureInit(width: int = 640,
                height: int = 480,
                PI_MODE=True) -> cv2.VideoCapture:
    "摄像头配置和打开"
    if PI_MODE:
        capture = cv2.VideoCapture(0)
    else:
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    capture.set(cv2.CAP_PROP_FOURCC, fourcc)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    cv2.namedWindow('video', cv2.WINDOW_KEEPRATIO)
    # cv2.setMouseCallback("video", getMouse)

    return capture


if __name__ == '__main__':
    cap = CaptureInit()
    cv2.createTrackbar('value', 'video', 82, 255, nothing)
    while True:
        _, frame = cap.read()
        
        hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
        m = cv2.getTrackbarPos('value', 'video')
        BLACK_RANGE = (np.array([0, 0, 0]), np.array([179, m, 255]))
        blackPart = cv2.inRange(hls, BLACK_RANGE[0],
                                BLACK_RANGE[1])
        
        cv2.imshow('video',blackPart)

        content = cv2.waitKey(1) & 0xff
        if content == 27:  # Esc
            print('exit!')
            break
    
    cv2.destroyAllWindows()