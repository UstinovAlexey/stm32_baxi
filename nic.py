import network
import time

eth=network.LAN()
try:
    eth.active(1)
    for i in range (5):
    
        print(eth.ifconfig())
        print ("Waiting DHCP")
    
        if eth.isconnected():
            break
    
        time.sleep(3)
except:
    print ("No Ethernet connection")
    




