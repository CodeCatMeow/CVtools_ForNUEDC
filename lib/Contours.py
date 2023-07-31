"""
轮廓处理常用函数
"""

import cv2
import numpy as np

AREA_COUNT_MODE = 0
AREA_GREEN_MODE = 1


def countArea(height, width, contour) -> int:
    "计算轮廓内非0像素点个数"
    mask = np.zeros((height, width))
    fill = cv2.fillConvexPoly(mask, contour, 255)
    return cv2.countNonZero(fill)


def inAreaRange(image: np.ndarray, contours: list, maxArea, minArea,
                mode) -> list:
    "将列表中面积处于上下阈值内的轮廓提取出来"
    succ = []
    if mode == AREA_COUNT_MODE:
        for i in range(len(contours)):
            area = countArea(image.shape[0], image.shape[1], contours[i])
            # 面积过滤
            if area >= minArea and area <= maxArea:
                succ.append(contours[i])
        return succ
    elif mode == AREA_GREEN_MODE:
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            # 面积过滤
            if area >= minArea and area <= maxArea:
                succ.append(contours[i])
        return succ
    else:
        return None


def getCenter(contour):
    "计算轮廓重心"
    moment = cv2.moments(contour)
    cx = int(moment['m10'] / moment['m00'])
    cy = int(moment['m01'] / moment['m00'])
    return (cx, cy)


def maxArea(contours):
    "返回列表中面积最大的轮廓"
    return max(contours, key=lambda x: cv2.contourArea(x))