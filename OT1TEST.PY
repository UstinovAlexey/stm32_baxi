import pyb
import machine
import micropython

micropython.alloc_emergency_exception_buf(100)

print("Start2")

btn=pyb.Pin("C13") 



class OpenTherm:
  cikles=0
  data=[]
  pin=0
  tim=0
    
  def __init__(self,pin="B0",timer_id=1): #B0-led

        OpenTherm.pin=pyb.Pin(pin,mode=pyb.Pin.OUT)
        OpenTherm.tim=pyb.Timer(timer_id,freq=2000) #timer_id,freq=2000,callback=self.mycallback())
  

  def mycallback (t):

      if OpenTherm.cikles>0:
          OpenTherm.cikles=OpenTherm.cikles-1 

              
          if OpenTherm.data[OpenTherm.cikles]:
          
           #OpenTherm.pin.on()
            OpenTherm.pin.off()
          else:
            #OpenTherm.pin.off()
            OpenTherm.pin.on()
         
          #OpenTherm.cikles=OpenTherm.cikles-1 
            
         
                 
      else:
          OpenTherm.tim.deinit()
          #OpenTherm.pin.off() # 
          OpenTherm.pin.on() # 

        
  def send(self,data):
      
      OpenTherm.data=[0,1] #start bit
      #buf=0
      #data=0
      for i in range (32):
        if data & (1<<i):
          #print(1)
          OpenTherm.data.append(0)
          OpenTherm.data.append(1)
        else:
          #print(0)
          OpenTherm.data.append(1)
          OpenTherm.data.append(0)
          
      OpenTherm.data.append(0)
      OpenTherm.data.append(1)

      OpenTherm.cikles=len(OpenTherm.data)
      print("len=",len(OpenTherm.data))
      OpenTherm.tim.freq(2000)
      OpenTherm.tim.callback(OpenTherm.mycallback)

import time

ot=OpenTherm(pin="E11")
pin_in=pyb.Pin("E13")

while (True):
    #while(btn()==1):
    #    pass
    #while(btn()==0):
    #    pass
    print("cikles=",ot.cikles)
    #ot.send(0x90014000)
    ot.send(0x10011E00)
    #0x10013C00-reg1
    #0x400C8000 -req 2
    print("cikles=",ot.cikles)
    time.sleep(1)
    print("Sended0x10013C00. Pin_in is {}".format(pin_in.value()))

import time
time.sleep(1)
print("{} End2".format(bin(255-64)))

import asyncio

class aioOpenTherm:
  def __init__(self,pin="B0",timer_id=1):
        self.cikles=0
        self.pin=pyb.Pin(pin)
        self.tim=pyb.Timer(timer_id,freq=2000) #timer_id,freq=2000,callback=self.mycallback())
        
  async def send(self,data):
    print("Send")

    self.pin.on()
    time.sleep_us(500)
    self.pin.off()
    time.sleep_us(500)
    self.pin.on()
    time.sleep_us(500)
    self.pin.off()
    time.sleep_us(500)
    self.pin.on()
    time.sleep_us(500)
    self.pin.off()
    time.sleep_us(500)
    self.pin.on()
    time.sleep_us(500)
    self.pin.off()
    time.sleep_us(500)
    self.pin.on()
    time.sleep_us(500)
    self.pin.off()
    time.sleep_us(500)
    self.pin.on()
    time.sleep_us(500)
    self.pin.off()
    
aioOT=aioOpenTherm()

async def main ():
    while True:
        await aioOT.send(12)
        print(1)
        await asyncio.sleep(1)
        print(2)
        await asyncio.sleep(1)

#asyncio.run(main())

      