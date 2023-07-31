from lib import PiSerial
from lib import Command

# r1 = 0.3
# r2 = 0.3

# PARA_DICT = {'r01': 0, 'ro2': 1}
# paraList = [Command.Para(r1, 0.3),
#             Command.Para(r2, 0.2)]
paraDict = {'r01': Command.Para(0.3),
            'r02': Command.Para(0.2)}

if __name__ == '__main__':
    ser = PiSerial.PiSerial()
    print('begin')
    while True:
        contect = ser.serialRead(ifPrint=True)
        if contect is not None:
            print('in')
            Command.parseCommand(contect.rstrip('\0'), paraDict)
            print('\nr01 = %.3f, r02 = %.3f \n' % (paraDict['r01'].value, paraDict['r02'].value))
            ser.serialSend("(r01_%.3f)" % paraDict['r01'].value)
