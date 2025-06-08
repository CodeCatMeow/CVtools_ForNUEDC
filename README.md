# 基于树莓派、面向电赛的的图像处理python代码

可用于电子设计大赛（控制方向）的一些图像识别代码。基于python，适用于Raspberry Pi平台。

## 目录

<!-- @import "[TOC]" {cmd="toc" depthFrom=2 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [目录](#目录)
- [安装](#安装)
- [使用说明](#使用说明)
  - [项目配置](#项目配置)
  - [主要功能介绍](#主要功能介绍)
    - [功能函数](#功能函数)
    - [工具代码](#工具代码)
  - [使用示例](#使用示例)
- [相关仓库](#相关仓库)
- [贡献](#贡献)
- [使用许可](#使用许可)

<!-- /code_chunk_output -->

## 安装

本项目基于树莓派4B和工业摄像头，需要与上位机进行通信（项目使用STM32进行实践）。

- 树莓派4B需要预装python及相关包。
  - opencv
- 个人电脑已验证如下版本可以运行。
  - opencv-python==4.9.0.80
- 使用[FastestDet](https://github.com/dog-qiuqiu/FastestDet)进行目标识别，模型需要自行训练并导出ONNX格式。

需要指出的是，若载入ONNX网络时出现类似下面的错误：

```
error: OpenCV(x.x.x) Error: Number of input channels should be multiple of 24 but got 1 in function ‘cv::dnn::ConvolutionLayerImpl::getMemoryShapes’
```

可考虑更换opencv版本。

## 使用说明

### 项目配置

- lib 目录内为相关库函数。
- example 目录内为示例。

### 主要功能介绍

#### 功能函数

功能函数位于lib目录内。

- `Car.py` [车辆循迹](lib/Car.py)
  - 多行采样与距离：引导线到视野中心的距离加权平均。
  - 多行采样与角度：拟合得到引导线的方向向量。
- `Command.py` [命令交互](lib/Command.py)
  - 参数处理：基于上位机命令，程序运行时的参数调整。
  - 指令分析：从上位机所得命令的解析和响应处理（命令格式需要遵循[预设传输协议](lib/command%E4%BC%A0%E8%BE%93%E5%8D%8F%E8%AE%AE.txt)）。
  - 数据解析：对上位机发送数据的解析（数据格式需要遵循[预设传输协议](lib/command%E4%BC%A0%E8%BE%93%E5%8D%8F%E8%AE%AE.txt)）。
  - 命令生成：将参数、数据等按照指定格式转化为命令，便于向上位机发送。
- `Contours.py` [轮廓处理](lib/Contours.py)
  - 轮廓过滤：通过面积阈值过滤所得轮廓。
  - 计算轮廓重心。
  - 提取（面积）最大轮廓。
- `FastestDet.py` [基于FastestDet神经网络的目标识别](lib/FastestDet.py)
  - 读取ONNX格式的模型。
  - 输入图片，获得模型输出。
- `Hop.py` [信号跳变检测](lib/Hop.py)
  - 信号上升沿&下降沿检测。
- `PiSerial.py` [与上位机串口通信](lib/PiSerial.py)
  - 发送信息到串口。
  - 从串口读取一次信息。
  - 从串口中读取起始符和结束符之间的内容。
- `ROI.py` [感兴趣区域提取](lib/ROI.py)
  - 提取or复制图像中的一部分区域（ROI）。
  - 判断某一点是否位于ROI内。
  - 计算ROI内黑白像素比例。
- `Video.py` [摄像头设置和调整](lib/Video.py)
  - 常用颜色分割阈值
    - HSV：七色、RGB三通道。
    - HLS：黑色。
  - 返回摄像头硬件参数。
  - 摄像头配置和打开。
  - 参数可视化调整：生成带有滑块的视频窗口并将滑块值与参数对应。

更为细致的介绍，请阅读相关代码。

#### 工具代码

- `AdjectPara.py` [工具：使用带有滑块的窗口对相机参数进行实时调整](AdjectPara.py)
- `GetCoordinate.py` [工具：点击屏幕显示坐标，命令行输出坐标和归一化坐标，按下退格键清零](GetCoordinate.py)
- `GetRange.py` [工具：使用带有滑块的窗口对阈值进行调整（以黑色提取为例）](GetRange.py)
- `GetROI.py` [工具：使用鼠标拖动确定ROI区域，命令行输出坐标和归一化坐标](GetROI.py)
- `GetTransMatrix.py` [工具：通过在屏幕左键单击4个点，生成并获取仿射变换矩阵。手动按下退格键进行重置/清零](GetTransMatrix.py)

### 使用示例

使用示例位于example目录内。

- `testCar.py`[Car.py的示例](example/testCar.py)
  - 运行后，输出图像示例和计算输出。
- `testCommand.py`[Command.py和PiSerial.py的示例](example/testCommand.py)
  - 假设上位机修改r01，按照接收数据对参数r01进行更新，并将修改后数据回传。
- `testFastestDet.py`[FastestDet.py的示例](example/testFastestDet.py)
  - 使用预训练的FastestDet网络对图片中1~8的数字进行目标识别，标出数字位置和置信度。
- `GetCoordinate.py`[Video.py的示例](GetCoordinate.py)
- `testROI.py`[ROI.py的示例](example/testROI.py)
  - HSV空间的红色提取
  - 划分ROI区域并计算黑白比例、判断点是否位于ROI内。

## 相关仓库

[⚡FastestDet⚡](https://github.com/dog-qiuqiu/FastestDet?tab=readme-ov-file) — 全新设计的超实时Anchor-free目标检测算法

## 贡献

本项目部分程序参考了互联网资料，同时也离不开老师、前辈、同仁们的无私帮助。

本项目欢迎任何人进行补充。

## 使用许可

[BSD 3-Clause](LICENSE) © CodeCatMeow
