import cv2

WIDTH = 640
HEIGHT = 480
point = [[0, 0], [0, 0]]
frame = cv2.VideoCapture()


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

    global HEIGHT, WIDTH, point
    if event == cv2.EVENT_LBUTTONDOWN:  # 鼠标左键单击
        point[0][0], point[0][1] = x, y
        # print(point[0])
    elif event == cv2.EVENT_MOUSEMOVE and (
            flags & cv2.EVENT_FLAG_LBUTTON):  # 鼠标左键按下拖动
        point[1][0], point[1][1] = x, y
        # print(point[1])
    elif event == cv2.EVENT_LBUTTONUP:
        for p in point:
            if p[0] > WIDTH:
                p[0] = WIDTH
            if p[1] > HEIGHT:
                p[1] = HEIGHT
        print('ROI:  (x1, y1) = (%d, %d), (x2, y2) = (%d, %d)' %
              (point[0][0], point[0][1], point[1][0], point[1][1]))
        print('Normalize:  (x1, y1) = (%.3f, %.3f), (x2, y2) = (%.3f, %.3f)' %
              (point[0][0] / WIDTH, point[0][1] / HEIGHT, point[1][0] / WIDTH,
               point[1][1] / HEIGHT))
        print()


cap = CaptureInit()

while True:
    _, frame = cap.read()

    cv2.rectangle(frame, tuple(point[0]), tuple(point[1]), (255, 0, 0), 2)
    cv2.imshow('video', frame)

    content = cv2.waitKey(1) & 0xff
    if content == 27:  # Esc
        print('exit!')
        break

cv2.destroyAllWindows()
