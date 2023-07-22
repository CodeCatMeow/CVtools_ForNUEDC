import serial


class PiSerial(serial.Serial):
    """
    树莓派串口通信类
    """
    def __init__(self, piport='/dev/ttyAMA2', pibaudrate=115200):
        super().__init__(port=piport, baudrate=pibaudrate)
        if not self.isOpen:
            self.open()
        self.flushInput()

    def SerialSend(self, data: str, ifPrint=False):
        "发送信息到串口"
        if ifPrint:
            print(data)
        self.write(data.encode('ascii'))

    def SerialRead(self, ifPrint=False) -> str:
        "从串口接收信息（非阻塞），无信息return none"
        recv = self.inWaiting()
        if recv > 0:
            data = self.read(recv)
            if ifPrint:
                print(data.decode('ascii', 'ignore'))
            return data.decode('ascii', 'ignore')
        else:
            return None
            