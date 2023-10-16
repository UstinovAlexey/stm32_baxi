import network
import time

eth=network.LAN()
eth.active(1)
for i in range (5):
    
    print(eth.ifconfig())
    print ("Hello!",i,eth.isconnected())
    
    time.sleep(3)
    




