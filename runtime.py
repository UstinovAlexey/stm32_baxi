import time
import umqtt
import ugit


import pyb

ledGreen = pyb.LED(1)
ledBlue = pyb.LED(2)
ledRed = pyb.LED(3)


while True:
    time.sleep(2)
    # Non-blocking wait for message
    mqttClient.check_msg()
    ledGreen.on()
    time.sleep(2)
    ledGreen.off()
    
    