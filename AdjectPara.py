"""
工具：使用带有滑块的窗口对相机参数进行实时调整
"""

import cv2
import numpy as np

from lib import Video


# def nothing(x):
#     pass


def CaptureInit(
    width: int = 640, height: int = 480, PI_MODE=True
) -> cv2.VideoCapture:
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

    # cv2.namedWindow('video', cv2.WINDOW_KEEPRATIO)
    # cv2.setMouseCallback("video", getMouse)

    return capture


if __name__ == "__main__":
    cap = CaptureInit(PI_MODE=False)
    video = Video.TrackWindow("video", "value", 50, 100)
    Video.printVideoPara(cap)

    while True:
        contrast = video.getValue()

        if contrast != cap.get(cv2.CAP_PROP_CONTRAST):
            # print(cap.isOpened(), cap.get(cv2.CAP_PROP_CONTRAST), contrast)
            cap.set(cv2.CAP_PROP_CONTRAST, contrast)

        _, frame = cap.read()

        video.show(frame)

        content = cv2.waitKey(1) & 0xFF
        if content == 27:  # Esc
            print("exit!")
            break
    cap.release()
    cv2.destroyAllWindows()
