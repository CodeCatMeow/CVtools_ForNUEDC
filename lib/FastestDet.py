"""
应用FastestDet神经网络进行目标识别
"""

import os

import cv2
import numpy as np

print(os.sys.path)

from lib.ROI import ROI


def sigmoid(x):
    "sigmoid函数"
    return 1.0 / (1 + np.exp(-x))


def tanh(x):
    "tanh函数"
    return 2.0 / (1 + np.exp(-2 * x)) - 1


class DetOutput:
    "FastestDet神经网络的的直接输出结果"

    def __init__(self, cx, cy, x1, y1, x2, y2, score, className) -> None:
        """
        cx, cy: 检测框归一化的中心坐标
        x1, y1: 检测框归一化的左上角坐标
        x2, y2: 检测框归一化的右下角坐标
        score: 检测框置信度
        className: 检测框从属类别的名称
        """
        self.cx = cx
        self.cy = cy
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.score = score
        self.className = className

    def actualize(self, image: np.ndarray):
        "获取检测结果在image中的实际坐标，返回Tuple（中心坐标、左上坐标、右下坐标）"
        imageHeight = image.shape[0]
        imageWidth = image.shape[1]
        cxa = int(self.cx * imageHeight)
        x1a = int(self.x1 * imageHeight)
        x2a = int(self.x2 * imageHeight)
        cya = int(self.cy * imageWidth)
        y1a = int(self.y1 * imageWidth)
        y2a = int(self.y2 * imageWidth)
        return (cxa, cya), (x1a, y1a), (x2a, y2a)

    def draw(
        self,
        image: np.ndarray,
        color=(180, 0, 0),
        radius=4,
        textwidth=2,
        circlewidth=-1,
        rowHeight=20,
    ):
        "绘出检测结果于image中"
        center, _, _ = self.actualize(image)
        cv2.circle(image, center, radius, color, circlewidth)
        cv2.putText(
            image,
            "%.2f" % self.score,
            (center[0], center[1] - radius),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            textwidth,
        )
        cv2.putText(
            image,
            "'%s'" % self.className,
            (center[0], center[1] - radius - rowHeight),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            textwidth,
        )


class FastestDet:
    "使用OpenCV调用ONNX格式的FastestDet神经网络"

    def __init__(
        self,
        inputWidth: int,
        inputHeight: int,
        path: str,
        confThreshold: float = 0.5,
        nmsThreshold: float = 0.4,
        ifDrawOutput: bool = False,
    ) -> None:
        """
        inputWidth: 输入图片宽
        inputHeight: 输入图片长
        path: 模型目录
        confThreshold: 置信度阈值
        nmsThreshold: 非极大值抑制阈值
        """
        # path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        #                     "models")
        path_names = os.path.join(path, "category.names")  # 识别类别
        path_onnx = os.path.join(path, "FastestDet.onnx")
        self.classes = list(
            map(lambda x: x.strip(), open(path_names, "r").readlines())
        )
        self.inputWidth = inputWidth
        self.inputHeight = inputHeight
        self.net = cv2.dnn.readNet(path_onnx)
        self.confThreshold = confThreshold
        self.nmsThreshold = nmsThreshold
        self.ifDrawOutput = ifDrawOutput
        self.outputlist = list()

    def __imageFormat(self, image: np.ndarray) -> np.ndarray:
        "输入图像与模型接口的对齐预处理"
        output = cv2.resize(
            image.astype(np.float32),
            (self.inputWidth, self.inputHeight),
            interpolation=cv2.INTER_AREA,
        )
        output = output.transpose(2, 0, 1)  # 调换通道
        result = (
            output.reshape((1, 3, self.inputHeight, self.inputWidth)) / 255.0
        )
        return result.astype("float32")

    def __nms(self, dets) -> list:
        """
        非极大值抑制
        dets: [[x1, y1, x2, y2, score, ...], [x1, y1, x2, y2, score, ...], ...]
        """
        if dets.shape[0] == 0:
            # if len(self.outputlist) == 0:
            return []
        x1 = dets[:, 0]
        y1 = dets[:, 1]
        x2 = dets[:, 2]
        y2 = dets[:, 3]
        scores = dets[:, 4]
        areas = (x2 - x1) * (y2 - y1)  # 求每个bbox的面积
        order = scores.argsort()[::-1]  # 对分数进行倒排序
        keep = []  # 用来保存最后留下来的bboxx下标

        while order.size > 0:
            i = order[0]  # 无条件保留每次迭代中置信度最高的bbox
            keep.append(i)

            # 计算置信度最高的bbox和其他剩下bbox之间的交叉区域
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            # 计算置信度高的bbox和其他剩下bbox之间交叉区域的面积
            w = np.maximum(0.0, xx2 - xx1)
            h = np.maximum(0.0, yy2 - yy1)
            inter = w * h

            # 求交叉区域的面积占两者（置信度高的bbox和其他bbox）面积和的必烈
            ovr = inter / (areas[i] + areas[order[1:]] - inter)

            # 保留ovr小于thresh的bbox，进入下一次迭代。
            inds = np.where(ovr <= self.nmsThreshold)[0]

            # 因为ovr中的索引不包括order[0]所以要向后移动一位
            order = order[inds + 1]

        output = []
        for i in keep:
            output.append(dets[i].tolist())

        return output

    def __postProssing(self, featureMap) -> list:
        "神经网络的预测结果的后处理，得到：归一化的中心坐标，归一化的左上、右下坐标，置信度，类别名称"
        predictions = []

        # 输出特征图转置: CHW -> HWC
        feature_map = featureMap.transpose(1, 2, 0)
        # 输出特征图的宽高
        feature_map_height = feature_map.shape[0]
        feature_map_width = feature_map.shape[1]

        # 特征图后处理
        for h in range(feature_map_height):
            for w in range(feature_map_width):
                data = feature_map[h][w]

                # 解析检测框置信度
                object_score, class_score = data[0], data[5:].max()
                score = (object_score**0.6) * (class_score**0.4)

                # 阈值筛选
                if score > self.confThreshold:
                    # 检测框类别
                    class_index = np.argmax(data[5:])
                    # 检测框中心点偏移
                    x_offset, y_offset = tanh(data[1]), tanh(data[2])
                    # 检测框归一化后的宽高
                    box_width, box_height = sigmoid(data[3]), sigmoid(data[4])
                    # 检测框归一化后中心点
                    box_cx = (w + x_offset) / feature_map_width
                    box_cy = (h + y_offset) / feature_map_height

                    # cx,cy,w,h => x1, y1, x2, y2
                    x1, y1 = (
                        box_cx - 0.5 * box_width,
                        box_cy - 0.5 * box_height,
                    )
                    x2, y2 = (
                        box_cx + 0.5 * box_width,
                        box_cy + 0.5 * box_height,
                    )

                    # 获取标签名
                    # className = self.classes[int(class_index)]

                    predictions.append(
                        [x1, y1, x2, y2, score, class_index, box_cx, box_cy]
                    )

        output = self.__nms(np.array(predictions))
        self.outputlist.clear()
        return list(
            map(
                lambda x: DetOutput(
                    x[6],
                    x[7],
                    x[0],
                    x[1],
                    x[2],
                    x[3],
                    x[4],
                    self.classes[int(x[5])],
                ),
                output,
            )
        )

    def putout(self, image: np.ndarray) -> list:
        "输出检测结果，输入待测帧，输出结果为元素为DetOutput类的列表，已经经过后处理和预处理"
        # 模型推理
        self.net.setInput(self.__imageFormat(image))
        featureMap = self.net.forward(self.net.getUnconnectedOutLayersNames())[
            0
        ][0]

        # 特征图后处理
        self.outputlist = self.__postProssing(featureMap)

        if self.ifDrawOutput:
            output: DetOutput
            for output in self.outputlist:
                output.draw(image)
        return self.outputlist

    def screenDetOutput(self, ROI: ROI) -> list:
        "筛除重合的检测结果中心坐标处于ROI之外的检测结果，并将结果返回（本函数对结果列表本身操作）"
        index = list()  # 需要删除的检测结果的索引

        for i in range(0, len(self.outputlist)):
            if not ROI.isInside(
                (self.outputlist[i].cx, self.outputlist[i].cy)
            ):
                index.append(i)

        index.sort(reverse=True)
        for k in index:
            del self.outputlist[k]

        return self.outputlist
