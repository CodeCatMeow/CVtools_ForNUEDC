"""
树莓派与MCU的串口通信与字符串接收
"""

import serial


class PiSerial(serial.Serial):
    """
    树莓派串口通信类
    """

    def __init__(self, piport="/dev/ttyAMA2", pibaudrate=115200):
        super().__init__(port=piport, baudrate=pibaudrate)
        if not self.isOpen:
            self.open()
        self.flushInput()

    def serialSend(self, data: str, ifPrint=False):
        "发送信息到串口"
        if ifPrint:
            print(data)
        self.write(data.encode("ascii"))

    def serialRead(self, ifPrint=False) -> str:
        "从串口接收信息（非阻塞），无信息return none，多字符存在一次接收不全的情况，推荐使用serialReadStr"
        recv = self.inWaiting()
        if recv > 0:
            data = self.read(recv).decode("ascii", "ignore")
            if ifPrint:
                print(data)
            return data
        else:
            return None

    def serialReadStr(self, Start="(", End=")", ifPrint=False):
        "从串口接收str，使用起始符和结束符以确保不会丢包，未接到内容返回None，非阻塞"
        data = self.serialRead()
        if data is None:
            pass
        else:
            con = data.partition(Start)[2]  # 起始符后面的部分
            if con == "":
                return None  # 未接到有效数据
            else:
                if con.find(End) == -1:  # 未找到结束符
                    data = con
                    while data.find(End) == -1:
                        data = self.serialRead()
                        if data is None:
                            continue
                    other = data.partition(End)[0]
                    con += other
                else:
                    con = con.partition(End)[0]
                if ifPrint:
                    print(con)
                return con
