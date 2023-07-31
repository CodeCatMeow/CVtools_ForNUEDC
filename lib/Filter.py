"""
滤波器，包含常用滤波方法
"""
import numpy as np


class Filter:
    # 滤波方法
    FILTER_LINIT = 0  # 限幅滤波
    FILTER_MEDIAN = 1  # 中位数滤波
    FILTER_AVERAGE_ARITHMETIC = 2  # 算术平均值滤波
    FILTER_LAG_FIRSEORDER = 3  # 一阶滞后滤波

    # 触发方法
    TRIGGER_NOTIMES = 0  # 建立滤波器后立即触发
    TRIGGER_TENTIMES = 1  # 建立滤波器后，连续10次数据稳定在Range范围内后触发

    def __init__(self,
                 filterType,
                 triggerType,
                 triggerRange=None,
                 filterRange=None,
                 proportion=None) -> bool:
        self.filterType = filterType
        if filterType == self.FILTER_LINIT:
            self.range = filterRange
            self.old = 0
        elif filterType == self.FILTER_MEDIAN:
            pass
        elif filterType == self.FILTER_AVERAGE_ARITHMETIC:
            pass
        elif filterType == self.FILTER_LAG_FIRSEORDER:
            pass
        else:
            return False

        if triggerType == self.TRIGGER_NOTIMES:
            self.isopen = True
        else:
            self.isopen = False
            if triggerType == self.TRIGGER_TENTIMES:
                self.triggerList = []
                self.triggerRange = triggerRange

    def doing(self, data):
        "进行计算，仅当触发器被触发时开始"
        if self.isopen or self.__trigger(data):
            if self.filterType == self.FILTER_LINIT:
                return self.__limitFilter(data, self.old, self.range)
            elif self.filterType == self.FILTER_MEDIAN:
                pass
            elif self.filterType == self.FILTER_AVERAGE_ARITHMETIC:
                pass
            elif self.filterType == self.FILTER_LAG_FIRSEORDER:
                pass

    def __trigger(self, data) -> bool:
        if self.triggerList == self.TRIGGER_NOTIMES:
            return True
        else:
            if self.triggerList == self.TRIGGER_TENTIMES:
                if len(self.triggerList) < 10:
                    return False
                else:
                    # 数据更新
                    self.triggerList.insert(0, data)
                    self.triggerList.pop()
                    # 判断
                    aver = np.mean(self.triggerList)
                    if abs(aver - data) < self.triggerRange:
                        self.isopen = True
                        return True
                    else:
                        return False

    @staticmethod
    def __limitFilter(data, lastData, Amplitude):
        '''
        A、名称：限幅滤波法（又称程序判断滤波法）
        B、方法：
            根据经验判断，确定两次采样允许的最大偏差值（设为A），
            每次检测到新值时判断：
            如果本次值与上次值之差<=A，则本次值有效，
            如果本次值与上次值之差>A，则本次值无效，放弃本次值，用上次值代替本次值。
        C、优点：
            能有效克服因偶然因素引起的脉冲干扰。
        D、缺点：
            无法抑制那种周期性的干扰。
        '''
        if abs(data - lastData) < Amplitude:  # 限幅
            return data
        else:
            return lastData
