import numpy as np
import cv2


# 颜色分割的阈值
class ColorSegHSV():
    RED_RANGE_1 = (np.array([0, 43, 46]), np.array([10, 255, 255]))
    ORANGE_RANGE = (np.array([11, 43, 46]), np.array([25, 255, 255]))
    YELLOW_RANGE = (np.array([26, 43, 46]), np.array([34, 255, 255]))
    GREEN_RANGE = (np.array([35, 43, 46]), np.array([77, 255, 255]))
    CYAN_RANGE = (np.array([78, 43, 46]), np.array([99, 255, 255]))
    BLUE_RANGE = (np.array([100, 43, 46]), np.array([124, 255, 255]))
    PURPLE_RANGE = (np.array([125, 43, 46]), np.array([155, 255, 255]))
    RED_RANGE_2 = (np.array([156, 43, 46]), np.array([180, 255, 255]))

class ColorSegHLS():
    BLACK_RANGE = (np.array([0, 0, 0]), np.array([179,90, 255]))


def printVideoPara(capture:cv2.VideoCapture):
    "返回摄像头各类参数"
    print('帧宽:', capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    print('帧高:', capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print('解码方式:', capture.get(cv2.CAP_PROP_FOURCC))
    print('帧率:', capture.get(cv2.CAP_PROP_FPS))
    print('亮度:', capture.get(cv2.CAP_PROP_BRIGHTNESS))
    print('对比度:', capture.get(cv2.CAP_PROP_CONTRAST))
    print('饱和度:', capture.get(cv2.CAP_PROP_SATURATION))
    print('色调:', capture.get(cv2.CAP_PROP_HUE))
    print('图像增益:', capture.get(cv2.CAP_PROP_GAIN))
    print('曝光度:', capture.get(cv2.CAP_PROP_EXPOSURE))