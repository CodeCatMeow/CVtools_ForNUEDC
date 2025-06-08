"""
轮廓处理常用函数
"""

import cv2
import numpy as np

# 面积计算模式选择，像素点个数or格林公式计算面积
AREA_COUNT_MODE = 0
AREA_GREEN_MODE = 1


def countArea(height, width, contour) -> int:
    "计算轮廓内非0像素点个数"
    mask = np.zeros((height, width))
    fill = cv2.fillConvexPoly(mask, contour, 255)
    return cv2.countNonZero(fill)


def inAreaRange(
    image: np.ndarray, contours: list, maxArea, minArea, mode
) -> list:
    "将轮廓列表contours中面积处于上下阈值内的轮廓提取出来"
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
    if moment["m00"] == 0:
        return None
    cx = int(moment["m10"] / moment["m00"])
    cy = int(moment["m01"] / moment["m00"])
    return (cx, cy)


def maxArea(contours, n=1):
    "返回列表中面积最大的前n个轮廓，若n为1则直接返回轮廓，否则返回轮廓列表"
    if len(contours) == 0:
        return None

    area = []
    conlist = []
    for contour in contours:
        area.append(cv2.contourArea(contour))

    for i in range(n):
        maxIndex = np.argmax(np.array(area))
        conlist.append(contours[maxIndex])
        area[maxIndex] = 0

    if n == 1:
        return conlist[0]
    else:
        return conlist
