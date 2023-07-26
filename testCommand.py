from lib import PiSerial
from lib import Command

r1 = 0.3
r2 = 0.3

PARA_DICT = {'r01': 0, 'ro2': 1}
paraList = [Command.Para(r1, 0.3),
            Command.Para(r2, 0.2)]
# paraDict = {'r01': Command.Para(r1, 0.3), 
#             'r02': Command.para(r2, 0.2)}

if __name__ == '__main__':
    ser = PiSerial.PiSerial()
    print('begin')
    while True:
        contect = ser.serialRead(ifPrint=True)
        if contect is not None:
            print('in')
            Command.parseCommand(contect.rstrip('\0'), paraList, PARA_DICT)
            print('\nr1 = %.3f, r2 = %.3f \n' % (r1, r2))
            print('\nr01 = %.3f, r02 = %.3f \n' % (paraList[0].para, paraList[1].para))
            ser.serialSend("(r01_%.3f)" % paraList[0].para)
