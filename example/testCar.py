"""
示例：使用Car.py内的函数
"""

import cv2

import sys

sys.path.append(sys.path[0] + "\\..\\")
from lib import Car

# 采样列表，列表内为采样类Sample的实例化
sam = [Car.Sample(0.3, 0.3), Car.Sample(0.5, 0.4), Car.Sample(0.7, 0.3)]

if __name__ == "__main__":
    image = cv2.imread("example/test/4.png", cv2.IMREAD_GRAYSCALE)

    Car.getDistance(
        image, sam, 0, Car.Sample.SAMPLE_COLUMN, ifDraw=True, ifPrint=True
    )

    Car.getLineSlope(
        image, sam, Car.Sample.SAMPLE_COLUMN, ifPrint=True, ifDraw=True
    )

    cv2.imshow("img", image)

    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
