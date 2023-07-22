import cv2
import numpy as np


class ROIArea:
    "从图像中截取感兴趣区域，使用归一化坐标和长宽进行定义，得到具体坐标和长宽"

    def __init__(self, image: np.ndarray, x1: float, y1: float, width: float,
                 height: float, ifExist=True):
        "ROI类的实例化，使用归一化的左上点横纵坐标和归一化的长宽"
        imageHeight = image.shape[0]
        imageWidth = image.shape[1]
        self.width = int(width * imageWidth)
        self.height = int(height * imageHeight)
        self.x1 = int(x1 * imageWidth)
        self.y1 = int(y1 * imageHeight)
        if ifExist:
            self.ROI = image[self.y1:(self.y1 + self.height), self.x1:(self.x1 + self.width)].copy()

    def draw(self, image: np.ndarray, color=(180, 0, 0), width=3):
        "将ROI区域在图片上绘制出来"
        cv2.rectangle(image, (self.x1, self.y1),
                      (self.x1 + self.width, self.y1 + self.height), color,
                      width)

    def isInside(self, point):
        "判断point点是否位于ROI区域内"
        x, y = point
        if (x < self.x1 or x > self.x1 + self.width) or (y < self.y1 or y > self.y1 + self.height):
            return False
        else:
            return True
