"""
示例：使用串口通信与上位机进行交互
"""

import sys

sys.path.append(sys.path[0] + "\\..\\")
from lib import PiSerial
from lib import Command as cmd

# 参数字典(推荐使用，便于查询且符合预留接口)
paraDict = {"r01": cmd.Para(3), "r02": cmd.Para(2)}

if __name__ == "__main__":
    ser = PiSerial.PiSerial()
    print("begin")
    while True:
        contect: str
        contect = ser.serialRead(ifPrint=True)
        if contect is not None:
            print("in")
            # 假设上位机修改r01，按照接收数据对参数r01进行更新，
            # 具体见command传输协议.txt中RFP项
            cmd.parseCommand(contect.rstrip("\0"), paraDict)
            print(
                "\nr01 = %.3f, r02 = %.3f \n"
                % (paraDict["r01"].value, paraDict["r02"].value)
            )
            # ser.serialSend("(r01_%.3f)" % paraDict['r01'].value)
            # 参数修改回传，有效位数3位，int型
            ser.serialSend(
                cmd.makeCommand(
                    "RTP", "r01", cmd.int2str(paraDict["r01"].value, 3)
                )
            )
