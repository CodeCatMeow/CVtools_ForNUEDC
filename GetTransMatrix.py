"""
工具：通过在屏幕左键单击4个点，生成并获取仿射变换矩阵。
手动按下退格键进行重置/清零
"""

import cv2
import numpy as np

from lib import Video


WIDTH = 640
HEIGHT = 480
MouseXY = list()
M = np.array(
    [
        [1.06529793e00, 5.74352066e-01, -8.49011963e01],
        [7.56745491e-02, 2.15384700e00, 1.45244346e01],
        [1.31131787e-04, 2.22461078e-03, 1.00000000e00],
    ]
)

height_after = 200
width_after = 200
rec_X = 200
rec_Y = 200


def getMouse(event, x, y, flags, param):
    global HEIGHT, WIDTH, MouseXY
    if event == cv2.EVENT_LBUTTONDOWN:  # 鼠标左键单击
        (xn, yn) = (x / WIDTH, y / HEIGHT)
        MouseXY.append(((x, y), (xn, yn)))
        print(
            "Mouse(x,y):",
            "(" + str(x) + "," + str(y) + ")",
            "Normalize:",
            "(" + str(round(xn, 3)) + "," + str(round(yn, 3)) + ")",
        )


def orderPoints(pts):
    # 初始化矩形4个顶点的坐标
    rect = np.zeros((4, 2), dtype="float32")
    # 坐标点求和 x+y
    s = pts.sum(axis=1)
    # np.argmin(s) 返回最小值在s中的序号
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # diff就是后一个元素减去前一个元素  y-x
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    # 返回矩形有序的4个坐标点
    return rect


if __name__ == "__main__":
    cap = Video.CaptureInit()
    cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("video", getMouse)

    while True:
        _, frame = cap.read()

        if len(MouseXY) == 4:
            srcM = orderPoints(np.array(list(map(lambda x: x[0], MouseXY))))
            dstM = orderPoints(
                np.array(
                    [
                        (rec_X, rec_Y),
                        (rec_X, rec_Y + height_after),
                        (rec_X + width_after, rec_Y),
                        (rec_X + width_after, rec_Y + height_after),
                    ]
                )
            )
            M = cv2.getPerspectiveTransform(srcM, dstM)
            print(M)
            # MouseXY.clear()

        for point in MouseXY:
            cv2.circle(frame, point[0], 2, (255, 0, 0), -1)
            cv2.putText(
                frame,
                "(%d, %d)" % (point[0][0], point[0][1]),
                (point[0][0], point[0][1] - 5),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                0.7,
                (255, 0, 0),
                2,
            )

        if M is not None:
            dst = cv2.warpPerspective(frame, M, (512, 512))
            cv2.imshow("dst", dst)
        cv2.imshow("video", frame)

        content = cv2.waitKey(1) & 0xFF
        if content == 27:  # Esc
            print("exit!")
            break
        elif content == 8:  # BackSpace
            print("clear all!")
            MouseXY.clear()

    cv2.destroyAllWindows()
