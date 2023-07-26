class Para:
    def __init__(self, para, initialValue, maxP=1., minP=0.) -> None:
        self.para = para
        self.initValue = initialValue
        self.max = maxP
        self.min = minP

    def reInit(self):
        "重置参数"
        self.para = self.initValue

    def refrash(self, op, step: float):
        "更新参数"
        if op == '+':
            self.para += step
            if self.para > self.max:
                self.para = self.max
        elif op == '-':
            self.para -= step
            if self.para < self.min:
                self.para = self.min


def resetAll(paraList):
    "将全部参数初始化"
    para: Para
    for para in paraList:
        para.reInit()


def refreshPara(paraList, nameID, op, step, PARA_DICT):
    "更改某个参数"
    para = paraList[PARA_DICT[nameID]]
    para: Para
    para.refrash(op, float(step))


def parseCommand(con: str, paraList, PARA_DICT):
    "解析命令，调用相关函数"
    if con.find('_') == -1:  # 全为命令，直接解析
        # FUNC_LIST[COM_DICT[con]](paraList)
        if con == 'RST':
            resetAll(paraList)
    else:
        comList = con.split('_')  # 以'_'为分隔符，将命令拆分为列表
        if comList[0] == 'RFP':
            refreshPara(paraList, comList[1], comList[2], comList[3], PARA_DICT)
            
