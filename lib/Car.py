"""
车辆循迹常用函数

本文件包含了：
采样类Sample及其方法
获取多个采样行/列的有效重心到行/列中心的像素距离并将其加权求和的方法getDistance
多个采样行/列的有效重心拟合直线的方向向量获取函数getLineSlope
"""

import cv2
import numpy as np


class Sample:  # 视野采集样本类
    # 类型区别，用于采样模式选择
    SAMPLE_ROW = 0
    SAMPLE_COLUMN = 1

    # 本轮检测结果无效时是否保持旧数据，用于模式选择
    VALUE_KEEPOLD = 0
    VALUE_NOTKEEPOLD = 1

    def __init__(
        self, position: float, weight: float, *, maxRatio=1.0, minRatio=0.0
    ) -> None:
        self.position = position  # 位置
        self.weight = weight  # 权重
        self.value = 0  # 记录目的数据
        self.existence = False  # 数据有效性
        self.ratioUpper = maxRatio  # 占比上限
        self.ratioLower = minRatio  # 占比下限

    def checkBeing(self, image: np.ndarray, samplizeMode=SAMPLE_ROW) -> bool:
        "检查图像采样位置是否存在有效值"
        Height = image.shape[0]  # size[0]为高度
        Width = image.shape[1]  # size[0]为高度
        if samplizeMode == self.SAMPLE_ROW:  # 行采样
            y = int(Height * self.position) - 1
            row = image[y, :]
            index = np.nonzero(row)
            if index[0].size == 0:  # 若未检测到
                self.existence = False  # 这里实际完成存在性/有效性设置
                return False
            else:
                self.existence = True
                return True
        else:
            x = int(Width * self.position) - 1
            column = image[:, x]
            index = np.nonzero(column)
            if index[0].size == 0:  # 若未检测到
                self.existence = False
                return False
            else:
                self.existence = True
                return True

    def centerPoint(
        self,
        image: np.ndarray,
        samplizeMode=SAMPLE_ROW,
        valueHandleMode=VALUE_NOTKEEPOLD,
    ):
        "计算采样行/列的有效区域中心点（白色部分，若采集黑色部分可以图片反色输入q）,仅适用于单通道图像"
        Height = image.shape[0]  # size[0]为高度
        Width = image.shape[1]  # size[1]为宽度
        if samplizeMode == self.SAMPLE_ROW:  # 行采样
            y = int(Height * self.position) - 1
            row = image[y, :]
            index = np.nonzero(row)
            lengthUpper = int(self.ratioUpper * Width)
            lengthLower = int(self.ratioLower * Width)
            if (
                index[0].size <= lengthLower or index[0].size >= lengthUpper
            ):  # 若未检测到或者检测有效区域处于设定范围之外
                self.existence = False
                if valueHandleMode == self.VALUE_NOTKEEPOLD:
                    x = int(Width / 2)
                    self.value = x
                elif valueHandleMode == self.VALUE_KEEPOLD:
                    x = self.value
                else:
                    return None
            else:  # 检测到
                self.existence = True
                x = int(np.mean(index))
                self.value = x
        else:
            x = int(Width * self.position) - 1
            column = image[:, x]
            index = np.nonzero(column)
            lengthUpper = int(self.ratioUpper * Height)
            lengthLower = int(self.ratioLower * Height)
            if (
                index[0].size <= lengthLower or index[0].size >= lengthUpper
            ):  # 若未检测到或者检测处于范围之外
                self.existence = False
                if valueHandleMode == self.VALUE_NOTKEEPOLD:
                    y = int(Height / 2)
                    self.value = y
                elif valueHandleMode == self.VALUE_KEEPOLD:
                    y = self.value
                else:
                    return None
            else:
                self.existence = True
                y = int(np.mean(index))
                self.value = y

        return (x, y)

    def drawPoint(
        self,
        image: np.ndarray,
        mode,  # 行列采样模式
        color=(70, 0, 0),
        radius=6,
        circlewidth=-1,
    ):
        "绘出采样点"
        Height = image.shape[0]
        Width = image.shape[1]
        if mode == self.SAMPLE_ROW:
            cv2.circle(
                image,
                (int(self.value), int(self.position * Height)),
                radius,
                color,
                circlewidth,
            )
        elif mode == self.SAMPLE_COLUMN:
            cv2.circle(
                image,
                (int(self.position * Width), int(self.value)),
                radius,
                color,
                circlewidth,
            )

    def drawLine(
        self, image: np.ndarray, mode=0, color=(180, 0, 0), lineWidth=2
    ):
        "绘出采样行"
        Height = image.shape[0]
        Width = image.shape[1]
        if mode == self.SAMPLE_ROW:
            cv2.line(
                image,
                (0, int(self.position * Height)),
                (Width, int(self.position * Height)),
                color,
                lineWidth,
            )
        elif mode == self.SAMPLE_COLUMN:
            cv2.line(
                image,
                (int(self.position * Width), 0),
                (int(self.position * Width), Height),
                color,
                lineWidth,
            )


def getDistance(
    frame: np.ndarray,
    sampleList: list,
    shifting=0.0,
    samplizeMode=Sample.SAMPLE_ROW,
    valueHandleMode=Sample.VALUE_NOTKEEPOLD,
    *,
    ifDraw=False,
    ifPrint=False
) -> int:
    """
    获取位置偏移量作为反馈量\\
    第一个参数为已经二值化的待处理帧(引导线处理为255，其他部分处理为0)\\
    第二个参数作为归一化后的y轴采样位置和对应权重\\
    shifting为另设偏移量，采取归一化数值
    mode为0为行采样，mode为1为列采样(建议使用采样类预设变量)\\
    返回距离单位为像素点数\\
    默认不进行绘制和命令行输出
    """
    result = 0
    Height = frame.shape[0]  # size[0]为高度
    Width = frame.shape[1]  # size[0]为高度

    # 计算每个采样处的偏移量并加权
    sample: Sample
    for sample in sampleList:
        sample.centerPoint(frame, samplizeMode, valueHandleMode)
        # 计算基准位置
        if samplizeMode == Sample.SAMPLE_ROW:
            reference = int(Width * (0.5 + shifting))
        else:
            reference = int(Height * (0.5 + shifting))

        delta = sample.weight * (sample.value - reference)
        result += delta

    if ifDraw:
        img = frame.copy()
        for sample in sampleList:
            sample.drawLine(img, samplizeMode)
            sample.drawPoint(img, samplizeMode)
        cv2.imshow(getDistance.__name__, img)

    if ifPrint:
        print("Delta Distance: ", int(result))

    return int(result)


def getLineSlope(
    frame: np.ndarray,
    sampleList,
    samplizeMode=Sample.SAMPLE_ROW,
    valueHandleMode=Sample.VALUE_NOTKEEPOLD,
    ifPrint=False,
    ifDraw=False,
):
    "点集拟合直线，并计算其方向向量的水平分量、竖直分量"
    point = []
    sam: Sample
    for sam in sampleList:
        point.append(sam.centerPoint(frame, samplizeMode, valueHandleMode))
    point = np.array(point)

    output = cv2.fitLine(point, cv2.DIST_L2, 0, 0.01, 0.01)

    if ifPrint:
        print(
            "X-component = %.2f, Y-component = %.2f" % (output[0], output[1])
        )

    if ifDraw:
        img = frame.copy()
        k = output[1] / output[0]
        (x, y) = int(output[2]), int(output[3])
        dx = 200
        dy = int(k * dx)
        cv2.line(img, (x, y), (x + dx, y + dy), 130, 3)
        cv2.imshow(getLineSlope.__name__, img)

    return output[0], output[1]
