import cv2

WIDTH = 640
HEIGHT = 480
MouseXY = list()


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
    cv2.setMouseCallback("video", getMouse)

    return capture


def getMouse(event, x, y, flags, param):

    global HEIGHT, WIDTH, MouseXY
    if event == cv2.EVENT_LBUTTONDOWN:  # 鼠标左键单击
        (xn, yn) = (x / WIDTH, y / HEIGHT)
        MouseXY.append(((x, y), (xn, yn)))
        print('Mouse(x,y):', '(' + str(x) + ',' + str(y) + ')', 'Normalize:',
              '(' + str(round(xn, 3)) + ',' + str(round(yn, 3)) + ')')
    # if event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 鼠标左键按下拖动


if __name__ == '__main__':
    cap = CaptureInit()

    while True:
        _, frame = cap.read()

        for point in MouseXY:
            cv2.circle(frame, point[0], 2, (255, 0, 0), -1)
            cv2.putText(frame, '(%d, %d)' % (point[0][0], point[0][1]),
                        (point[0][0], point[0][1] - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        0.7, (255, 0, 0), 2)
        cv2.imshow('video', frame)

        content = cv2.waitKey(1) & 0xff
        if content == 27:  # Esc
            print('exit!')
            break
        elif content == 8:  # BackSpace
            print('clear all!')
            MouseXY.clear()

    cv2.destroyAllWindows()
