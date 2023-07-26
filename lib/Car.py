import cv2
import numpy as np


class Sample:
    ROW_MODE = 0
    COLUMN_MODE = 1

    def __init__(self, position: float, weight: float) -> None:
        self.normalPos = position
        self.weight = weight
        self.otherPos = 0  # 记录旧数据

    def centerPoint(self, image: np.ndarray, mode):
        "计算采样行/列的中心点（白色部分）,仅适用于单通道图像"
        Height = image.shape[0]  # size[0]为高度
        Width = image.shape[1]  # size[0]为高度
        if mode == self.ROW_MODE:  # 行采样
            y = int(Height * self.normalPos) - 1
            row = image[y, :]
            index = np.nonzero(row)
            if index[0].size == 0:
                x = self.otherPos
            else:
                x = int(np.mean(index))
                self.otherPos = x
        else:
            x = int(Width * self.normalPos) - 1
            column = image[:, x]
            index = np.nonzero(column)
            if index[0].size == 0:
                y = self.otherPos
            else:
                y = int(np.mean(index))
                self.otherPos = y

        return (x, y)

    def drawPoint(self,
                  image: np.ndarray,
                  mode,
                  color=(70, 0, 0),
                  radius=6,
                  circlewidth=-1):
        "绘出采样点"
        Height = image.shape[0]
        Width = image.shape[1]
        if mode == self.ROW_MODE:
            cv2.circle(image,
                       (int(self.otherPos), int(self.normalPos * Height)),
                       radius, color, circlewidth)
        elif mode == self.COLUMN_MODE:
            cv2.circle(image,
                       (int(self.normalPos * Width), int(self.otherPos)),
                       radius, color, circlewidth)

    def drawLine(self,
                 image: np.ndarray,
                 mode=0,
                 color=(180, 0, 0),
                 lineWidth=2):
        "绘出采样行"
        Height = image.shape[0]
        Width = image.shape[1]
        if mode == self.ROW_MODE:
            cv2.line(image, (0, int(self.normalPos * Height)),
                     (Width, int(self.normalPos * Height)), color, lineWidth)
        elif mode == self.COLUMN_MODE:
            cv2.line(image, (int(self.normalPos * Width), 0),
                     (int(self.normalPos * Width), Height), color, lineWidth)


def getDistance(frame: np.ndarray,
                sampleList: list,
                shifting=0.,
                mode=0,
                ifDraw=False,
                ifPrint=False) -> int:
    """
    获取位置偏移量作为反馈量\\
    第一个参数为已经二值化的待处理帧(引导线处理为255，其他部分处理为0)，第二个参数作为归一化后的y轴采样位置和对应权重\\
    shifting为另设偏移量，采取归一化数值
    mode为0为行采样，mode为1为列采样\\
    返回参数为像素点数
    """
    result = 0
    Height = frame.shape[0]  # size[0]为高度
    Width = frame.shape[1]  # size[0]为高度

    # 计算每个采样处的偏移量并加权
    sample: Sample
    for sample in sampleList:
        sample.centerPoint(frame, mode)
        # 计算基准位置
        if mode == Sample.ROW_MODE:
            reference = int(Width * (0.5 + shifting))
        else:
            reference = int(Height * (0.5 + shifting))

        delta = sample.weight * (sample.otherPos - reference)
        result += delta

    if ifDraw:
        img = frame.copy()
        for sample in sampleList:
            sample.drawLine(img, mode)
            sample.drawPoint(img, mode)
        cv2.imshow(getDistance.__name__, img)

    if ifPrint:
        print('Delta Distance: ', int(result))

    return int(result)


def getLineSlope(frame: np.ndarray,
                 sampleList,
                 mode,
                 ifPrint=False,
                 ifDraw=False):
    "点集拟合直线，并计算其方向向量的水平分量、竖直分量"
    point = []
    sam: Sample
    for sam in sampleList:
        point.append(sam.centerPoint(frame, mode))
    point = np.array(point)

    output = cv2.fitLine(point, cv2.DIST_L2, 0, 0.01, 0.01)

    if ifPrint:
        print('X-component = %.2f, Y-component = %.2f' %
              (output[0], output[1]))

    if ifDraw:
        img = frame.copy()
        k = output[1] / output[0]
        (x, y) = int(output[2]), int(output[3])
        dx = 200
        dy = int(k * dx)
        cv2.line(img, (x, y), (x + dx, y + dy), 130, 3)
        cv2.imshow(getLineSlope.__name__, img)

    return output[0], output[1]
