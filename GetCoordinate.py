"""
工具：点击屏幕显示坐标，命令行输出坐标和归一化坐标，按下退格键清零
"""

import cv2

from lib import Video

WIDTH = 640
HEIGHT = 480
MouseXY = list()


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
    # if event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 鼠标左键按下拖动


if __name__ == "__main__":
    cap = Video.CaptureInit()
    cv2.namedWindow("video", cv2.WINDOW_KEEPRATIO)
    cv2.setMouseCallback("video", getMouse)

    while True:
        _, frame = cap.read()

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
        cv2.imshow("video", frame)

        content = cv2.waitKey(1) & 0xFF
        if content == 27:  # Esc
            print("exit!")
            break
        elif content == 8:  # BackSpace
            print("clear all!")
            MouseXY.clear()

    cv2.destroyAllWindows()
