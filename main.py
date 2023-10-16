# main.py -- put your code here!
from pyb import LED
import time

ledGreen=LED(1)
ledBlue=LED(2)
ledRed=LED(3)

while True:
    ledGreen.on()
    time.sleep(1)

    ledGreen.off()
    ledRed.off()
    ledBlue.off()
    
    ledRed.on()
    time.sleep(1)

    ledGreen.off()
    ledRed.off()
    ledBlue.off()
    
    ledBlue.on()
    time.sleep(1)

    ledGreen.off()
    ledRed.off()
    ledBlue.off()



    
red.on()