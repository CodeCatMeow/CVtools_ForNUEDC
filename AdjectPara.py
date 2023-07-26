
import cv2
import numpy as np

from lib import Video


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
    # fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    # capture.set(cv2.CAP_PROP_FOURCC, fourcc)
    # capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    cv2.namedWindow('video', cv2.WINDOW_KEEPRATIO)
    # cv2.setMouseCallback("video", getMouse)

    return capture


if __name__ == '__main__':
    cap = CaptureInit(PI_MODE=False)
    Video.printVideoPara(cap)

    cv2.createTrackbar('value', 'video', 50, 100, nothing)
    while True:
        contrast = cv2.getTrackbarPos('value', 'video')

        if contrast != cap.get(cv2.CAP_PROP_CONTRAST):
            print(cap.isOpened(), cap.get(cv2.CAP_PROP_CONTRAST), contrast)
            cap.set(cv2.CAP_PROP_CONTRAST, contrast)

        _, frame = cap.read()
        
        cv2.imshow('video', frame)
        # cv2.imshow('frame', frame)

        content = cv2.waitKey(1) & 0xff
        if content == 27:  # Esc
            print('exit!')
            break
    cap.release()
    cv2.destroyAllWindows()