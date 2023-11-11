# D2 (PF15) MasterIn 
# D3 (PE13) SlaveIn
# D4 (PF14) MasterOut
# D5 (PE11) SlaveOut
# Slave- to Boiler
# Master- to Termostat

import pyb,time

pinMasterOut = pyb.Pin('F14', pyb.Pin.OUT_PP)
pinSlaveOut = pyb.Pin('E11', pyb.Pin.OUT_PP)

def callback_MasterIn(line):
    print("MasterIn line =", line)
def callback_SlaveIn(line):
    print("SlaveIn line =", line)

extint_MasterIn = pyb.ExtInt("F15", pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback_MasterIn)
extint_SlaveIn = pyb.ExtInt("E13", pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback_SlaveIn)


ledGreen = pyb.LED(1)
ledBlue = pyb.LED(2)
ledRed = pyb.LED(3)


while True:
    print(".",end="")
    time.sleep(1)
    pinMasterOut.off()
    ledGreen.off()
    
    pinSlaveOut.off()
    ledRed.off()
    

    time.sleep(1)
    pinMasterOut.off()
    ledGreen.off()
    pinSlaveOut.off()
    ledRed.off()
    
    time.sleep(1)
    pinMasterOut.off()
    ledGreen.off()
    pinSlaveOut.off()
    ledRed.off()
    
    time.sleep(1)
    pinMasterOut.off()
    ledGreen.off()
    pinSlaveOut.off()
    ledRed.off()
