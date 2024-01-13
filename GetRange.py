"""
工具：使用带有滑块的窗口对阈值进行调整（以黑色提取为例）
"""

import cv2
import numpy as np

from lib import Video


def nothing(x):
    pass


if __name__ == "__main__":
    cap = Video.CaptureInit(PI_MODE=False)
    video = Video.TrackWindow("video", "value", 82, 255)
    # cv2.createTrackbar('value', 'video', 82, 255, nothing)
    while True:
        _, frame = cap.read()

        hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
        # m = cv2.getTrackbarPos('value', 'video')
        m = video.getValue()
        BLACK_RANGE = (np.array([0, 0, 0]), np.array([179, m, 255]))
        blackPart = cv2.inRange(hls, BLACK_RANGE[0], BLACK_RANGE[1])

        # cv2.imshow('video', blackPart)
        video.show(blackPart)

        content = cv2.waitKey(1) & 0xFF
        if content == 27:  # Esc
            print("exit!")
            break

    cv2.destroyAllWindows()
