"""
关于树莓派与MCU互传命令的处理函数库
"""


class Para:
    def __init__(self, initialValue, maxP=1., minP=0., resetFunc = None) -> None:
        self.value = initialValue
        self.initValue = initialValue
        self.max = maxP
        self.min = minP
        self.resetFunc = resetFunc

    def reSet(self):
        "重置参数"
        if self.resetFunc is None:
            self.value = self.initValue
        else:
            self.resetFunc(self.value)

    def refrash(self, op, step: float):
        "更新参数"
        if op == '+':
            self.value += step
            if self.value > self.max:
                self.value = self.max
        elif op == '-':
            self.value -= step
            if self.value < self.min:
                self.value = self.min


def resetAll(paraDict: dict):
    "将全部参数初始化"
    para: Para
    # 参数作为字典的value,对字典的value进行遍历
    for para in paraDict.values():
        para.reSet()


def refreshPara(paraDict, nameID, op, step):
    "更改某个参数"
    para = paraDict[nameID]
    para: Para
    para.refrash(op, float(step))


def parseCommand(con: str, paraDict):
    "解析命令，调用相关函数"
    if con.find('_') == -1:  # 全为命令，直接解析
        if con == 'RST':
            resetAll(paraDict)
            return None
    else:
        comList = con.split('_')  # 以'_'为分隔符，将命令拆分为列表
        if comList[0] == 'RFP':
            refreshPara(paraDict, comList[1], comList[2], comList[3])
            return None
        elif comList[0] == 'CTC':
            return comList[1]


def makeCommand(prefix: str, *contents) -> str:
    "发送命令，prefix为前导符，content为内容，使用\'_\'分隔开"
    command = '('
    command += prefix
    for content in contents:
        command += '_' + content
    command += ')'
    return command


def whatItems(contect: str, prefix: str, number: int):
    "解析形如‘Axxx’的数据，其中A为前导符prefix， 后跟数据number位，直接返回字符串"
    index = contect.find(prefix)
    if index == -1:
        if number == 0:
            return False
        else:
            return None
    else:
        if number == 0:
            return True
        else:
            return contect[index + len(prefix):index + len(prefix) + number]


def int2str(number: int, digit: int) -> str:
    "将数字转化为X-XXX格式，有效数字部分位数为digit，不足用0补齐，多出不考虑"
    data = ''
    # 判断正负，正为‘1’，负为‘0’
    if number < 0:
        data += '0'
        number *= -1
    else:
        data += '1'
    # 追加偏移量数字
    data += str(number).zfill(digit)
    return data


def bool2str(judge: bool) -> str:
    "将布尔量转化为字符0和1"
    if judge:
        return '1'
    else:
        return '0'


def dataTreatment(*data) -> str:
    "将数据转化为待发送字符串，None用X占位"
    con = ''
    for datum in data:
        if datum[0] is None:
            con += 'X' * datum[1]
        elif isinstance(datum[0], bool):
            con += bool2str(datum[0])
        elif isinstance(datum[0], int):
            con += int2str(datum[0], datum[1])

    return con