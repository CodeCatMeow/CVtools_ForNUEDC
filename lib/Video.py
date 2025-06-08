"""
颜色分割阈值、视频调试
"""

import numpy as np
import cv2


# 颜色分割的阈值
class ColorSegHSV:
    "HSV模式下常用颜色分割参数"
    # 七色阈值分割
    RED_RANGE_1 = (np.array([0, 43, 46]), np.array([10, 255, 255]))
    ORANGE_RANGE = (np.array([11, 43, 46]), np.array([25, 255, 255]))
    YELLOW_RANGE = (np.array([26, 43, 46]), np.array([34, 255, 255]))
    GREEN_RANGE = (np.array([35, 43, 46]), np.array([77, 255, 255]))
    CYAN_RANGE = (np.array([78, 43, 46]), np.array([99, 255, 255]))
    BLUE_RANGE = (np.array([100, 43, 46]), np.array([124, 255, 255]))
    PURPLE_RANGE = (np.array([125, 43, 46]), np.array([155, 255, 255]))
    RED_RANGE_2 = (np.array([156, 43, 46]), np.array([180, 255, 255]))

    # RGB三通道分割（推荐直接使用RGB模式）
    R_RANGE_1 = (np.array([151, 43, 46]), np.array([180, 255, 255]))
    R_RANGE_2 = (np.array([0, 43, 46]), np.array([30, 255, 255]))
    G_RANGE = (np.array([31, 43, 46]), np.array([90, 255, 255]))
    B_RANGE = (np.array([91, 43, 46]), np.array([150, 255, 255]))


class ColorSegHLS:
    "HLS空间分割"
    BLACK_RANGE = (np.array([0, 0, 0]), np.array([179, 90, 255]))  # 黑色提取


def printVideoPara(capture: cv2.VideoCapture):
    "返回摄像头各类参数"
    print("帧宽:", capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("帧高:", capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("解码方式:", capture.get(cv2.CAP_PROP_FOURCC))
    print("帧率:", capture.get(cv2.CAP_PROP_FPS))
    print("亮度:", capture.get(cv2.CAP_PROP_BRIGHTNESS))
    print("对比度:", capture.get(cv2.CAP_PROP_CONTRAST))
    print("饱和度:", capture.get(cv2.CAP_PROP_SATURATION))
    print("色调:", capture.get(cv2.CAP_PROP_HUE))
    print("图像增益:", capture.get(cv2.CAP_PROP_GAIN))
    print("曝光度:", capture.get(cv2.CAP_PROP_EXPOSURE))


def CaptureInit(
    index: int = 0, /, width: int = 640, height: int = 480, PI_MODE=True
) -> cv2.VideoCapture:
    "摄像头配置和打开"
    if PI_MODE:  # 是否使用树莓派模式（不同设备使用不同设置）
        capture = cv2.VideoCapture(index)
    else:
        capture = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    fourcc = cv2.VideoWriter_fourcc("M", "J", "P", "G")  # 设置视频流格式，从而可在树莓派上调试
    capture.set(cv2.CAP_PROP_FOURCC, fourcc)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 缓存区设置为1，防止滞后过度使得控制效果较差
    return capture


class TrackWindow:
    """
    带有滑块的视频窗口
    """

    def __init__(
        self,
        windowName: str,
        paraname: str = "value",  # 绑定参数
        para: int = 0,  # 参数初始值
        maxP: int = 255,
    ) -> None:
        self.name = paraname
        self.window = windowName
        cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
        cv2.createTrackbar(paraname, windowName, para, maxP, self.__nothing)
        # self.show()

    def __nothing(self, x):
        pass

    def getValue(self) -> int:
        return cv2.getTrackbarPos(self.name, self.window)

    def show(self, image: np.ndarray):
        cv2.imshow(self.window, image)
